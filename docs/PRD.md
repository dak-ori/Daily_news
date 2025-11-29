# PRD: Daily Tech Trends & News Service

## 📋 문서 정보
- **문서명**: Daily Tech Trends & News Service PRD
- **버전**: 1.0
- **작성일**: 2025년 11월 29일
- **작성자**: 개발팀

---

## 1. 개요 (Overview)

### 1.1 프로젝트 배경
기술 트렌드는 빠르게 변화하고 있으며, 개발자와 IT 관련 종사자들이 최신 기술 동향을 파악하는 것은 매우 중요합니다. 그러나 여러 소스를 매일 확인하는 것은 시간이 많이 소요됩니다. 이 서비스는 GitHub Trending과 IT 뉴스를 자동으로 수집하여 사용자에게 매일 아침 요약된 정보를 제공합니다.

### 1.2 프로젝트 목표
- **자동화**: 매일 오전 9시에 자동으로 최신 기술 트렌드 정보 수집
- **통합**: GitHub Trending 저장소와 IT 뉴스를 한 곳에서 확인
- **인사이트 제공**: 어떤 기술이 부상하고 있는지 분석하여 제공
- **접근성**: 다양한 채널(이메일, Slack, Discord 등)을 통한 알림 지원

---

## 2. 타겟 사용자 (Target Users)

### 2.1 주요 사용자
| 사용자 유형 | 설명 | 니즈 |
|------------|------|------|
| 개발자 | 최신 기술 트렌드를 파악하고 싶은 개발자 | 새로운 라이브러리, 프레임워크 정보 |
| 기술 리더 | 팀의 기술 스택 결정에 참고가 필요한 리더 | 산업 동향, 기술 채택 트렌드 |
| IT 종사자 | 기술 분야 전반에 관심 있는 종사자 | IT 뉴스, 업계 동향 |
| 학생/취준생 | 기술 트렌드를 학습하고 싶은 학생 | 인기 기술, 학습 방향 |

---

## 3. 핵심 기능 (Core Features)

### 3.1 데이터 수집 기능

#### 3.1.1 GitHub Trending 수집
- **일간/주간 Trending 저장소** 수집
- **프로그래밍 언어별** 필터링 (Python, JavaScript, Go 등)
- 수집 정보:
  - 저장소 이름 및 설명
  - Star 수 및 증가량
  - 주요 사용 언어
  - 저장소 URL

#### 3.1.2 IT 뉴스 수집
- **뉴스 소스**:
  - Hacker News (Top Stories)
  - TechCrunch
  - The Verge (Tech)
  - Dev.to
  - Reddit (r/programming, r/technology)
  - GeekNews (한국어)
  - 요즘IT (한국어)
- 수집 정보:
  - 기사 제목 및 요약
  - 원문 URL
  - 발행일
  - 카테고리/태그

### 3.2 AI 기반 분석 및 인사이트 기능

#### 3.2.1 트렌드 분석
- **키워드 추출**: 자주 언급되는 기술 키워드 분석
- **카테고리 분류**: AI/ML, Web, Mobile, DevOps 등 분야별 분류
- **트렌드 점수**: 각 기술의 인기도 점수 산출

#### 3.2.2 🤖 AI 기술 설명 생성 (신규)
- **기술 개요 설명**: 해당 기술/라이브러리가 무엇인지 쉽게 설명
  - 예: "Rust는 메모리 안전성을 보장하는 시스템 프로그래밍 언어입니다."
- **핵심 특징 요약**: 해당 기술의 주요 장점 3~5가지
- **기존 기술과 비교**: 유사한 기술과의 차이점 설명
  - 예: "Bun vs Node.js: 더 빠른 JavaScript 런타임"

#### 3.2.3 🎯 AI 사용처 추천 (신규)
- **실무 활용 사례**: 이 기술을 어디에 사용할 수 있는지 구체적 예시 제공
  - 예: "FastAPI → REST API 서버, 마이크로서비스, ML 모델 서빙"
- **추천 프로젝트 유형**: 개인 프로젝트, 스타트업, 대기업 등 적합한 규모 제안
- **학습 난이도 표시**: 초급/중급/고급으로 학습 진입 장벽 안내
- **관련 기술 스택 추천**: 함께 사용하면 좋은 기술 조합
  - 예: "Next.js + Supabase + Vercel"

#### 3.2.4 요약 생성
- AI 기반 뉴스 요약 생성
- 주요 포인트 하이라이트
- 한국어 번역 지원

### 3.3 알림 및 배포 기능

