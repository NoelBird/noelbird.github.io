# 한 컴퓨터에서 여러 개의 github 계정을 사용하는 방법

회사를 다니시는 분들은 개인 계정과 회사 계정을 혼합해서 사용하고 계신 분들이 많을 것 같습니다.

제가 찾은 방법은 다음과 같습니다.



1. ssh-keygen 명령어로 개인 키 생성(이 때 comment 로 github에서 사용하는 email 주소가 있어야 함)
2. github에서 계정의 settings -> ssh and gpg -> ssh 공개 키 등록
3. ~/.ssh 폴더에서 config 파일 생성
4. 회사 및 개인 계정에 대해서 다른 hostname 지정
5. 각 local의 git 디렉토리에서 .git 폴더로 진입. remote 부분에서 git@github.com 이 부분을 git@<4번에서 설정한 hostname> 이런 식으로 변경





https://zzpanqing.github.io/2017/02/28/github-push-without-username-and-password.html
https://mygumi.tistory.com/96