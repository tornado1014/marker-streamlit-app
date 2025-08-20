# 🚀 배포 가이드

## GitHub Repository 생성 및 코드 푸시

### 1단계: GitHub에서 새 Repository 생성
1. https://github.com 접속 후 로그인
2. 우상단 "+" → "New repository" 클릭
3. Repository 정보 입력:
   - **Repository name**: `marker-streamlit-app`
   - **Description**: `PDF to Markdown converter using Marker and Streamlit`
   - **Visibility**: Public 선택
   - README, .gitignore, license는 **선택하지 않음** (이미 있음)
4. "Create repository" 클릭

### 2단계: 코드 푸시
Repository 생성 후 다음 명령어 실행:

```bash
cd /e/marker-streamlit-app
git branch -M main
git remote add origin https://github.com/tornado1014@gmail.com/marker-streamlit-app.git
git push -u origin main
```

**참고**: 비밀번호 대신 Personal Access Token 사용 권장

### 3단계: Personal Access Token 생성 (권장)
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token (classic)" 클릭
3. Scopes: `repo` 선택
4. 생성된 토큰을 복사

### 4단계: Token으로 푸시
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/tornado1014@gmail.com/marker-streamlit-app.git
git push -u origin main
```

## Streamlit Community Cloud 배포

### 1단계: Streamlit 계정 생성/로그인
1. https://share.streamlit.io 접속
2. "Sign up with GitHub" 클릭
3. GitHub 계정으로 인증

### 2단계: 앱 배포
1. "New app" 버튼 클릭
2. 배포 설정:
   - **Repository**: `tornado1014@gmail.com/marker-streamlit-app`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. "Deploy!" 클릭

### 3단계: 배포 완료 대기
- 첫 배포는 dependencies 설치로 5-10분 소요
- 배포 로그에서 진행 상황 확인 가능
- 완료되면 고유 URL 제공

## 환경 변수 설정 (선택사항)

LLM 기능을 사용하려면 Streamlit Cloud에서 환경 변수 설정:
1. App dashboard → Settings → Secrets
2. 다음 내용 추가:
```
GEMINI_API_KEY = "your_api_key_here"
```

## 배포 후 확인사항

✅ 앱이 정상적으로 로드되는지 확인
✅ 파일 업로드가 작동하는지 테스트
✅ 변환 기능이 정상 작동하는지 확인

## 문제 해결

### 배포 실패시
1. Streamlit Cloud 로그 확인
2. requirements.txt 의존성 문제 확인
3. 메모리 사용량 확인 (Community Cloud 제한)

### 성능 개선
- 대용량 파일 처리 제한 추가
- 모델 로딩 최적화
- 캐싱 활용

---
🎉 배포 성공시 URL을 공유해주세요!