#### 3.3.1 알림 채널
| 채널 | 우선순위 | 설명 |
|------|---------|------|
| 이메일 | P0 | 구독자에게 뉴스레터 형태로 발송 |
| Slack | P1 | Slack 워크스페이스에 메시지 전송 |
| Discord | P1 | Discord 채널에 메시지 전송 |
| 웹 대시보드 | P2 | 웹에서 트렌드 확인 가능 |
| RSS 피드 | P2 | RSS 구독 지원 |

#### 3.3.2 스케줄링
- **기본 스케줄**: 매일 오전 9시 (KST)
- **사용자 정의 스케줄** 지원 (선택적)
- **수동 트리거** 기능

---

## 4. 기술 스택 (Tech Stack)

### 4.1 백엔드
```
- 언어: Python 3.11+
- 프레임워크: FastAPI (API 서버) 또는 순수 스크립트
- 스케줄러: GitHub Actions (Cron)
- 데이터베이스: Supabase (PostgreSQL + 실시간 기능 + Auth)
```

### 4.2 데이터 수집
```
- HTTP 클라이언트: httpx, aiohttp
- 웹 스크래핑: BeautifulSoup4, Selectolax
- API 클라이언트: GitHub API, News API
```

### 4.3 AI/LLM
```
- LLM API: OpenAI GPT-4o / Claude API / Google Gemini
- 대안 (무료/저비용):
  - Groq (무료 티어, 빠른 응답)
  - Together AI
  - Ollama (로컬 실행, GitHub Actions에서는 제한적)
- SDK: openai, anthropic, google-generativeai
```

### 4.4 알림/배포
```
- 이메일: SendGrid, AWS SES, Resend
- Slack: Slack SDK (slack_sdk)
- Discord: discord.py, Webhook
```

### 4.5 인프라
```
- 스케줄링 & 백엔드: GitHub Actions (무료, 스케줄 기반)
  - 매일 오전 9시 데이터 수집 및 Supabase 저장
  - Python 스크립트 실행
- 프론트엔드 호스팅: GitHub Pages (github.io)
  - 정적 웹사이트로 대시보드 제공
  - Supabase JS SDK로 데이터 조회
- 데이터베이스: Supabase (무료 티어 사용 가능)
```

> ⚠️ **참고**: GitHub Pages는 정적 사이트만 호스팅 가능합니다.
> - ✅ 가능: HTML/CSS/JS로 Supabase 데이터를 조회하여 표시
> - ❌ 불가능: 서버 사이드 로직 (Python, Node.js 백엔드)
> - 💡 해결책: 데이터 수집은 GitHub Actions에서, 표시는 GitHub Pages에서 담당

---

## 5. 시스템 아키텍처 (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                     Scheduler (Cron/GitHub Actions)          │
│                         매일 오전 9시 트리거                    │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Collectors                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   GitHub     │  │  Hacker News │  │  Other News  │       │
│  │   Trending   │  │     API      │  │   Sources    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Processor                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Parsing    │  │   Analysis   │  │   Formatting │       │
│  │              │  │   & Scoring  │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Notification Service                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Email   │  │  Slack   │  │  Discord │  │   Web    │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 데이터 모델 (Data Model)

### 6.1 TrendingRepository
```python
class TrendingRepository:
    name: str              # 저장소 이름 (owner/repo)
    description: str       # 저장소 설명
    url: str               # GitHub URL
    language: str          # 주요 프로그래밍 언어
    stars: int             # 총 Star 수
    stars_today: int       # 오늘 증가한 Star 수
    forks: int             # Fork 수
    collected_at: datetime # 수집 시간
    
    # AI 생성 필드
    ai_summary: str        # AI가 생성한 기술 설명
    ai_use_cases: List[str]  # AI가 추천한 사용처 목록
    ai_difficulty: str     # 학습 난이도 (초급/중급/고급)
    ai_related_tech: List[str]  # 관련 기술 스택
```

### 6.2 NewsArticle
```python
class NewsArticle:
    title: str             # 기사 제목
    summary: str           # 기사 요약
    url: str               # 원문 URL
    source: str            # 뉴스 소스 (HN, TechCrunch 등)
    category: str          # 카테고리
    published_at: datetime # 발행일
    score: int             # 인기도 점수 (optional)
    collected_at: datetime # 수집 시간
```

### 6.3 DailyDigest
```python
class DailyDigest:
    date: date                           # 날짜
    trending_repos: List[TrendingRepository]
    news_articles: List[NewsArticle]
    top_keywords: List[str]              # 상위 키워드
    
    # AI 생성 필드
    ai_daily_summary: str                # 오늘의 기술 트렌드 종합 요약
    ai_hot_technologies: List[dict]      # 주목할 기술 + 설명 + 사용처
    ai_learning_recommendations: List[str]  # 학습 추천 ("이번 주에 배워볼 만한 기술")
    
    created_at: datetime
```

