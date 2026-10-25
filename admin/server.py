#!/usr/bin/env python3
"""로컬 전용 글쓰기 admin 서버. 사용법은 admin/README.md 참고."""
import argparse
import atexit
import datetime
import json
import re
import signal
import subprocess
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = (ROOT / 'docs').resolve()
MKDOCS_YML = ROOT / 'mkdocs.yml'
STATIC = Path(__file__).resolve().parent / 'static'

IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
MAX_UPLOAD = 20 * 1024 * 1024
NAME_RE = re.compile(r'^[\w][\w\-. ]*$')
NAV_ITEM_RE = re.compile(r'^( *)- (.+?)\s*$')


class ApiError(Exception):
    pass


def doc_path(rel):
    p = (DOCS / rel).resolve()
    if DOCS not in p.parents or p.suffix != '.md':
        raise ApiError('docs/ 아래의 .md 파일만 다룰 수 있습니다.')
    return p


def yaml_quote(s):
    return "'" + s.replace("'", "''") + "'"


# ---- mkdocs.yml nav ----
# PyYAML 로 다시 쓰면 주석이 사라지므로, 읽기만 YAML 로 하고 쓰기는 줄 단위로 끼워 넣는다.

def read_nav():
    lines = MKDOCS_YML.read_text(encoding='utf-8').splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.rstrip() == 'nav:')
    except StopIteration:
        raise ApiError('mkdocs.yml 에 nav 가 없습니다.')
    sections, pages, stack = [], set(), []
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if not line.startswith(' '):
            break
        m = NAV_ITEM_RE.match(line)
        if not m:
            continue
        indent = len(m.group(1))
        try:
            item = yaml.safe_load('- ' + m.group(2))[0]
        except yaml.YAMLError:
            continue
        if isinstance(item, dict) and len(item) == 1:
            (label, value), = item.items()
        else:
            label, value = None, item
        while stack and stack[-1]['indent'] >= indent:
            stack.pop()
        for s in stack:
            s['last'] = i
        if stack and stack[-1]['child_indent'] is None:
            stack[-1]['child_indent'] = indent
        if isinstance(value, str):
            pages.add(value)
            if stack:
                stack[-1]['pages'].append(value)
        elif value is None and label is not None:
            sec = {
                'id': i,
                'path': ' > '.join([s['label'] for s in stack] + [str(label)]),
                'label': str(label),
                'indent': indent,
                'child_indent': None,
                'last': i,
                'pages': [],
            }
            sections.append(sec)
            stack.append(sec)
    return lines, sections, pages


def add_to_nav(section_path, label, rel, position, new_section=''):
    lines, sections, _ = read_nav()
    # 줄 번호는 다른 글을 등록할 때마다 밀리므로 메뉴 경로로 찾는다.
    sec = next((s for s in sections if s['path'] == section_path), None)
    if sec is None:
        raise ApiError(f'메뉴를 찾을 수 없습니다: {section_path}')
    indent = sec['child_indent'] or sec['indent'] + 2
    entries = []
    if new_section:
        if any(s['path'] == f"{section_path} > {new_section}" for s in sections):
            raise ApiError(f'"{new_section}" 메뉴가 이미 있습니다. 위 목록에서 고르세요.')
        entries.append(' ' * indent + '- ' + yaml_quote(new_section) + ':')
        indent += 2
    entries.append(' ' * indent + '- ' + yaml_quote(label) + ': ' + yaml_quote(rel))
    at = sec['id'] + 1 if position == 'top' else sec['last'] + 1
    lines[at:at] = entries
    MKDOCS_YML.write_text('\n'.join(lines) + '\n', encoding='utf-8')


# ---- API ----

def api_files(_q, _body):
    _, _, pages = read_nav()
    files = []
    for p in sorted(DOCS.rglob('*.md')):
        rel = p.relative_to(DOCS).as_posix()
        if any(part.startswith('.') for part in p.relative_to(DOCS).parts):
            continue
        files.append({'path': rel, 'in_nav': rel in pages})
    dirs = sorted({''} | {
        d.relative_to(DOCS).as_posix() for d in DOCS.rglob('*')
        if d.is_dir() and 'img' not in d.relative_to(DOCS).parts
        and not any(part.startswith('.') for part in d.relative_to(DOCS).parts)
    })
    return {'files': files, 'dirs': dirs}


def api_nav(_q, _body):
    _, sections, _ = read_nav()
    return {'sections': [{'path': s['path'], 'label': s['label'], 'pages': s['pages']} for s in sections]}


def api_get_doc(q, _body):
    p = doc_path(q.get('path', [''])[0])
    if not p.exists():
        raise ApiError('파일이 없습니다.')
    return {'content': p.read_text(encoding='utf-8')}


def api_save_doc(_q, body):
    p = doc_path(body.get('path', ''))
    if not p.exists():
        raise ApiError('파일이 없습니다. 새 글은 "새 글" 버튼으로 만드세요.')
    p.write_text(body.get('content', ''), encoding='utf-8')
    return {'ok': True}


