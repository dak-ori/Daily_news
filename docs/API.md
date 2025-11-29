# API 문서

## Supabase 데이터베이스 API

Supabase는 자동으로 RESTful API를 생성합니다.

### Base URL

```
https://your-project.supabase.co/rest/v1
```

### Headers

```
apikey: your_supabase_anon_key
Authorization: Bearer your_supabase_anon_key
```

## 엔드포인트

### 1. Trending Repositories

#### GET /trending_repos

트렌딩 저장소 목록 조회

**쿼리 파라미터:**
- `limit`: 결과 개수 (기본값: 25)
- `language`: 언어 필터 (예: `eq.Python`)
- `order`: 정렬 (예: `collected_at.desc`)

**예시:**

```bash
curl "https://your-project.supabase.co/rest/v1/trending_repos?limit=10&order=collected_at.desc" \
  -H "apikey: your_key" \
  -H "Authorization: Bearer your_key"
```

**응답:**

```json
[
  {
    "id": 1,
    "name": "microsoft/autogen",
    "description": "Enable Next-Gen Large Language Model Applications",
    "url": "https://github.com/microsoft/autogen",
    "language": "Python",
    "stars": 15234,
    "stars_today": 123,
    "forks": 1523,
    "ai_summary": "AutoGen은 LLM 기반 애플리케이션을 쉽게 구축할 수 있는 프레임워크입니다.",
    "ai_use_cases": ["챗봇 개발", "자동화 에이전트", "멀티 에이전트 시스템"],
    "ai_difficulty": "중급",
    "ai_related_tech": ["LangChain", "OpenAI", "FastAPI"],
    "collected_at": "2025-11-29T00:00:00Z",
    "created_at": "2025-11-29T00:00:00Z"
  }
]
```

### 2. News Articles

#### GET /news_articles

뉴스 기사 목록 조회

**쿼리 파라미터:**
- `limit`: 결과 개수 (기본값: 50)
- `source`: 소스 필터 (예: `eq.Hacker News`)
- `order`: 정렬 (예: `collected_at.desc`)

**예시:**

```bash
curl "https://your-project.supabase.co/rest/v1/news_articles?limit=20&order=score.desc" \
  -H "apikey: your_key" \
  -H "Authorization: Bearer your_key"
```

**응답:**

```json
[
  {
    "id": 1,
    "title": "OpenAI announces GPT-5",
    "summary": "The next generation of language models",
    "url": "https://example.com/article",
    "source": "Hacker News",
    "category": "AI",
    "score": 523,
    "published_at": "2025-11-28T12:00:00Z",
    "collected_at": "2025-11-29T00:00:00Z",
    "created_at": "2025-11-29T00:00:00Z"
  }
]
```

### 3. Daily Digests

#### GET /daily_digests

일일 다이제스트 조회

**쿼리 파라미터:**
- `digest_date`: 날짜 필터 (예: `eq.2025-11-29`)
- `order`: 정렬 (예: `digest_date.desc`)

**예시:**

```bash
# 최신 다이제스트 조회
curl "https://your-project.supabase.co/rest/v1/daily_digests?order=digest_date.desc&limit=1" \
  -H "apikey: your_key" \
  -H "Authorization: Bearer your_key"
```

**응답:**

```json
[
  {
    "id": 1,
    "digest_date": "2025-11-29",
    "top_keywords": ["AI", "Python", "React"],
    "ai_daily_summary": "오늘은 AI 관련 기술이 주목받고 있습니다...",
    "ai_hot_technologies": [
      {
        "name": "AutoGen",
        "description": "LLM 애플리케이션 프레임워크",
        "why_hot": "멀티 에이전트 지원으로 주목"
      }
    ],
    "ai_learning_recommendations": [
      "LangChain 학습하기",
      "FastAPI로 API 서버 만들기"
    ],
    "created_at": "2025-11-29T00:00:00Z"
  }
]
```

## JavaScript 예시 (Supabase JS SDK)

### 설정

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'your_supabase_url',
  'your_supabase_anon_key'
)
```

### 트렌딩 저장소 조회

```javascript
const { data, error } = await supabase
  .from('trending_repos')
  .select('*')
  .order('collected_at', { ascending: false })
  .limit(10)

if (error) {
  console.error('Error:', error)
} else {
  console.log('Repos:', data)
}
```

### 특정 언어 필터링

```javascript
const { data, error } = await supabase
  .from('trending_repos')
  .select('*')
  .eq('language', 'Python')
  .order('stars_today', { ascending: false })
  .limit(5)
```

### 뉴스 기사 조회

```javascript
const { data, error } = await supabase
  .from('news_articles')
  .select('*')
  .order('collected_at', { ascending: false })
  .limit(20)
```

### 최신 다이제스트 조회

```javascript
const { data, error } = await supabase
  .from('daily_digests')
  .select('*')
  .order('digest_date', { ascending: false })
  .limit(1)
  .single()

if (data) {
  console.log('Latest digest:', data)
}
```

## Python 예시 (Supabase Python SDK)

### 설정

```python
from supabase import create_client

supabase = create_client(
    'your_supabase_url',
    'your_supabase_key'
)
```

### 트렌딩 저장소 조회

```python
response = supabase.table('trending_repos') \
    .select('*') \
    .order('collected_at', desc=True) \
    .limit(10) \
    .execute()

repos = response.data
```

### 뉴스 기사 조회

```python
response = supabase.table('news_articles') \
    .select('*') \
    .eq('source', 'Hacker News') \
    .order('score', desc=True) \
    .limit(20) \
    .execute()

articles = response.data
```

## 에러 응답

### 401 Unauthorized

```json
{
  "message": "Invalid API key"
}
```

### 400 Bad Request

```json
{
  "message": "Invalid query parameters"
}
```

### 500 Internal Server Error

```json
{
  "message": "Internal server error"
}
```

## Rate Limiting

Supabase 무료 티어:
- 50,000 요청/월
- 500MB 데이터베이스
- 1GB 파일 스토리지

유료 티어로 업그레이드 시 제한 완화 가능

## 보안

- Anon Key는 클라이언트 사이드에서 사용 가능
- Row Level Security (RLS)로 읽기 전용 접근 제어
- Service Role Key는 서버 사이드에서만 사용
