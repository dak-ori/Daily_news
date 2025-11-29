# 🚀 빠른 시작 가이드

## ✅ 현재 상태

- ✅ 프로젝트 코드 완성
- ✅ 가상환경 생성됨
- ✅ `.env` 파일 생성됨
- ✅ Supabase URL, Key 등록됨
- ✅ Google API Key 등록됨
- ✅ 패키지 설치 완료

---

## 📋 다음 단계 (순서대로 진행)

### 1단계: 패키지 설치 완료 확인

```bash
cd /home/dakori/바탕화면/학교활동/2025년/2학기_바이브코딩_보조강사\(40시간\)/daily_news
source venv/bin/activate
pip list | grep supabase  # supabase가 보이면 설치 완료
```

### 2단계: ⚠️ **Supabase 테이블 생성 (매우 중요!)**

1. **Supabase 대시보드 접속**
   - https://supabase.com/dashboard 로 이동
   - 프로젝트 선택: `xeoehbpzgficmuoifyrv`

2. **SQL Editor 열기**
   - 왼쪽 메뉴에서 **SQL Editor** 클릭

3. **테이블 생성 SQL 실행**
   - `src/database/schema.sql` 파일 내용 전체를 복사
   - SQL Editor에 붙여넣기
   - **Run** 버튼 클릭

   또는 아래 명령으로 파일 내용 확인:
   ```bash
   cat src/database/schema.sql
   ```

### 3단계: OpenAI API 키 등록 (AI 분석 사용 시)

`.env` 파일 수정:
```bash
nano .env
```

아래 줄을 수정:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

💡 OpenAI API 키가 없다면:
- https://platform.openai.com/api-keys 에서 발급
- 또는 `.env`에서 `GOOGLE_API_KEY` 사용 (이미 등록되어 있음)

### 4단계: 로컬 테스트 실행

```bash
source venv/bin/activate
python main.py
```

**성공 시 다음과 같이 표시됩니다:**
```
=== Daily Tech Digest 파이프라인 시작 ===
1️⃣ 데이터 수집 시작...
✅ 수집 완료: 저장소 25개, 뉴스 30개
2️⃣ AI 분석 시작...
✅ AI 분석 완료
...
=== 파이프라인 완료 ===
```

**결과물:**
- 콘솔에 예쁘게 출력됨
- `digest_20251129.md` 마크다운 파일 생성
- Supabase 데이터베이스에 데이터 저장됨

### 5단계: (선택) 알림 채널 설정

**Slack 알림:**
```bash
# .env 파일에 추가
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**Discord 알림:**
```bash
# .env 파일에 추가
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
```

### 6단계: (선택) GitHub Actions 자동화

1. **GitHub 저장소 생성**
   ```bash
   git add .
   git commit -m "Initial commit: Daily Tech Digest"
   git remote add origin https://github.com/username/daily_news.git
   git push -u origin main
   ```

2. **GitHub Secrets 등록**
   - GitHub 저장소 > Settings > Secrets and variables > Actions
   - 다음 Secret들 추가:
     - `SUPABASE_URL`: 이미 `.env`에 있음
     - `SUPABASE_KEY`: 이미 `.env`에 있음
     - `GOOGLE_API_KEY`: 이미 `.env`에 있음
     - (선택) `SLACK_WEBHOOK_URL`
     - (선택) `DISCORD_WEBHOOK_URL`

3. **워크플로우 활성화**
   - Actions 탭에서 "Daily Tech Digest" 워크플로우 확인
   - "Run workflow" 버튼으로 수동 실행 가능
   - 매일 오전 9시 자동 실행됨

### 7단계: (선택) 웹 대시보드 배포

1. **Supabase 설정 업데이트**

   `web/app.js` 파일 수정:
   ```javascript
   const SUPABASE_URL = 'https://xeoehbpzgficmuoifyrv.supabase.co';
   const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
   ```

2. **GitHub Pages 활성화**
   - Settings > Pages
   - Source: Deploy from a branch
   - Branch: `main`, Folder: `/web`
   - Save

3. **접속**
   - `https://username.github.io/daily_news/`

---

## 🔍 문제 해결

### 에러: "SUPABASE_URL is not set"
- `.env` 파일이 프로젝트 루트에 있는지 확인
- `cat .env`로 내용 확인

### 에러: "table 'trending_repos' does not exist"
- **2단계: Supabase 테이블 생성**을 완료하지 않았습니다!
- SQL Editor에서 `schema.sql` 실행 필요

### 에러: "Invalid API key"
- OpenAI API 키가 올바른지 확인
- 또는 Google API Key 사용으로 변경

### AI 분석이 작동하지 않음
- `.env`에서 `OPENAI_API_KEY` 또는 `GOOGLE_API_KEY` 확인
- `src/analyzers/tech_analyzer.py`에서 provider 변경 가능

---

## 📊 완료 체크리스트

- [x] 1단계: 패키지 설치 완료
- [ ] 2단계: Supabase 테이블 생성 ⚠️ **매우 중요! (다음 필수 단계)**
- [ ] 3단계: API 키 등록 (Google API Key는 이미 등록됨)
- [ ] 4단계: 로컬 테스트 성공
- [ ] 5단계: (선택) 알림 채널 설정
- [ ] 6단계: (선택) GitHub Actions 설정
- [ ] 7단계: (선택) 웹 대시보드 배포

---

## 💡 팁

- **최소 요구사항**: 2단계, 3단계, 4단계만 완료해도 로컬에서 사용 가능
- **자동화**: 6단계까지 완료하면 매일 자동으로 뉴스 수집
- **공유**: 7단계까지 완료하면 웹에서 누구나 확인 가능

**추가 도움이 필요하면 문서를 확인하세요:**
- [README.md](README.md)
- [docs/SETUP.md](docs/SETUP.md)
- [docs/API.md](docs/API.md)
