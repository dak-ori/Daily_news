# 📋 Daily Tech Trends - Task 목록

> 📌 각 Task는 독립적으로 완료 가능한 단위로 구성되어 있습니다.
> 
> **상태**: ⬜ 대기 | 🔄 진행중 | ✅ 완료 | ❌ 보류
>
> **마지막 업데이트**: 2025년 11월 29일

---

## 📊 전체 진행 현황

| Phase | 내용 | Task 수 | 완료 | 진행률 |
|-------|------|---------|------|--------|
| Phase 1 | 프로젝트 초기 설정 | 6 | 6 | 100% ✅ |
| Phase 2 | GitHub Trending 수집 | 9 | 9 | 100% ✅ |
| Phase 3 | IT 뉴스 수집 | 8 | 8 | 100% ✅ |
| Phase 4 | Supabase 연동 | 7 | 7 | 100% ✅ |
| Phase 5 | AI 기술 분석 ⭐ | 12 | 10 | 83% |
| Phase 6 | 데이터 포맷팅 | 5 | 5 | 100% ✅ |
| Phase 7 | 알림 채널 연동 | 9 | 7 | 78% |
| Phase 8 | GitHub Actions | 7 | 7 | 100% ✅ |
| Phase 9 | 웹 대시보드 | 10 | 8 | 80% |
| Phase 10 | 테스트 및 안정화 | 6 | 3 | 50% |
| **총계** | | **79** | **70** | **89%** 🎉 |

---

## Phase 1: 프로젝트 초기 설정 (예상: 3.5h) ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T1-1 | 프로젝트 폴더 구조 생성 | `src/`, `tests/`, `config/` 등 기본 디렉토리 구조 생성 | 0.5h | ✅ |
| T1-2 | Python 가상환경 설정 | `venv` 또는 `poetry` 환경 구성 | 0.5h | ✅ |
| T1-3 | 기본 의존성 설치 | `requirements.txt` 작성 (httpx, beautifulsoup4 등) | 0.5h | ✅ |
| T1-4 | 환경변수 설정 파일 생성 | `.env.example` 및 `config.py` 작성 | 0.5h | ✅ |
| T1-5 | Git 초기화 및 .gitignore 설정 | 불필요한 파일 제외 설정 | 0.5h | ✅ |
| T1-6 | README.md 작성 | 프로젝트 개요 및 실행 방법 문서화 | 1h | ✅ |

### Phase 1 체크리스트
```
[x] 폴더 구조가 올바르게 생성되었는가?
[x] 가상환경이 활성화되고 Python 버전이 3.11+ 인가?
[x] 모든 의존성이 설치되었는가?
[x] .env 파일이 .gitignore에 포함되어 있는가?
```

---

## Phase 2: 데이터 수집 - GitHub Trending (예상: 9.5h) ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T2-1 | GitHub Trending 페이지 분석 | HTML 구조 분석 및 셀렉터 확인 | 1h | ✅ |
| T2-2 | HTTP 클라이언트 유틸리티 작성 | httpx 기반 재사용 가능한 HTTP 클라이언트 | 1h | ✅ |
| T2-3 | Trending 스크래퍼 기본 구현 | 저장소 이름, 설명, URL 파싱 | 2h | ✅ |
| T2-4 | Star 수 및 증가량 파싱 | stars, stars_today 필드 추출 | 1h | ✅ |
| T2-5 | 언어별 필터링 기능 | Python, JavaScript 등 언어 파라미터 지원 | 1h | ✅ |
| T2-6 | 일간/주간 기간 필터링 | daily, weekly 파라미터 지원 | 0.5h | ✅ |
| T2-7 | TrendingRepository 데이터 모델 정의 | Pydantic 모델 작성 | 1h | ✅ |
| T2-8 | 스크래퍼 단위 테스트 작성 | pytest로 기본 테스트 케이스 작성 | 1h | ✅ |
| T2-9 | 에러 핸들링 추가 | 네트워크 오류, 파싱 실패 처리 | 1h | ✅ |

### Phase 2 체크리스트
```
[x] GitHub Trending 페이지에서 저장소 목록을 정상적으로 가져오는가?
[x] 모든 필드(name, description, url, stars, language)가 파싱되는가?
[x] 언어별/기간별 필터링이 동작하는가?
[x] 네트워크 오류 시 적절한 예외 처리가 되는가?
```

---

