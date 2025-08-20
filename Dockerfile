FROM python:3.10-slim

# 시스템 패키지 업데이트 및 필수 라이브러리 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리 설정
WORKDIR /app

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 파일들 복사
COPY . .

# Streamlit 포트 설정
EXPOSE 8501

# Streamlit 설정
RUN mkdir -p ~/.streamlit/
RUN echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = 8501\n\
" > ~/.streamlit/config.toml

# 앱 실행
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]