### 6.4 AIAnalysis (신규)
```python
class AIAnalysis:
    technology_name: str       # 기술/라이브러리 이름
    category: str              # 카테고리 (AI, Web, DevOps 등)
    
    # 기술 설명
    what_is_it: str            # "이 기술은 무엇인가요?"
    key_features: List[str]    # 핵심 특징 3~5가지
    comparison: str            # 유사 기술과 비교
    
    # 사용처 추천
    use_cases: List[str]       # 실무 활용 사례
    project_types: List[str]   # 적합한 프로젝트 유형
    difficulty_level: str      # 초급/중급/고급
    related_stack: List[str]   # 함께 사용하면 좋은 기술
    
    # 메타 정보
    generated_at: datetime
    llm_model: str             # 사용된 AI 모델
```

---

## 7. API 명세 (API Specification)

### 7.1 수동 트리거 API
```
POST /api/digest/trigger
- 설명: 수동으로 데일리 다이제스트 생성 트리거
- 응답: { "status": "success", "digest_id": "..." }
```

### 7.2 다이제스트 조회 API
```
GET /api/digest/{date}
- 설명: 특정 날짜의 다이제스트 조회
- 파라미터: date (YYYY-MM-DD)
- 응답: DailyDigest 객체
```

### 7.3 트렌딩 저장소 조회 API
```
GET /api/trending
- 설명: 최신 트렌딩 저장소 목록 조회
- 쿼리 파라미터: language (optional), limit (default: 25)
- 응답: List[TrendingRepository]
```

---

## 8. 개발 Task 목록

> 📌 상세 Task 목록은 [TASKS.md](./TASKS.md) 파일을 참조하세요.

### Phase 요약

| Phase | 내용 | Task 수 | 예상 시간 |
|-------|------|---------|----------|
| Phase 1 | 프로젝트 초기 설정 | 6 | 3.5h |
| Phase 2 | GitHub Trending 수집 | 9 | 9.5h |
| Phase 3 | IT 뉴스 수집 | 8 | 10h |
| Phase 4 | Supabase 연동 | 7 | 6h |
| Phase 5 | AI 기술 분석 ⭐ | 12 | 11.5h |
| Phase 6 | 데이터 포맷팅 | 5 | 5.5h |
| Phase 7 | 알림 채널 연동 | 9 | 10h |
| Phase 8 | GitHub Actions | 7 | 6h |
| Phase 9 | 웹 대시보드 | 10 | 13h |
| Phase 10 | 테스트 및 안정화 | 6 | 7.5h |
| **총계** | | **79** | **약 82시간** |

---

## 9. 성공 지표 (Success Metrics)

### 9.1 기술 지표
| 지표 | 목표 |
|------|------|
| 데이터 수집 성공률 | 99% 이상 |
| 알림 발송 성공률 | 99% 이상 |
| 수집-발송 소요 시간 | 5분 이내 |

### 9.2 사용자 지표
| 지표 | 목표 |
|------|------|
| 일일 활성 구독자 | - |
| 이메일 오픈율 | 40% 이상 |
| 링크 클릭률 | 20% 이상 |

---

## 10. 리스크 및 대응 방안

| 리스크 | 영향도 | 대응 방안 |
|--------|--------|----------|
| GitHub Trending 페이지 구조 변경 | 높음 | 정기적 모니터링, 대체 API 검토 |
| 뉴스 소스 API 제한 | 중간 | 캐싱, Rate Limiting 준수, 다중 소스 활용 |
| 스케줄러 실패 | 중간 | 재시도 로직, 실패 알림 설정 |
| 스팸 필터 차단 (이메일) | 중간 | SPF/DKIM 설정, 발송 도메인 인증 |

---

## 11. 향후 확장 계획

1. **다국어 지원**: 영어, 일본어 뉴스 소스 추가
2. **개인화**: 관심 기술/언어 기반 맞춤 필터링
3. **히스토리 분석**: 주간/월간 트렌드 리포트
4. **커뮤니티 기능**: 북마크, 코멘트 기능
5. **모바일 앱**: 푸시 알림 지원

---

## 12. 부록

### 12.1 참고 자료
- [GitHub Trending](https://github.com/trending)
- [Hacker News API](https://github.com/HackerNews/API)
- [GeekNews](https://news.hada.io/)

### 12.2 용어 정의
- **Trending**: 특정 기간 동안 인기가 급상승한 저장소/기술
- **Digest**: 수집된 정보를 정리한 일일 요약본
- **웹훅**: 외부 서비스로 데이터를 자동 전송하는 방식

---

*이 문서는 프로젝트 진행에 따라 업데이트될 수 있습니다.*
