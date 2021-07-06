# fira font



fira font는 아래와 같은 특수 기호들을 적용할 수 있게 해줍니다.

![Fira Code](img/fira-font/logo.svg)



개인적으로 vscode의 기본 폰트가 조금 더 이쁜 것 같긴 한데, 특수 기호들이 예쁜 것 같긴 한데,

특수 기호가 깔끔하게 보이는 게 좋아서 적용했습니다.



링크: https://github.com/tonsky/FiraCode





설치 순서는 OS에 폰트를 먼저 설치한 후, vscode에서

`ctrl + ,`을 눌러서 preference에 들어가서 settings.json에 아래의 코드 두 줄을 적어 놓으면 됩니다.

저는 `"editor.fontLigatures": null`이 있어서 주석처리 했습니다.

```json
"editor.fontFamily": "Fira Code",
"editor.fontLigatures": true,
```

