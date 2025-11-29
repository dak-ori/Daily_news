-- ============================================
-- RLS INSERT 정책 추가
-- Supabase SQL Editor에서 실행하세요
-- ============================================

-- 공개 쓰기 정책 (서비스에서 데이터 저장 가능하도록)
-- IF NOT EXISTS를 사용할 수 없으므로 DROP IF EXISTS 후 생성
DROP POLICY IF EXISTS "Allow public insert access" ON trending_repos;
CREATE POLICY "Allow public insert access" ON trending_repos
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public insert access" ON news_articles;
CREATE POLICY "Allow public insert access" ON news_articles
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public insert access" ON daily_digests;
CREATE POLICY "Allow public insert access" ON daily_digests
    FOR INSERT WITH CHECK (true);

-- 공개 업데이트 정책
DROP POLICY IF EXISTS "Allow public update access" ON trending_repos;
CREATE POLICY "Allow public update access" ON trending_repos
    FOR UPDATE USING (true);

DROP POLICY IF EXISTS "Allow public update access" ON news_articles;
CREATE POLICY "Allow public update access" ON news_articles
    FOR UPDATE USING (true);

DROP POLICY IF EXISTS "Allow public update access" ON daily_digests;
CREATE POLICY "Allow public update access" ON daily_digests
    FOR UPDATE USING (true);
