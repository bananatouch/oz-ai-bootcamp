# 가상환경 없이 파이썬이 없는 환경을 위해 베이스 이미지 설정
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# # 현재 경로의 main.py를 도커 컨테이너 안(이미지)으로 복사
# COPY main.py main.py

# 현재 모든 파일을 도커 컨테이너 안(이미지)으로 복사
COPY . .

# # 이미지 안에 FastAPI 설치 명령어 추가!
# RUN pip install "fastapi[standard]"

# requirements.txt 파일을 이미지 안으로 복사해서 한번에 설치
RUN pip install -r requirements.txt 


# 이미지 내 컨테이너 안에서 실행 명령 (필요한 경우 추가)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["python", "main.py]

# 컨테이너 다시 시작하려면 명령어를
# docker run -p 8000:8000 <이미지 이름>