def api_new_doc(_q, body):
    directory = body.get('dir', '').strip().strip('/')
    filename = body.get('filename', '').strip()
    title = body.get('title', '').strip()
    if not filename.endswith('.md'):
        filename += '.md'
    if not NAME_RE.match(filename):
        raise ApiError('파일 이름에는 글자·숫자·-·_·. 만 쓸 수 있습니다.')
    if directory and not all(NAME_RE.match(part) for part in directory.split('/')):
        raise ApiError('폴더 이름에는 글자·숫자·-·_·. 만 쓸 수 있습니다.')
    rel = f'{directory}/{filename}' if directory else filename
    p = doc_path(rel)
    if p.exists():
        raise ApiError(f'{rel} 이(가) 이미 있습니다.')
    section_path = body.get('section_path', '')
    if section_path:
        # 파일을 만들기 전에 nav 부터 넣어, nav 실패 시 파일만 남는 일이 없게 한다.
        add_to_nav(section_path, body.get('label') or title or p.stem, rel,
                   body.get('position', 'bottom'), body.get('new_section', '').strip())
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f'# {title}\n\n' if title else '', encoding='utf-8')
    return {'path': rel}


def api_upload(q, body_bytes):
    doc = doc_path(q.get('doc', [''])[0])
    ext = q.get('ext', [''])[0].lower()
    if ext not in IMAGE_EXTS:
        raise ApiError(f'지원하지 않는 그림 형식입니다: {ext or "(없음)"}')
    img_dir = doc.parent / 'img' / doc.stem
    img_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
    target = img_dir / f'image-{stamp}.{ext}'
    n = 1
    while target.exists():
        target = img_dir / f'image-{stamp}-{n}.{ext}'
        n += 1
    target.write_bytes(body_bytes)
    return {'src': target.relative_to(doc.parent).as_posix()}


GET_ROUTES = {'/api/files': api_files, '/api/nav': api_nav, '/api/doc': api_get_doc}
POST_ROUTES = {'/api/doc': api_save_doc, '/api/new': api_new_doc}


class Handler(BaseHTTPRequestHandler):
    port = 8001
    preview = 'http://127.0.0.1:8000'

    def _allowed_hosts(self):
        return {f'127.0.0.1:{self.port}', f'localhost:{self.port}'}

    def _check_origin(self):
        # DNS rebinding 과 다른 사이트에서의 요청(CSRF)을 막는다.
        if self.headers.get('Host') not in self._allowed_hosts():
            return False
        origin = self.headers.get('Origin')
        return origin is None or origin in {f'http://{h}' for h in self._allowed_hosts()}

    def _send(self, status, body, ctype='application/json; charset=utf-8'):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def _run(self, fn, *args):
        try:
            self._send(200, fn(*args))
        except ApiError as e:
            self._send(400, {'error': str(e)})

    def do_GET(self):
        if not self._check_origin():
            return self._send(403, {'error': 'forbidden'})
        url = urlparse(self.path)
        if url.path == '/':
            return self._send(200, (STATIC / 'index.html').read_bytes(), 'text/html; charset=utf-8')
        if url.path == '/api/config':
            return self._send(200, {'preview': self.preview})
        if url.path in GET_ROUTES:
            return self._run(GET_ROUTES[url.path], parse_qs(url.query), None)
        self._send(404, {'error': 'not found'})

    def do_POST(self):
        if not self._check_origin():
            return self._send(403, {'error': 'forbidden'})
        url = urlparse(self.path)
        length = int(self.headers.get('Content-Length') or 0)
        if length > MAX_UPLOAD:
            return self._send(413, {'error': '파일이 너무 큽니다 (최대 20MB).'})
        raw = self.rfile.read(length)
        ctype = self.headers.get('Content-Type', '')
        if url.path == '/api/upload' and ctype == 'application/octet-stream':
            return self._run(api_upload, parse_qs(url.query), raw)
        if url.path in POST_ROUTES and ctype.startswith('application/json'):
            return self._run(POST_ROUTES[url.path], None, json.loads(raw or b'{}'))
        self._send(404, {'error': 'not found'})

    def log_message(self, fmt, *args):
        if not self.path.startswith('/api/files'):
            sys.stderr.write('admin: ' + fmt % args + '\n')


def ensure_preview(port):
    try:
        urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=1)
        print(f'미리보기: 이미 실행 중인 mkdocs serve(:{port})를 사용합니다.')
        return
    except Exception:
        pass
    try:
        import mkdocs  # noqa: F401
    except ImportError:
        print('mkdocs 가 없어 미리보기는 꺼집니다. `pip install mkdocs-material` 후 다시 실행하세요.')
        return
    proc = subprocess.Popen(
        [sys.executable, '-m', 'mkdocs', 'serve', '-a', f'127.0.0.1:{port}'], cwd=ROOT)
    atexit.register(proc.terminate)
    print(f'미리보기: mkdocs serve 를 :{port} 에서 시작했습니다.')


def main():
    ap = argparse.ArgumentParser(description='로컬 글쓰기 admin')
    ap.add_argument('--port', type=int, default=8001)
    ap.add_argument('--preview-port', type=int, default=8000)
    args = ap.parse_args()

    # SIGTERM 에도 atexit 가 실행되도록 해, 띄워 둔 mkdocs serve 가 남지 않게 한다.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    Handler.port = args.port
    Handler.preview = f'http://127.0.0.1:{args.preview_port}'
    ensure_preview(args.preview_port)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'admin: http://127.0.0.1:{args.port}/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
