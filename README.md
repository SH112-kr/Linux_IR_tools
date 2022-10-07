# BoB10_IR_tools
침해사고 수업 

피드백 : 도커나 virtualbox 고려해보기
문제점 : 파일 경로를 동적으로 불러오는 과정에서 시스템 환경마다 에러가 발생하는 버그 존재. (추후 수정)
명령어 이해 하기 : 옵션 별 출력 내용 이해 - 목적에 맞게 옵션 수행

scan 도구의 대표적 도구들 찾기

새로 생성된 계정

패스워드가 없는 계정

syslog 데몬이 재시작 되는 로그가 남는지

로그파일의 변경일자 확인

find / -user root -perm -4000 -print > suidlist

find / -user root -perm -2000 -print > sgidlist

find / -type f -printf "%P,%A+,%T+,%C+,%u,%g,%M,%s\n”

### 1. 수집

```jsx
fmem + vol.py 메모리 덤프
도커랑 VirtualBox에 관한 정보도 수집

기초 수집
--------------------------------
1. **find / -printf "%T+\t%p\n" | sort**
2. **history**
3. **/etc/group** 
4. **last**
5. **/etc/passwd** 
6. **/etc/shadow**
7. **w (USER, FROM, LOGIN, WHAT) 컬럼**
8-1. **uname -v : Cent-os or Ubuntu**
8-2. **if Cent-os : cat /var/log/secure
	   if Ubuntu : cat /var/log/auth.log**		
9. **service --status-all | grep "+"**
10. **cat /var/log/syslog**

-----------------------------
#네트워크 정보
1. **arp -an**
2. **lsof ( COMMAND, PID, USER, NAME)**
3. **netstat -an**  
4. ifconfig -16.04 버전부터는 기본적으로 없다. sudo apt get install net-tools
5. ip link (맥주소 가져오기) 
-----------------------------
#os 정보
1. **date** 
2. **df -T**
3. **hostname**
4. **uname -a**
-----------------------------
#process 정보
1. **crontab -l**
2. ipcs -u
3. lsmod
4. **ps -auxf** 
5. pstree -a (apt -get install tree 해야함)
------------------------------
# 웹정보 파싱
1. cat /var/log/apache2/access.log
2. cat /var/log/apache2/error.log
3. cat /etc/apache2/sites-available/000-default.conf
------------------------------
# 웹디렉토리 한꺼번에 갖고오기
웹루트 : apache, tomcat, flask, django, wordpress
apache : find / -name "000-default.conf"  #보통 var/www/html 존재
nginx :  /etc/nginx/sites-enabled/default 
flask :
django :

------------------------------
#데 몬
1. /etc/inetd.d
2. /etc/xinetd.d
------------------------------
#apt 설치 리스트
pip list
apt list --installed ( automatic 문자열 제외)

```


### 2. 파싱

```jsx
#삭제 흔적
history, auth.log 등의 로그에서 삭제흔적이 있는지 확인.

/etc/passwd -> UID 0의 값을 가진것이 있는지 검사

arp -> arp 테이블중 중복되는 맥주소가 있는지 등 판단

netstat -an -> 포트 검사를 통해 리버스쉘등의 간단한 검사 진행 + 랜덤포트 검사

df -T -> 마운트안되어있는 정보 extundelete

auth.log | grep "COMMAND" 로 간략화

#의심되는 파일 정보
1. find /{web디렉토리} -name “*.php” | xargs grep “system32” ->php 파일내부에 system32 명령어확인
2. find /{web디렉토리} -name “*.html” -ctime 2 -> web디렉토리에서 2일 안에 변경된 html파일 찾기
3. 기타 웹쉘로 의심되는 확장자 포함 예정
```

### 3. 처리

```jsx
ps -eaf 와 pstree 정보 병합

access.log , error.log - 시그니처 검사 진행 

대용량 로그 ELK 적용시도.

diff 처리결과 - repository 링크를 가지고 있으면 좋지만 자동화하기는 힘들다(버전따는것만)

비정상 URL 요청 분석
- null 바이트 포함되었는지

- 파라미터에 ? 포함되었는지

```

### 4. 보고
