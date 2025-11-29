// Supabase 설정
// ⚠️ 주의: 실제 사용 시 SUPABASE_URL과 SUPABASE_ANON_KEY를 설정해야 합니다.
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 상태 관리
let availableDates = [];
let currentDate = null;

// DOM 요소
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const content = document.getElementById('content');
const dailySummary = document.getElementById('daily-summary');
const hotTechnologies = document.getElementById('hot-technologies');
const trendingRepos = document.getElementById('trending-repos');
const newsArticles = document.getElementById('news-articles');
const lastUpdated = document.getElementById('last-updated');
const summarySection = document.getElementById('summary-section');
const hotTechSection = document.getElementById('hot-tech-section');
const dateFilter = document.getElementById('date-filter');
const prevDateBtn = document.getElementById('prev-date');
const nextDateBtn = document.getElementById('next-date');

// 날짜 목록 로드
async function loadAvailableDates() {
    try {
        const { data, error: dateError } = await supabase
            .from('daily_digests')
            .select('digest_date')
            .order('digest_date', { ascending: false });

        if (dateError) throw dateError;

        availableDates = data.map(d => d.digest_date);
        
        // 날짜 선택 UI 업데이트
        if (dateFilter) {
            dateFilter.innerHTML = availableDates.map(date => 
                `<option value="${date}">${formatDateKorean(date)}</option>`
            ).join('');
        }

        return availableDates;
    } catch (err) {
        console.error('날짜 목록 로드 오류:', err);
        return [];
    }
}

// 날짜 한국어 포맷
function formatDateKorean(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'short'
    });
}

// 특정 날짜의 데이터 로드
async function loadDataByDate(selectedDate = null) {
    try {
        loading.classList.remove('hidden');
        content.classList.add('hidden');
        error.classList.add('hidden');

        // 날짜가 지정되지 않으면 최신 날짜 사용
        let targetDate = selectedDate;
        if (!targetDate && availableDates.length > 0) {
            targetDate = availableDates[0];
        }

        // 다이제스트 조회 (날짜 기반)
        let digestQuery = supabase
            .from('daily_digests')
            .select('*');

        if (targetDate) {
            digestQuery = digestQuery.eq('digest_date', targetDate);
        } else {
            digestQuery = digestQuery.order('digest_date', { ascending: false }).limit(1);
        }

        const { data: digest, error: digestError } = await digestQuery.single();

        if (digestError) throw digestError;

        currentDate = digest.digest_date;

        // 트렌딩 저장소 조회 (해당 날짜)
        const startOfDay = new Date(digest.digest_date);
        startOfDay.setHours(0, 0, 0, 0);
        const endOfDay = new Date(digest.digest_date);
        endOfDay.setHours(23, 59, 59, 999);

        const { data: repos, error: reposError } = await supabase
            .from('trending_repos')
            .select('*')
            .gte('collected_at', startOfDay.toISOString())
            .lte('collected_at', endOfDay.toISOString())
            .order('stars_today', { ascending: false })
            .limit(25);

        if (reposError) throw reposError;

        // 뉴스 기사 조회 (해당 날짜)
        const { data: articles, error: articlesError } = await supabase
            .from('news_articles')
            .select('*')
            .gte('collected_at', startOfDay.toISOString())
            .lte('collected_at', endOfDay.toISOString())
            .order('score', { ascending: false })
            .limit(30);

        if (articlesError) throw articlesError;

        // UI 렌더링
        renderDailySummary(digest);
        renderHotTechnologies(digest);
        renderTrendingRepos(repos);
        renderNewsArticles(articles);

        // 마지막 업데이트 시간
        lastUpdated.textContent = `${formatDateKorean(currentDate)} 다이제스트`;

        // 네비게이션 버튼 상태 업데이트
        updateNavigationButtons();

        // 로딩 숨기고 컨텐츠 표시
        loading.classList.add('hidden');
        content.classList.remove('hidden');

    } catch (err) {
        console.error('데이터 로드 오류:', err);
        loading.classList.add('hidden');
        error.classList.remove('hidden');
    }
}

// 네비게이션 버튼 상태 업데이트
function updateNavigationButtons() {
    if (!prevDateBtn || !nextDateBtn) return;
    
    const currentIndex = availableDates.indexOf(currentDate);
    
    // 이전 날짜 버튼 (더 오래된 날짜로)
    prevDateBtn.disabled = currentIndex >= availableDates.length - 1;
    prevDateBtn.classList.toggle('opacity-50', prevDateBtn.disabled);
    
    // 다음 날짜 버튼 (더 최신 날짜로)
    nextDateBtn.disabled = currentIndex <= 0;
    nextDateBtn.classList.toggle('opacity-50', nextDateBtn.disabled);
}