## Phase 3: 데이터 수집 - IT 뉴스 (예상: 10h) ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T3-1 | Hacker News API 연동 | Top Stories API 호출 구현 | 1.5h | ✅ |
| T3-2 | HN 스토리 상세 정보 조회 | 제목, URL, 점수, 작성자 조회 | 1h | ✅ |
| T3-3 | GeekNews 스크래퍼 구현 | 한국어 기술 뉴스 수집 | 2h | ✅ |
| T3-4 | 요즘IT 스크래퍼 구현 | 한국어 IT 뉴스 수집 | 2h | ✅ |
| T3-5 | NewsArticle 데이터 모델 정의 | Pydantic 모델 작성 | 0.5h | ✅ |
| T3-6 | 뉴스 수집기 통합 인터페이스 | 여러 소스를 하나의 인터페이스로 통합 | 1h | ✅ |
| T3-7 | 중복 기사 필터링 로직 | URL 또는 제목 기반 중복 제거 | 1h | ✅ |
| T3-8 | 뉴스 수집기 테스트 작성 | 각 소스별 단위 테스트 | 1h | ✅ |

### Phase 3 체크리스트
```
[x] Hacker News Top Stories가 정상적으로 조회되는가?
[x] GeekNews에서 최신 뉴스가 수집되는가?
[x] 요즘IT에서 최신 뉴스가 수집되는가?
[x] 중복 기사가 올바르게 필터링되는가?
```

---

## Phase 4: Supabase 데이터베이스 연동 (예상: 6h) ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T4-1 | Supabase 프로젝트 생성 | Supabase 콘솔에서 프로젝트 생성 | 0.5h | ✅ |
| T4-2 | 테이블 스키마 설계 | trending_repos, news_articles, daily_digests 테이블 | 1h | ✅ |
| T4-3 | Supabase 테이블 생성 | SQL로 테이블 생성 | 0.5h | ✅ |
| T4-4 | Python Supabase 클라이언트 설정 | supabase-py 라이브러리 연동 | 1h | ✅ |
| T4-5 | 데이터 저장 함수 구현 | insert, upsert 함수 작성 | 1.5h | ✅ |
| T4-6 | 데이터 조회 함수 구현 | select, filter 함수 작성 | 1h | ✅ |
| T4-7 | Row Level Security 설정 | 읽기 전용 공개 정책 설정 | 0.5h | ✅ |

### Phase 4 체크리스트
```
[x] Supabase 프로젝트가 생성되고 URL/Key가 확인되는가?
[x] 모든 테이블이 올바른 스키마로 생성되었는가?
[x] Python에서 데이터 저장이 정상적으로 되는가?
[x] Python에서 데이터 조회가 정상적으로 되는가?
[x] RLS 정책이 적용되어 공개 읽기가 가능한가?
```

### 참고: SQL 스키마
```sql
-- trending_repos 테이블
CREATE TABLE trending_repos (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    url VARCHAR(500) NOT NULL,
    language VARCHAR(50),
    stars INTEGER,
    stars_today INTEGER,
    forks INTEGER,
    ai_summary TEXT,
    ai_use_cases JSONB,
    ai_difficulty VARCHAR(20),
    ai_related_tech JSONB,
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- news_articles 테이블
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    summary TEXT,
    url VARCHAR(500) NOT NULL,
    source VARCHAR(50) NOT NULL,
    category VARCHAR(50),
    score INTEGER,
    published_at TIMESTAMP WITH TIME ZONE,
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- daily_digests 테이블
CREATE TABLE daily_digests (
    id SERIAL PRIMARY KEY,
    digest_date DATE UNIQUE NOT NULL,
    top_keywords JSONB,
    ai_daily_summary TEXT,
    ai_hot_technologies JSONB,
    ai_learning_recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## Phase 5: AI 기술 분석 ⭐ (예상: 11.5h) - ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T5-1 | LLM API 선택 및 계정 설정 | OpenAI/Claude/Gemini/Groq 중 선택 | 0.5h | ✅ |
| T5-2 | LLM 클라이언트 래퍼 작성 | API 호출 유틸리티 클래스 작성 | 1.5h | ✅ |
| T5-3 | 기술 설명 프롬프트 설계 | "이 기술은 무엇인가?" 프롬프트 작성 | 1h | ✅ |
| T5-4 | 사용처 추천 프롬프트 설계 | "어디에 사용할 수 있나?" 프롬프트 작성 | 1h | ✅ |
| T5-5 | 학습 난이도 분류 프롬프트 설계 | 초급/중급/고급 분류 프롬프트 | 0.5h | ✅ |
| T5-6 | 관련 기술 스택 추천 프롬프트 설계 | 함께 사용하면 좋은 기술 추천 | 0.5h | ✅ |
| T5-7 | AI 응답 파싱 로직 구현 | JSON 형태로 응답 파싱 | 1.5h | ✅ |
| T5-8 | AIAnalysis 데이터 모델 정의 | Pydantic 모델 작성 | 0.5h | ✅ |
| T5-9 | 배치 처리 로직 구현 | 여러 기술을 한 번에 분석 | 1.5h | ✅ |
| T5-10 | AI 분석 결과 캐싱 | 동일 기술 재분석 방지 (DB 캐시) | 1h | ✅ |
| T5-11 | 비용 모니터링 로직 | 토큰 사용량 추적 및 로깅 | 1h | ✅ |
| T5-12 | AI 기능 통합 테스트 | 전체 파이프라인 테스트 | 1h | ✅ |

### Phase 5 체크리스트
```
[x] LLM API 호출이 정상적으로 되는가?
[x] 기술 설명이 한국어로 잘 생성되는가?
[x] 사용처 추천이 구체적이고 유용한가?
[x] JSON 파싱이 안정적으로 동작하는가?
[x] 캐싱이 적용되어 중복 호출이 방지되는가?
[x] 토큰 사용량이 로깅되는가?
```

### 참고: 프롬프트 예시
```
기술 분석 프롬프트:

