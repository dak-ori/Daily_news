# 설치 및 설정 가이드

## 1. 사전 요구사항

- Python 3.11 이상
- Git
- Supabase 계정
- LLM API 키 (OpenAI, Anthropic, 또는 Google 중 하나)

## 2. 프로젝트 클론

```bash
git clone https://github.com/your-username/daily_news.git
cd daily_news
```

## 3. 가상환경 설정

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

## 4. 의존성 설치

```bash
pip install -r requirements.txt
```

## 5. Supabase 설정

### 5.1 Supabase 프로젝트 생성

1. [Supabase](https://supabase.com/)에 가입하고 새 프로젝트 생성
2. Project URL과 Anon Key를 복사

### 5.2 데이터베이스 스키마 생성

1. Supabase 대시보드의 **SQL Editor**로 이동
2. `src/database/schema.sql` 파일의 내용을 복사하여 실행

## 6. 환경변수 설정

### 6.1 .env 파일 생성

```bash
cp .env.example .env
```

### 6.2 API 키 설정

`.env` 파일을 열고 다음 항목들을 설정:

```env
# 필수: Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# 필수: LLM (하나 이상 선택)
OPENAI_API_KEY=your_openai_api_key
# ANTHROPIC_API_KEY=your_anthropic_api_key
# GOOGLE_API_KEY=your_google_api_key

# 선택: 알림 채널
SLACK_WEBHOOK_URL=your_slack_webhook_url
DISCORD_WEBHOOK_URL=your_discord_webhook_url

# 선택: 이메일
RESEND_API_KEY=your_resend_api_key
EMAIL_FROM=noreply@yourdomain.com
EMAIL_TO=your@email.com
```

### 6.3 API 키 발급 방법

#### OpenAI API Key
1. [OpenAI Platform](https://platform.openai.com/)에 가입
2. **API Keys** 메뉴에서 새 키 생성

#### Slack Webhook URL
1. Slack 워크스페이스에서 **Apps** > **Incoming Webhooks** 검색
2. 채널 선택 후 Webhook URL 복사

#### Discord Webhook URL
1. Discord 서버 설정 > **연동** > **웹후크**
2. 새 웹후크 생성 후 URL 복사

## 7. 로컬 실행

```bash
python main.py
```

성공적으로 실행되면:
- GitHub Trending 저장소 수집
- IT 뉴스 수집
- AI 분석 수행
- Supabase에 데이터 저장
- 콘솔에 결과 출력
- 마크다운 파일 생성 (`digest_YYYYMMDD.md`)

## 8. GitHub Actions 설정

### 8.1 GitHub Secrets 설정

GitHub 저장소의 **Settings** > **Secrets and variables** > **Actions**에서:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OPENAI_API_KEY`
- `SLACK_WEBHOOK_URL` (선택)
- `DISCORD_WEBHOOK_URL` (선택)
- `RESEND_API_KEY` (선택)
- `EMAIL_FROM` (선택)
- `EMAIL_TO` (선택)

### 8.2 워크플로우 활성화

1. GitHub 저장소의 **Actions** 탭으로 이동
2. **Daily Tech Digest** 워크플로우 활성화
3. **Run workflow** 버튼으로 수동 실행 가능

## 9. 웹 대시보드 배포

### 9.1 Supabase 설정 업데이트

`web/app.js` 파일에서:

```javascript
const SUPABASE_URL = 'your_supabase_url';
const SUPABASE_ANON_KEY = 'your_supabase_anon_key';
```

### 9.2 GitHub Pages 활성화

1. GitHub 저장소의 **Settings** > **Pages**로 이동
2. **Source**: Deploy from a branch
3. **Branch**: `main` / Folder: `/web`
4. **Save** 클릭

### 9.3 접속

`https://your-username.github.io/daily_news/`

## 10. 테스트 실행

```bash
pytest tests/ -v
```

## 문제 해결

### 에러: "SUPABASE_URL is not set"

- `.env` 파일이 프로젝트 루트에 있는지 확인
- `.env` 파일에 `SUPABASE_URL`이 올바르게 설정되었는지 확인

### 에러: "HTTP request failed"

- 인터넷 연결 확인
- GitHub/Supabase가 정상 작동 중인지 확인

### AI 분석이 작동하지 않음

- LLM API 키가 올바르게 설정되었는지 확인
- API 사용량 제한을 초과하지 않았는지 확인

## 추가 정보

자세한 내용은 다음 문서를 참조하세요:
- [README.md](../README.md)
- [TASKS.md](./TASKS.md)
- [PRD.md](./PRD.md)
