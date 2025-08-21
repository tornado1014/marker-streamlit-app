FROM python:3.10-slim

# 시스템 패키지 설치 (최소한만)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리 설정
WORKDIR /app

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface/transformers
ENV MARKER_CACHE_DIR=/tmp/marker_cache
ENV XDG_CACHE_HOME=/tmp/cache

# 캐시 디렉터리 생성
RUN mkdir -p /tmp/huggingface /tmp/marker_cache /tmp/cache && \
    chmod -R 777 /tmp/huggingface /tmp/marker_cache /tmp/cache

# Python 의존성 설치 (캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 앱 파일들 복사
COPY . .

# Streamlit 설정
RUN mkdir -p /app/.streamlit && \
    echo '[general]\nemail = ""\n' > /app/.streamlit/credentials.toml && \
    echo '[server]\nheadless = true\nenableCORS = false\nenableXsrfProtection = false\nport = 8501\naddress = "0.0.0.0"\ngatherUsageStats = false\nmaxUploadSize = 10\n' > /app/.streamlit/config.toml

ENV STREAMLIT_CONFIG_DIR=/app/.streamlit

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]