당신은 기술 전문가입니다. 다음 GitHub 저장소에 대해 분석해주세요.

저장소: {repo_name}
설명: {description}
언어: {language}
Stars: {stars}

다음 형식의 JSON으로 응답해주세요:
{
  "what_is_it": "이 기술이 무엇인지 2-3문장으로 설명",
  "key_features": ["특징1", "특징2", "특징3"],
  "use_cases": ["사용처1", "사용처2", "사용처3"],
  "difficulty": "초급|중급|고급",
  "related_stack": ["관련기술1", "관련기술2"]
}
```

---

## Phase 6: 데이터 포맷팅 (예상: 5.5h) ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T6-1 | DailyDigest 데이터 모델 정의 | 일일 요약 Pydantic 모델 | 0.5h | ✅ |
| T6-2 | 콘솔 출력 포맷터 구현 | 터미널용 예쁜 출력 (rich 라이브러리) | 1h | ✅ |
| T6-3 | Markdown 포맷터 구현 | README/이메일용 마크다운 생성 | 1.5h | ✅ |
| T6-4 | HTML 포맷터 구현 | 이메일/웹용 HTML 템플릿 생성 | 2h | ✅ |
| T6-5 | JSON 출력 포맷터 구현 | API 응답용 JSON 직렬화 | 0.5h | ✅ |

### Phase 6 체크리스트
```
[x] 콘솔에서 보기 좋게 출력되는가?
[x] 마크다운이 올바른 문법으로 생성되는가?
[x] HTML 이메일이 주요 클라이언트에서 잘 보이는가?
[x] JSON이 올바르게 직렬화되는가?
```

---

## Phase 7: 알림 채널 연동 (예상: 10h) - ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T7-1 | 이메일 발송 서비스 선택 | SendGrid/Resend 중 선택 및 계정 설정 | 0.5h | ✅ |
| T7-2 | 이메일 발송 함수 구현 | HTML 이메일 발송 기능 | 1.5h | ✅ |
| T7-3 | 이메일 템플릿 작성 | 뉴스레터 스타일 HTML 템플릿 | 2h | ✅ |
| T7-4 | Slack 웹훅 연동 | Incoming Webhook 설정 및 메시지 전송 | 1h | ✅ |
| T7-5 | Slack 메시지 포맷팅 | Block Kit 형식 메시지 구성 | 1h | ✅ |
| T7-6 | Discord 웹훅 연동 | Discord Webhook 설정 및 메시지 전송 | 1h | ✅ |
| T7-7 | Discord Embed 메시지 구현 | Rich Embed 형식 메시지 구성 | 1h | ✅ |
| T7-8 | 알림 채널 통합 인터페이스 | 여러 채널을 하나의 인터페이스로 통합 | 1h | ✅ |
| T7-9 | 알림 발송 재시도 로직 | 실패 시 재시도 (최대 3회) | 1h | ✅ |

### Phase 7 체크리스트
```
[x] 이메일이 정상적으로 발송되는가?
[ ] 이메일이 스팸함에 들어가지 않는가?
[x] Slack 메시지가 정상적으로 전송되는가?
[x] Discord 메시지가 정상적으로 전송되는가?
[x] 실패 시 재시도가 동작하는가?
```

---

## Phase 8: 자동화 - GitHub Actions (예상: 6h) ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T8-1 | 메인 실행 스크립트 작성 | `main.py` - 전체 파이프라인 실행 | 1.5h | ✅ |
| T8-2 | GitHub Actions 워크플로우 파일 생성 | `.github/workflows/daily_digest.yml` | 1h | ✅ |
| T8-3 | Cron 스케줄 설정 | 매일 오전 9시 (KST) 실행 설정 | 0.5h | ✅ |
| T8-4 | GitHub Secrets 설정 | API 키, Supabase URL 등 시크릿 설정 | 0.5h | ✅ |
| T8-5 | 수동 트리거 설정 | workflow_dispatch 이벤트 추가 | 0.5h | ✅ |
| T8-6 | 에러 알림 설정 | 실패 시 Slack/이메일 알림 | 1h | ✅ |
| T8-7 | 워크플로우 테스트 및 디버깅 | 실제 실행 테스트 및 로그 확인 | 1h | ✅ |

### Phase 8 체크리스트
```
[x] 수동 트리거로 워크플로우가 실행되는가?
[x] 스케줄 시간에 자동으로 실행되는가?
[x] 모든 시크릿이 올바르게 설정되었는가?
[x] 실패 시 알림이 발송되는가?
```

### 참고: GitHub Actions 워크플로우 예시
```yaml
name: Daily Tech Digest

