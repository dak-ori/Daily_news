-- ============================================
-- Daily Tech Trends Database Schema
-- ============================================

-- trending_repos 테이블
CREATE TABLE IF NOT EXISTS trending_repos (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    url VARCHAR(500) NOT NULL,
    language VARCHAR(50),
    stars INTEGER DEFAULT 0,
    stars_today INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,
    ai_summary TEXT,
    ai_use_cases JSONB,
    ai_difficulty VARCHAR(20),
    ai_related_tech JSONB,
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- news_articles 테이블
CREATE TABLE IF NOT EXISTS news_articles (
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
CREATE TABLE IF NOT EXISTS daily_digests (
    id SERIAL PRIMARY KEY,
    digest_date DATE UNIQUE NOT NULL,
    top_keywords JSONB,
    ai_daily_summary TEXT,
    ai_hot_technologies JSONB,
    ai_learning_recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_trending_repos_collected_at ON trending_repos(collected_at DESC);
CREATE INDEX IF NOT EXISTS idx_trending_repos_language ON trending_repos(language);
CREATE INDEX IF NOT EXISTS idx_news_articles_collected_at ON news_articles(collected_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_articles_source ON news_articles(source);
CREATE INDEX IF NOT EXISTS idx_daily_digests_date ON daily_digests(digest_date DESC);

-- Row Level Security (RLS) 설정
ALTER TABLE trending_repos ENABLE ROW LEVEL SECURITY;
ALTER TABLE news_articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_digests ENABLE ROW LEVEL SECURITY;

-- 공개 읽기 정책
CREATE POLICY "Allow public read access" ON trending_repos
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON news_articles
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access" ON daily_digests
    FOR SELECT USING (true);

-- 공개 쓰기 정책 (서비스에서 데이터 저장 가능하도록)
CREATE POLICY "Allow public insert access" ON trending_repos
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public insert access" ON news_articles
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public insert access" ON daily_digests
    FOR INSERT WITH CHECK (true);

-- 공개 업데이트 정책
CREATE POLICY "Allow public update access" ON trending_repos
    FOR UPDATE USING (true);

CREATE POLICY "Allow public update access" ON news_articles
    FOR UPDATE USING (true);

CREATE POLICY "Allow public update access" ON daily_digests
    FOR UPDATE USING (true);
