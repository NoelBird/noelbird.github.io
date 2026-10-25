# 로컬 글쓰기 admin

내 컴퓨터에서만 열리는 글 편집기입니다. 배포되는 사이트(`docs/`)에는 포함되지 않습니다.

## 실행

```bash
pip install mkdocs-material   # 처음 한 번
python admin/server.py
```

- 편집기: http://127.0.0.1:8001/
- 미리보기: `mkdocs serve`(:8000)가 꺼져 있으면 함께 띄우고, admin 을 끄면 같이 끕니다.
- 포트 변경: `python admin/server.py --port 8001 --preview-port 8000`

## 기능

- **새 글**: 폴더 · 파일 이름 · 제목을 입력하면 `docs/<폴더>/<파일>.md` 를 만들고 `mkdocs.yml` 의 nav 에 등록합니다.
  - 폴더를 고르면 같은 폴더 글이 있는 메뉴와 순서(맨 위/맨 아래)를 미리 골라 줍니다.
  - `daily` 에 날짜 이름(`2026-11-01`)으로 만들면 해당 달 메뉴(`2026년 11월`)를 고르고, 없으면 새로 만듭니다.
  - `mkdocs.yml` 의 주석과 서식은 그대로 두고 한 줄만 추가합니다.
- **편집**: ⌘S(Ctrl+S) 로 저장하면 오른쪽 미리보기가 자동으로 새로고침됩니다.
- **그림**: 편집기에 붙여넣기 · 끌어다 놓기 · "그림" 버튼. `<글 폴더>/img/<글 이름>/image-<시각>.png` 에 저장하고
  커서 위치에 `![](...)` 를 넣습니다. png · jpg · gif · webp · svg, 20MB 까지.
- 파일 목록의 "메뉴 없음" 표시는 nav 에 등록되지 않아 사이트 메뉴에 안 보이는 글입니다.

## 게시

admin 은 파일만 저장합니다. 사이트에 올리려면 평소처럼 커밋 후 master 에 push 하세요.

```bash
git add docs mkdocs.yml
git commit -m "daily 2026-11-01"
git push
```

## 보안

`127.0.0.1` 에만 열리고, 다른 사이트에서 오는 요청(Host · Origin 이 다른 요청)은 거부합니다.
파일 쓰기는 `docs/` 아래와 `mkdocs.yml` 의 nav 로 제한됩니다.
