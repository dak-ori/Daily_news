# Daily Tech Trends & News Service

매일 아침 최신 기술 트렌드와 IT 뉴스를 자동으로 수집하고 분석하여 전달하는 서비스입니다.

## 주요 기능

- **GitHub Trending 수집**: 일간/주간 트렌딩 저장소 자동 수집
- **IT 뉴스 수집**: Hacker News, GeekNews, 요즘IT 등 다양한 소스
- **AI 기술 분석**: LLM을 활용한 기술 설명 및 사용처 추천
- **다채널 알림**: 이메일, Slack, Discord 지원
- **웹 대시보드**: GitHub Pages를 통한 트렌드 시각화

## 기술 스택

- **언어**: Python 3.11+
- **데이터베이스**: Supabase (PostgreSQL)
- **AI/LLM**: OpenAI GPT-4 / Claude / Google Gemini
- **스케줄러**: GitHub Actions
- **프론트엔드**: HTML/CSS/JavaScript (GitHub Pages)

## 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 필요한 API 키를 입력하세요
```

### 4. 실행

```bash
python main.py
```

## 프로젝트 구조

```
daily_news/
├── src/
│   ├── scrapers/        # 데이터 수집 (GitHub, 뉴스)
│   ├── analyzers/       # AI 분석 및 인사이트
│   ├── database/        # Supabase 연동
│   ├── formatters/      # 데이터 포맷팅
│   ├── notifiers/       # 알림 전송
│   └── utils/           # 유틸리티
├── tests/               # 테스트 코드
├── config/              # 설정 파일
├── web/                 # 웹 대시보드
├── docs/                # 문서
└── main.py              # 메인 실행 스크립트
```

## 개발 진행 상황

자세한 Task 목록과 진행 상황은 [TASKS.md](./docs/TASKS.md)를 참조하세요.

## 라이선스

MIT License

## 기여

이슈와 PR을 환영합니다!
