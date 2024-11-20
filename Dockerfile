#Python 3.10 slim 버전을 베이스 이미지로 사용
FROM python:3.10-slim

#작업 디렉토리 설정
WORKDIR /app

#필요한 파일 복사
COPY requirements.txt .
COPY . .

#의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

#포트 노출
EXPOSE 8000

#FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]