# github에서 이미 push된 파일 제외하기

```bash
git rm -r --cached .
git add .
git commit -m "Apply .gitignore"
git push
```