// 이전 날짜로 이동
function goToPreviousDate() {
    const currentIndex = availableDates.indexOf(currentDate);
    if (currentIndex < availableDates.length - 1) {
        const prevDate = availableDates[currentIndex + 1];
        if (dateFilter) dateFilter.value = prevDate;
        loadDataByDate(prevDate);
    }
}

// 다음 날짜로 이동
function goToNextDate() {
    const currentIndex = availableDates.indexOf(currentDate);
    if (currentIndex > 0) {
        const nextDate = availableDates[currentIndex - 1];
        if (dateFilter) dateFilter.value = nextDate;
        loadDataByDate(nextDate);
    }
}

// 기존 loadData 함수 대체
async function loadData() {
    await loadAvailableDates();
    await loadDataByDate();
}

// 일일 요약 렌더링
function renderDailySummary(digest) {
    if (digest.ai_daily_summary) {
        dailySummary.textContent = digest.ai_daily_summary;
    } else {
        summarySection.classList.add('hidden');
    }
}

// 주목할 기술 렌더링
function renderHotTechnologies(digest) {
    if (!digest.ai_hot_technologies || digest.ai_hot_technologies.length === 0) {
        hotTechSection.classList.add('hidden');
        return;
    }

    hotTechnologies.innerHTML = digest.ai_hot_technologies.map(tech => `
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 class="text-xl font-bold text-gray-800 mb-2">${tech.name}</h3>
            <p class="text-gray-700 mb-3">${tech.description}</p>
            ${tech.why_hot ? `
                <p class="text-sm text-yellow-700">
                    <strong>주목받는 이유:</strong> ${tech.why_hot}
                </p>
            ` : ''}
        </div>
    `).join('');
}

// 트렌딩 저장소 렌더링
function renderTrendingRepos(repos) {
    if (!repos || repos.length === 0) {
        trendingRepos.innerHTML = '<p class="text-gray-500">트렌딩 저장소가 없습니다.</p>';
        return;
    }

    trendingRepos.innerHTML = repos.map(repo => `
        <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <h3 class="text-xl font-bold text-blue-600 hover:text-blue-800">
                        <a href="${repo.url}" target="_blank" rel="noopener noreferrer">
                            ${repo.name}
                        </a>
                    </h3>
                    <div class="flex items-center gap-3 mt-2 text-sm text-gray-600">
                        ${repo.language ? `
                            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                ${repo.language}
                            </span>
                        ` : ''}
                        <span>⭐ ${repo.stars.toLocaleString()}</span>
                        <span class="text-yellow-600">+${repo.stars_today} today</span>
                    </div>
                    ${repo.description ? `
                        <p class="text-gray-700 mt-3">${repo.description}</p>
                    ` : ''}
                    ${repo.ai_summary ? `
                        <div class="mt-4 bg-blue-50 border-l-4 border-blue-500 p-3">
                            <p class="text-sm text-gray-700">
                                <strong>AI 분석:</strong> ${repo.ai_summary}
                            </p>
                        </div>
                    ` : ''}
                    ${repo.ai_use_cases && repo.ai_use_cases.length > 0 ? `
                        <div class="mt-3">
                            <strong class="text-sm text-gray-700">활용 사례:</strong>
                            <ul class="list-disc list-inside text-sm text-gray-600 ml-2">
                                ${repo.ai_use_cases.map(use => `<li>${use}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// 뉴스 기사 렌더링
function renderNewsArticles(articles) {
    if (!articles || articles.length === 0) {
        newsArticles.innerHTML = '<p class="text-gray-500">뉴스 기사가 없습니다.</p>';
        return;
    }

    newsArticles.innerHTML = articles.map(article => `
        <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <h3 class="text-lg font-bold text-gray-800 hover:text-blue-600">
                        <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                            ${article.title}
                        </a>
                    </h3>
                    <div class="flex items-center gap-3 mt-2 text-sm text-gray-600">
                        <span class="bg-gray-100 text-gray-800 px-2 py-1 rounded">
                            ${article.source}
                        </span>
                        ${article.score ? `
                            <span class="text-yellow-600">${article.score}점</span>
                        ` : ''}
                        ${article.category ? `
                            <span class="text-gray-500">${article.category}</span>
                        ` : ''}
                    </div>
                    ${article.summary ? `
                        <p class="text-gray-700 mt-3">${article.summary}</p>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// 페이지 로드 시 데이터 로드
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    
    // 날짜 필터 이벤트
    if (dateFilter) {
        dateFilter.addEventListener('change', (e) => {
            loadDataByDate(e.target.value);
        });
    }
    
    // 이전/다음 버튼 이벤트
    if (prevDateBtn) {
        prevDateBtn.addEventListener('click', goToPreviousDate);
    }
    if (nextDateBtn) {
        nextDateBtn.addEventListener('click', goToNextDate);
    }
    
    // 키보드 네비게이션
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            goToPreviousDate();
        } else if (e.key === 'ArrowRight') {
            goToNextDate();
        }
    });
});
