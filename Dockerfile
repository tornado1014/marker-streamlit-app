FROM python:3.10-slim

# 시스템 패키지 업데이트 및 필수 라이브러리 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
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

# Streamlit 설정 디렉터리 생성 (권한 문제 해결)
RUN mkdir -p /app/.streamlit
RUN echo "\
[general]\n\
email = \"\"\n\
" > /app/.streamlit/credentials.toml

RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
port = 8501\n\
gatherUsageStats = false\n\
maxUploadSize = 10\n\
" > /app/.streamlit/config.toml

# 환경 변수로 Streamlit 설정 디렉터리 지정
ENV STREAMLIT_CONFIG_DIR /app/.streamlit

# 캐시 디렉터리 설정 및 권한 부여
RUN mkdir -p /app/.cache/huggingface /app/.cache/torch /app/.cache/transformers /app/.cache/datalab
ENV XDG_CACHE_HOME /app/.cache
ENV HUGGINGFACE_HUB_CACHE /app/.cache/huggingface
ENV TORCH_HOME /app/.cache/torch
ENV TRANSFORMERS_CACHE /app/.cache/transformers
ENV HF_HOME /app/.cache/huggingface

# Marker 특화 캐시 경로
ENV MARKER_CACHE_DIR /app/.cache/datalab

# 캐시 디렉터리 권한 설정
RUN chmod -R 777 /app/.cache

# 앱 실행 (사용자 통계 비활성화, CORS 설정)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]