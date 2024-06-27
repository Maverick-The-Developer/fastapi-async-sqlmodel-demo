# 비동기방식 CRUD 예제 - sqlmodel 패키지 사용
>sqlmodel은 pydantic을 포함하여 DB model(table)을 정의하여 코드를 간결하게 만들 수 있음.

### 가상환경 및 패키지 설치
```bash
python -m venv ./venv
source ./venv/bin/activate # OS 환경에 맞게 activation
pip install -r ./requirements.txt
```
>설치되는 패키지
>- fastapi - framework
>- uvicorn[standard] - 서버실행
>- sqlalchemy[asyncio] - orm, 비동기 기능 추가
>- sqlmodel - 위에 설명
>- aiosqlite - sqlite를 비동기방식으로 연결하기위한 패키지

### 실행
```bash
python main.py
```
>main.py의 최하단 참고