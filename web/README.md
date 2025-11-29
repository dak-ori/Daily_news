# 웹 대시보드

GitHub Pages를 통해 Daily Tech Digest를 웹에서 확인할 수 있습니다.

## 설정 방법

### 1. Supabase 설정

`app.js` 파일에서 Supabase URL과 Anon Key를 설정하세요:

```javascript
const SUPABASE_URL = 'your_supabase_url';
const SUPABASE_ANON_KEY = 'your_supabase_anon_key';
```

### 2. GitHub Pages 배포

#### 방법 1: Settings에서 배포

1. GitHub 저장소의 **Settings** > **Pages**로 이동
2. **Source**를 `Deploy from a branch`로 선택
3. **Branch**를 `main` (또는 `master`) 선택하고 폴더를 `/web`으로 설정
4. **Save** 클릭

#### 방법 2: GitHub Actions로 배포

`.github/workflows/deploy-pages.yml` 파일을 생성:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './web'

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

### 3. 접속

배포 후 `https://your-username.github.io/daily_news/`에서 확인할 수 있습니다.

## 기능

- ✅ 최신 Daily Digest 조회
- ✅ GitHub Trending 저장소 목록
- ✅ IT 뉴스 목록
- ✅ AI 분석 결과 표시
- ✅ 반응형 디자인 (모바일 지원)

## 기술 스택

- HTML5
- Tailwind CSS (CDN)
- JavaScript (Vanilla)
- Supabase JS SDK