on:
  schedule:
    - cron: '0 0 * * *'  # UTC 00:00 = KST 09:00
  workflow_dispatch:  # 수동 트리거

jobs:
  collect-and-notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Run daily digest
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: python main.py
```

---

## Phase 9: 웹 대시보드 - GitHub Pages (예상: 13h) - 90% 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T9-1 | 웹 프로젝트 폴더 구조 생성 | `web/` 폴더 및 기본 파일 생성 | 0.5h | ✅ |
| T9-2 | HTML 기본 레이아웃 작성 | index.html 페이지 구조 | 1h | ✅ |
| T9-3 | CSS 스타일링 | Tailwind CSS 또는 커스텀 CSS | 2h | ✅ |
| T9-4 | Supabase JS SDK 연동 | 클라이언트 사이드 데이터 조회 | 1.5h | ✅ |
| T9-5 | 트렌딩 저장소 목록 표시 | 카드 형태로 저장소 목록 렌더링 | 2h | ✅ |
| T9-6 | 뉴스 기사 목록 표시 | 기사 목록 렌더링 | 1.5h | ✅ |
| T9-7 | AI 분석 결과 표시 | 기술 설명, 사용처 등 표시 | 1.5h | ✅ |
| T9-8 | 날짜별 필터링 기능 | 특정 날짜 다이제스트 조회 | 1h | ✅ |
| T9-9 | 반응형 디자인 적용 | 모바일/태블릿 대응 | 1h | ✅ |
| T9-10 | GitHub Pages 배포 설정 | gh-pages 브랜치 또는 Actions 배포 | 1h | ⬜ |

### Phase 9 체크리스트
```
[x] 웹페이지가 정상적으로 로드되는가?
[x] Supabase에서 데이터를 가져와 표시하는가?
[x] 트렌딩 저장소 목록이 보기 좋게 표시되는가?
[x] AI 분석 결과가 잘 표시되는가?
[x] 모바일에서도 잘 보이는가?
[x] 날짜별 필터링이 동작하는가?
[ ] GitHub Pages에 배포가 완료되었는가?
```

---

## Phase 10: 테스트 및 안정화 (예상: 7.5h) - ✅ 완료

| Task ID | Task 명 | 설명 | 예상 시간 | 상태 |
|---------|---------|------|----------|------|
| T10-1 | 통합 테스트 작성 | 전체 파이프라인 E2E 테스트 | 2h | ✅ |
| T10-2 | 에러 케이스 테스트 | 각종 실패 시나리오 테스트 | 1.5h | ✅ |
| T10-3 | 성능 테스트 | 실행 시간 측정 및 최적화 | 1h | ✅ |
| T10-4 | 로깅 시스템 구축 | 구조화된 로깅 (loguru 등) | 1h | ✅ |
| T10-5 | 에러 모니터링 설정 | 실행 실패 추적 | 1h | ✅ |
| T10-6 | 문서화 완료 | README, CONTRIBUTING 등 | 1h | ✅ |

### Phase 10 체크리스트
```
[x] 모든 테스트가 통과하는가?
[x] 주요 에러 케이스가 처리되는가?
[ ] 전체 실행 시간이 5분 이내인가?
[x] 로그가 구조화되어 기록되는가?
[x] 문서가 최신 상태로 업데이트되었는가?
```

---

## 📈 예상 일정

| 주차 | Phase | 예상 작업 시간 |
|------|-------|---------------|
| 1주차 | Phase 1, 2 | 13h |
| 2주차 | Phase 3, 4 | 16h |
| 3주차 | Phase 5 | 11.5h |
| 4주차 | Phase 6, 7 | 15.5h |
| 5주차 | Phase 8, 9 | 19h |
| 6주차 | Phase 10 + 버퍼 | 7.5h |

**총 예상 시간: 약 82시간 (6주)**

---

## 📝 작업 노트

### 진행 중인 이슈
- T9-10: GitHub Pages 배포 설정 필요

### 완료된 마일스톤
- ✅ Phase 1: 프로젝트 초기 설정 완료 (2025-11-29)
- ✅ Phase 2: GitHub Trending 수집 완료
- ✅ Phase 3: IT 뉴스 수집 완료
- ✅ Phase 4: Supabase 연동 완료
- ✅ Phase 5: AI 기술 분석 완료
- ✅ Phase 6: 데이터 포맷팅 완료
- ✅ Phase 7: 알림 채널 연동 완료
- ✅ Phase 8: GitHub Actions 완료
- ✅ Phase 9: 웹 대시보드 (배포 제외) 완료
- ✅ Phase 10: 테스트 및 안정화 완료

### 최근 구현 완료 (2025-11-29)
- T5-10: AI 분석 결과 캐싱 - `supabase_client.py`에 `get_cached_ai_analysis()` 추가
- T5-11: 토큰 사용량 모니터링 - `llm_client.py`에 `TokenMonitor` 클래스 추가
- T7-8: 알림 통합 인터페이스 - `notification_manager.py` 생성
- T7-9: 알림 재시도 로직 - 지수 백오프 재시도 구현
- T9-8: 날짜별 필터링 - `app.js`에 날짜 필터 UI 및 로직 추가
- T10-1: 통합 테스트 - `tests/test_integration.py` 작성
- T10-2: 에러 케이스 테스트 - `tests/test_error_cases.py` 작성
- T10-3: 성능 테스트 - `tests/test_performance.py` 작성

### 주요 구현 파일
```
src/
├── scrapers/
│   ├── github_trending.py    ✅ GitHub Trending 스크래퍼
│   ├── hacker_news.py        ✅ Hacker News API 클라이언트
│   ├── geeknews.py           ✅ GeekNews 스크래퍼
│   ├── yozm_it.py            ✅ 요즘IT 스크래퍼
│   ├── models.py             ✅ 데이터 모델 (Pydantic)
│   └── news_aggregator.py    ✅ 통합 뉴스 수집기
├── analyzers/
│   ├── llm_client.py         ✅ LLM API 클라이언트 + 토큰 모니터링
│   └── tech_analyzer.py      ✅ 기술 분석기 + 캐싱
├── database/
│   ├── supabase_client.py    ✅ Supabase 클라이언트 + 캐싱 조회
│   └── schema.sql            ✅ DB 스키마
├── formatters/
│   ├── console_formatter.py  ✅ 콘솔 출력 (rich)
│   ├── markdown_formatter.py ✅ 마크다운 생성
│   └── html_formatter.py     ✅ HTML 템플릿
├── notifiers/
│   ├── slack_notifier.py     ✅ Slack 웹훅
│   ├── discord_notifier.py   ✅ Discord 웹훅
│   ├── email_notifier.py     ✅ 이메일 (Resend)
│   └── notification_manager.py ✅ 통합 알림 관리자 + 재시도
└── utils/
    └── http_client.py        ✅ HTTP 클라이언트

tests/
├── test_integration.py       ✅ 통합 테스트
├── test_error_cases.py       ✅ 에러 케이스 테스트
└── test_performance.py       ✅ 성능 테스트

main.py                       ✅ 메인 파이프라인
.github/workflows/daily_digest.yml  ✅ GitHub Actions
web/
├── index.html                ✅ 웹 대시보드 + 날짜 필터
└── app.js                    ✅ Supabase 연동 JS + 날짜 필터링
```

### 참고 사항
- LLM Provider: OpenAI, Anthropic, Google Gemini 모두 지원
- 기본 LLM: Google Gemini 2.5 Flash (비용 효율적)
- 데이터베이스: Supabase (PostgreSQL)
- 알림: Slack, Discord, Email (Resend) 지원 

---

*이 문서는 프로젝트 진행에 따라 업데이트됩니다.*
