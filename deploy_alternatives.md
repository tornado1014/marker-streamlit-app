# 🚀 대안 배포 플랫폼 가이드

## 1. Hugging Face Spaces (무료 + GPU 옵션)

### 장점
- 무료 플랜: 16GB 메모리
- GPU 지원 (유료 $0.05/hour)
- Git 기반 배포
- 큰 AI 모델 지원

### 배포 방법
1. https://huggingface.co 가입
2. Spaces → Create new Space
3. Space type: Streamlit 선택
4. Git으로 코드 푸시

```bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/marker-converter
git push hf main
```

## 2. Railway (유료, 간단함)

### 장점
- $5/month부터
- 8GB 메모리
- GitHub 연동 자동 배포
- 무제한 대역폭

### 배포 방법
1. https://railway.app 가입
2. New Project → Deploy from GitHub
3. 환경변수 설정
4. 자동 배포

## 3. Render (무료 + 유료)

### 무료 플랜
- 512MB 메모리 (여전히 부족)
- 15분 비활성시 sleep

### 유료 플랜
- $7/month부터
- 2GB+ 메모리
- 항상 온라인

## 4. Google Cloud Run

### 장점
- 사용한 만큼 지불
- 최대 32GB 메모리 가능
- 자동 스케일링

### 비용
- CPU: $0.00001667/vCPU초
- 메모리: $0.00000184/GB초

## 5. AWS App Runner

### 장점
- 완전 관리형
- 4GB 메모리까지 지원
- Docker 이미지 지원

## 6. 로컬 + Ngrok (개발/테스트용)

### 무료로 외부 접근 가능
```bash
# 로컬에서 앱 실행
streamlit run app.py

# 다른 터미널에서
ngrok http 8501
```

## 추천 순서

1. **Hugging Face Spaces** (무료 16GB)
2. **Railway** (유료 $5, 사용하기 쉬움)
3. **Streamlit Cloud Teams** (유료 $20, 기존 유지)
4. **Google Cloud Run** (사용량 기반)

## 비용 비교 (월 기준)

| 플랫폼 | 무료 메모리 | 유료 시작가 | 권장 메모리 가격 |
|--------|-------------|-------------|------------------|
| HF Spaces | 16GB | $0.05/hour (GPU) | 무료 |
| Railway | - | $5 (8GB) | $5 |
| Streamlit | 1GB | $20 (4GB) | $20 |
| Render | 512MB | $7 (2GB) | $15 (4GB) |
| GCP Run | - | 사용량 기반 | ~$10-30 |

**결론: Hugging Face Spaces가 가장 경제적입니다.**