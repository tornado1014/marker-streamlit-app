FROM python:3.10-slim

# 시스템 패키지 업데이트 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 환경 변수 설정 - Hugging Face Spaces 권한 문제 해결
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface/transformers
ENV HF_DATASETS_CACHE=/tmp/huggingface/datasets
ENV MARKER_CACHE_DIR=/tmp/marker_cache
ENV XDG_CACHE_HOME=/tmp/cache
ENV PYTHONPATH=/app

# 캐시 디렉토리 생성 및 권한 설정
RUN mkdir -p /tmp/huggingface /tmp/marker_cache /tmp/cache /tmp/huggingface/transformers /tmp/huggingface/datasets
RUN chmod -R 777 /tmp/huggingface /tmp/marker_cache /tmp/cache

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 설정
EXPOSE 7860

# Streamlit 설정
RUN mkdir -p ~/.streamlit
RUN echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml
RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = 7860\n\
address = \"0.0.0.0\"\n\
" > ~/.streamlit/config.toml

# 앱 실행
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]