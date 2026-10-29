const path = require('path');
const fs = require('fs');
// .env 는 server.js 와 같은 폴더에서 읽는다 (다른 폴더에서 node 를 실행해도 키가 빠지지 않도록)
require('dotenv').config({ path: path.join(__dirname, '.env') });
const express = require('express');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

// 값 앞뒤 공백/따옴표가 섞여 들어가도 인증이 깨지지 않도록 정리
const cleanEnv = (v) => (v || '').trim().replace(/^['"]|['"]$/g, '').trim();
const CLIENT_ID = cleanEnv(process.env.TWITCH_CLIENT_ID);
const CLIENT_SECRET = cleanEnv(process.env.TWITCH_CLIENT_SECRET);

// IGDB(트위치) 연결 상태: unknown | ok | missing | invalid_client | invalid_secret | network_error | error
const igdbStatus = { state: 'unknown', message: '아직 확인 전', checkedAt: null };
function setIgdbStatus(state, message) {
    igdbStatus.state = state;
    igdbStatus.message = message;
    igdbStatus.checkedAt = new Date().toISOString();
}

function checkEnvFormat() {
    const problems = [];
    if (!fs.existsSync(path.join(__dirname, '.env'))) problems.push('.env 파일이 server.js 와 같은 폴더에 없습니다.');
    if (!CLIENT_ID) problems.push('TWITCH_CLIENT_ID 가 비어 있습니다.');
    if (!CLIENT_SECRET) problems.push('TWITCH_CLIENT_SECRET 가 비어 있습니다.');
    if (CLIENT_ID && !/^[a-z0-9]{20,40}$/.test(CLIENT_ID)) problems.push('TWITCH_CLIENT_ID 형식이 이상합니다 (소문자+숫자 30자 정도여야 함).');
    if (CLIENT_SECRET && !/^[a-z0-9]{20,40}$/.test(CLIENT_SECRET)) problems.push('TWITCH_CLIENT_SECRET 형식이 이상합니다 (소문자+숫자 30자 정도여야 함).');
    if (CLIENT_ID && CLIENT_SECRET && CLIENT_ID === CLIENT_SECRET) problems.push('ID 와 SECRET 이 같은 값입니다. SECRET 자리에 ID 를 붙여넣은 것 같습니다.');
    return problems;
}

// CORS 완전 허용
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-File-Name');
    res.setHeader('Access-Control-Expose-Headers', 'X-IGDB-Status, X-IGDB-Message');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

// 실시간 요청 로깅 미들웨어
app.use((req, res, next) => {
    const start = Date.now();
    res.on('finish', () => {
        if (req.url.startsWith('/api/')) {
            console.log(`[${new Date().toLocaleTimeString()}] ${req.method} ${req.url} -> ${res.statusCode} (${Date.now() - start}ms)`);
        }
    });
    next();
});

app.use(express.json({ limit: '25mb' }));

// 정적 파일 서빙
app.use(express.static(path.join(__dirname)));
app.use('/portfolio-assets', express.static(path.join(__dirname, '포폴 정리용')));

// 헬스체크 엔드포인트
app.get('/api/health', async (req, res) => {
    // 아직 확인 전이거나 실패 상태면 한 번 더 토큰 발급을 시도해 최신 상태를 알려준다
    if (igdbStatus.state !== 'ok' && CLIENT_ID && CLIENT_SECRET) {
        try { await getAccessToken(); } catch (e) { /* 상태는 getAccessToken 에서 기록 */ }
    }
    res.json({
        status: 'ok',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        hasTwitchCredentials: !!(CLIENT_ID && CLIENT_SECRET),
        envProblems: checkEnvFormat(),
        igdb: igdbStatus
    });
});

let cachedToken = null;
let tokenExpiry = null;

async function getAccessToken(forceRefresh = false) {
    if (!forceRefresh && cachedToken && tokenExpiry && Date.now() < tokenExpiry - 60000) {
        return cachedToken;
    }
    if (!CLIENT_ID || !CLIENT_SECRET) {
        setIgdbStatus('missing', '.env 에 TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET 이 없습니다.');
        throw new Error(igdbStatus.message);
    }
    try {
        const response = await axios.post('https://id.twitch.tv/oauth2/token', null, {
            params: {
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
                grant_type: 'client_credentials'
            },
            timeout: 10000
        });
        cachedToken = response.data.access_token;
        tokenExpiry = Date.now() + response.data.expires_in * 1000;
        console.log('✓ 트위치 토큰 발급/갱신 성공! (유효기간:', Math.floor(response.data.expires_in / 3600), '시간)');
        setIgdbStatus('ok', 'IGDB 연결 정상');
        return cachedToken;
    } catch (error) {
        cachedToken = null;
        tokenExpiry = null;
        const data = error.response ? error.response.data : null;
        const msg = (data && data.message) ? String(data.message) : error.message;
        if (error.response && /invalid client secret/i.test(msg)) {
            setIgdbStatus('invalid_secret', 'TWITCH_CLIENT_SECRET 이 틀렸습니다. dev.twitch.tv 콘솔에서 [새 비밀번호]를 발급받아 .env 에 다시 넣어주세요.');
        } else if (error.response && /invalid client/i.test(msg)) {
            setIgdbStatus('invalid_client', 'TWITCH_CLIENT_ID 가 틀렸거나 앱이 삭제되었습니다. dev.twitch.tv 콘솔의 클라이언트 ID 를 확인하세요.');
        } else if (!error.response) {
            setIgdbStatus('network_error', '트위치 인증 서버에 접속하지 못했습니다 (인터넷/방화벽 확인): ' + error.message);
        } else {
            setIgdbStatus('error', '트위치 토큰 발급 실패 (' + error.response.status + '): ' + msg);
        }
        console.error('✗ 트위치 토큰 발급 실패:', igdbStatus.message);
        throw error;
    }
}

// IGDB 호출 공통 함수: 토큰이 만료/폐기돼 401 이 나면 토큰을 새로 받아 1회 재시도
async function igdbPost(body, timeout = 10000) {
    const call = (token) => axios.post('https://api.igdb.com/v4/games', body, {
        headers: { 'Client-ID': CLIENT_ID, 'Authorization': 'Bearer ' + token, 'Content-Type': 'text/plain' },
        timeout
    });
    try {
        return await call(await getAccessToken());
    } catch (e) {
        if (e.response && e.response.status === 401) {
            console.warn('IGDB 401 → 토큰 재발급 후 재시도');
            return await call(await getAccessToken(true));
        }
        throw e;
    }
}

function markIgdb(res, state, message) {
    res.setHeader('X-IGDB-Status', state);
    res.setHeader('X-IGDB-Message', encodeURIComponent(message || ''));
}

// 한글 게임 검색어 영문 자동 매핑 사전 (대폭 확장)
const koreanGameMap = {
    '문명': 'Civilization',
    '문명6': 'Civilization VI',
    '문명 6': 'Civilization VI',
    '문명5': 'Civilization V',
    '문명 5': 'Civilization V',
    '림월드': 'RimWorld',
    '풋볼매니저': 'Football Manager',
    '에펨': 'Football Manager',
    'fm': 'Football Manager',
    'fm2024': 'Football Manager 2024',
    '시티즈': 'Cities: Skylines',
    '시티즈스카이라인': 'Cities: Skylines',
    '마리오': 'Mario',
    '슈퍼마리오': 'Super Mario',
    '젤다': 'The Legend of Zelda',
    '젤다의 전설': 'The Legend of Zelda',
    '젤다의전설': 'The Legend of Zelda',
    '야숨': 'The Legend of Zelda: Breath of the Wild',
    '왕눈': 'The Legend of Zelda: Tears of the Kingdom',
    '포켓몬': 'Pokemon',
    '포켓몬스터': 'Pokemon',
    '스타': 'StarCraft',
    '스타크래프트': 'StarCraft',
    '스타2': 'StarCraft II',
    '디아': 'Diablo',
    '디아블로': 'Diablo',
    '디아4': 'Diablo IV',
    '롤': 'League of Legends',
    '리그오브레전드': 'League of Legends',
    '배그': 'PUBG: BATTLEGROUNDS',
    '배틀그라운드': 'PUBG: BATTLEGROUNDS',
    '사이버펑크': 'Cyberpunk 2077',
    '사펑': 'Cyberpunk 2077',
    '위쳐': 'The Witcher',
    '위쳐3': 'The Witcher 3: Wild Hunt',
    '발더스': 'Baldur\'s Gate',
    '발더스게이트': 'Baldur\'s Gate',
    '발더스3': 'Baldur\'s Gate 3',
    '발더스게이트3': 'Baldur\'s Gate 3',
    '엘든링': 'Elden Ring',
    '다크소울': 'Dark Souls',
    '블러드본': 'Bloodborne',
    '세키로': 'Sekiro: Shadows Die Twice',
    '아머드코어': 'Armored Core',
    '몬헌': 'Monster Hunter',
    '몬스터헌터': 'Monster Hunter',
    '몬헌월드': 'Monster Hunter: World',
    '동물의숲': 'Animal Crossing',
    '동숲': 'Animal Crossing',
    '모동숲': 'Animal Crossing: New Horizons',
    '팰월드': 'Palworld',
    '철권': 'Tekken',
    '철권8': 'Tekken 8',
    '스파': 'Street Fighter',
    '스트리트파이터': 'Street Fighter',
    '스트리트파이터6': 'Street Fighter 6',
    '원신': 'Genshin Impact',
    '붕괴': 'Honkai',
    '스타레일': 'Honkai: Star Rail',
    '붕괴스타레일': 'Honkai: Star Rail',
    '마인크래프트': 'Minecraft',
    '마크': 'Minecraft',
    '로블록스': 'Roblox',
    '하스스톤': 'Hearthstone',
    '오버워치': 'Overwatch',
    '옵치': 'Overwatch 2',
    '발로란트': 'Valorant',
    '산나비': 'SANABI',
    '데이브': 'Dave the Diver',
    '데더다': 'Dave the Diver',
    '스팀': 'Steam',
    '라스트오브어스': 'The Last of Us',
    '라오어': 'The Last of Us',
    '갓오브워': 'God of War',
    '스파이더맨': 'Marvel\'s Spider-Man',
    '레데리': 'Red Dead Redemption',
    '레데리2': 'Red Dead Redemption 2',
    'gta': 'Grand Theft Auto',
    'gta5': 'Grand Theft Auto V'
};

// 기본 인기 추천 게임 캐시 목록
const fallbackPopularGames = [
    { id: 1942, title: 'Sid Meier\'s Civilization VI (2016)', platform: 'PC / Console / Mobile', genre: '전략 / 시뮬레이션', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co49x5.jpg', releaseYear: 2016 },
    { id: 11133, title: 'RimWorld (2018)', platform: 'PC (Steam)', genre: 'SF 생존 / 시뮬레이션', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2k34.jpg', releaseYear: 2018 },
    { id: 260591, title: 'Football Manager 2024 (2023)', platform: 'PC / Console / Mobile', genre: '스포츠 / 경영 시뮬레이션', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co73d7.jpg', releaseYear: 2023 },
    { id: 119133, title: 'Baldur\'s Gate 3 (2023)', platform: 'PC / PS5 / Xbox', genre: 'CRPG / 롤플레잉', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co670h.jpg', releaseYear: 2023 },
    { id: 119171, title: 'Elden Ring (2022)', platform: 'PC / PS5 / Xbox', genre: '액션 RPG / 오픈월드', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co4jni.jpg', releaseYear: 2022 },
    { id: 1877, title: 'Cyberpunk 2077 (2020)', platform: 'PC / PS5 / Xbox', genre: '오픈월드 / 액션 RPG', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2mjt.jpg', releaseYear: 2020 },
    { id: 1009, title: 'StarCraft II: Wings of Liberty (2010)', platform: 'PC', genre: 'RTS / 실시간 전략', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2m37.jpg', releaseYear: 2010 },
    { id: 1334, title: 'Diablo IV (2023)', platform: 'PC / PS5 / Xbox', genre: '핵앤슬래시 / 액션 RPG', coverUrl: 'https://images.igdb.com/igdb/image/upload/t_cover_big/co6b5z.jpg', releaseYear: 2023 }
];

// IGDB 게임 검색 API
app.get('/api/search-games', async (req, res) => {
    let query = req.query.q;
    
    // 검색어가 없으면 인기 추천 게임을 기본으로 반환
    if (!query || query.trim() === '') {
        try {
            const defaultQuery = 'fields name, cover.image_id, platforms.name, genres.name, first_release_date, aggregated_rating_count; where aggregated_rating_count > 10 & cover != null; sort aggregated_rating_count desc; limit 20;';
            const igdbRes = await igdbPost(defaultQuery, 8000);
            
            const games = (igdbRes.data || []).map(game => ({
                id: game.id,
                title: game.name,
                platform: game.platforms ? game.platforms.map(p => p.name).join(' / ') : '정보 없음',
                genre:    game.genres    ? game.genres.map(g => g.name).join(' / ')    : '정보 없음',
                coverUrl: game.cover     ? `https://images.igdb.com/igdb/image/upload/t_cover_big/${game.cover.image_id}.jpg` : null,
                releaseYear: game.first_release_date ? new Date(game.first_release_date * 1000).getFullYear() : null
            }));

            markIgdb(res, 'ok', 'IGDB 실시간 데이터');
            return res.json(games.length > 0 ? games : fallbackPopularGames);
        } catch (e) {
            console.warn('[IGDB 기본목록 오류 폴백]', e.message);
            markIgdb(res, 'fallback', igdbStatus.state === 'ok' ? ('IGDB 요청 실패: ' + e.message) : igdbStatus.message);
            return res.json(fallbackPopularGames);
        }
    }

    query = query.trim();
    const lowerQuery = query.toLowerCase();
    const mappedQuery = koreanGameMap[query] || koreanGameMap[lowerQuery] || query;
    console.log(`[IGDB 검색 요청] 원본: "${query}" -> 매핑: "${mappedQuery}"`);

    try {
        await getAccessToken();
        const safeQuery = mappedQuery.replace(/"/g, '').trim();

        const searchQuery = `search "${safeQuery}"; fields name, cover.image_id, platforms.name, genres.name, first_release_date, aggregated_rating_count; limit 30;`;
        const nameQuery = `fields name, cover.image_id, platforms.name, genres.name, first_release_date, aggregated_rating_count; where name ~ *"${safeQuery}"*; sort aggregated_rating_count desc; limit 30;`;

        const [searchRes, nameRes] = await Promise.allSettled([
            igdbPost(searchQuery),
            igdbPost(nameQuery)
        ]);
        if (searchRes.status === 'rejected' && nameRes.status === 'rejected') {
            throw searchRes.reason;
        }

        const searchGames = searchRes.status === 'fulfilled' ? searchRes.value.data : [];
        const nameGames   = nameRes.status   === 'fulfilled' ? nameRes.value.data   : [];

        const seen = new Set();
        const merged = [];
        for (const g of [...nameGames, ...searchGames]) {
            if (!seen.has(g.id)) {
                seen.add(g.id);
                merged.push(g);
            }
        }

        merged.sort((a, b) => (b.aggregated_rating_count || 0) - (a.aggregated_rating_count || 0));

        let games = merged.slice(0, 30).map(game => ({
            id: game.id,
            title: game.name,
            platform: game.platforms ? game.platforms.map(p => p.name).join(' / ') : '정보 없음',
            genre:    game.genres    ? game.genres.map(g => g.name).join(' / ')    : '정보 없음',
            coverUrl: game.cover     ? `https://images.igdb.com/igdb/image/upload/t_cover_big/${game.cover.image_id}.jpg` : null,
            releaseYear: game.first_release_date
                ? new Date(game.first_release_date * 1000).getFullYear()
                : null
        }));

        // 만약 검색 결과가 없고 fallback 리스트 중에 매칭되는 항목이 있으면 제공
        if (games.length === 0) {
            const fallbackMatches = fallbackPopularGames.filter(g => 
                g.title.toLowerCase().includes(lowerQuery) || 
                g.genre.toLowerCase().includes(lowerQuery)
            );
            if (fallbackMatches.length > 0) {
                games = fallbackMatches;
            }
        }

        console.log(`[IGDB 검색 완료] "${query}" -> ${games.length}개 결과 반환`);
        markIgdb(res, 'ok', 'IGDB 실시간 데이터');
        res.json(games);
    } catch (error) {
        console.error('✗ IGDB 검색 오류:', error.response ? error.response.data : error.message);
        // 오류 발생 시에도 사용자에게 빈 화면이나 500 에러 대신 폴백 추천 목록을 반환
        const filteredFallback = fallbackPopularGames.filter(g => 
            g.title.toLowerCase().includes(query.toLowerCase())
        );
        markIgdb(res, 'fallback', igdbStatus.state === 'ok' ? ('IGDB 요청 실패: ' + error.message) : igdbStatus.message);
        res.json(filteredFallback.length > 0 ? filteredFallback : fallbackPopularGames);
    }
});

// ─────────────────────────────────────────────
// 포트폴리오 문서: '포폴 정리용/<번호_프로젝트>/<기획서|데이터 테이블|게임>' 폴더를 실시간으로 스캔
//  - 폴더에 파일을 넣기만 하면 자동으로 페이지에 등록됨 (서버 재시작 불필요)
//  - 제목/설명은 data/portfolio-meta.json, 없는 파일은 파일명으로 자동 생성
//  - 파일 자체는 위의 express.static 으로 그대로 열림
// ─────────────────────────────────────────────
const { scanPortfolio } = require('./tools/portfolio-scan');

app.get('/api/portfolio-documents', (req, res) => {
    res.json(scanPortfolio());
});

// ─────────────────────────────────────────────
// 편집 모드 저장소: 텍스트/이미지 편집 내용과 추가한 게임을 page-edits.json 에 저장
// ─────────────────────────────────────────────
const EDITS_FILE = path.join(__dirname, 'page-edits.json');
const EDIT_IMG_DIR = path.join(__dirname, 'edit-images');

app.get('/api/page-edits', (req, res) => {
    try {
        if (!fs.existsSync(EDITS_FILE)) return res.json({});
        res.json(JSON.parse(fs.readFileSync(EDITS_FILE, 'utf-8') || '{}'));
    } catch (e) {
        console.error('편집 내용 읽기 실패:', e.message);
        res.status(500).json({ error: '편집 내용 파일을 읽지 못했습니다.' });
    }
});

app.post('/api/page-edits', (req, res) => {
    try {
        const data = req.body && typeof req.body === 'object' ? req.body : {};
        const tmp = EDITS_FILE + '.tmp';
        fs.writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf-8');
        fs.renameSync(tmp, EDITS_FILE);
        res.json({ ok: true, savedAt: new Date().toISOString() });
    } catch (e) {
        console.error('편집 내용 저장 실패:', e.message);
        res.status(500).json({ error: '편집 내용 저장 실패: ' + e.message });
    }
});

// 이미지 업로드 (본문 = 이미지 바이너리, 헤더 X-File-Name = 원본 파일명)
app.post('/api/upload-image', express.raw({ type: () => true, limit: '30mb' }), (req, res) => {
    try {
        if (!req.body || !req.body.length) return res.status(400).json({ error: '이미지 데이터가 없습니다.' });
        const original = decodeURIComponent(req.get('X-File-Name') || 'image.png');
        const m = path.extname(original).toLowerCase().match(/^\.(png|jpe?g|gif|webp|svg|avif)$/);
        const ext = m ? m[0] : '.png';
        fs.mkdirSync(EDIT_IMG_DIR, { recursive: true });
        const name = Date.now() + '_' + Math.random().toString(36).slice(2, 8) + ext;
        fs.writeFileSync(path.join(EDIT_IMG_DIR, name), req.body);
        res.json({ ok: true, url: 'edit-images/' + name });
    } catch (e) {
        console.error('이미지 업로드 실패:', e.message);
        res.status(500).json({ error: '이미지 업로드 실패: ' + e.message });
    }
});

const server = app.listen(PORT, async () => {
    console.log('🚀 서버가 http://localhost:' + PORT + ' 에서 안정적으로 가동 중입니다.');
    console.log('🌐 포트폴리오 웹페이지: http://localhost:' + PORT + '/index.html');
    const problems = checkEnvFormat();
    if (problems.length) {
        console.warn('⚠️  .env 키 설정 문제:');
        problems.forEach(p => console.warn('   - ' + p));
    }
    try {
        await getAccessToken();
        console.log('🎮 IGDB 게임 데이터 서버 연결 확인 완료');
    } catch (e) {
        console.warn('⚠️  IGDB 연결 실패 → ' + igdbStatus.message);
        console.warn('    (연결이 안 되는 동안에는 기본 추천 게임 목록으로 대체됩니다)');
    }
});

// 프로세스 예외 핸들링
process.on('uncaughtException', (err) => {
    console.error('서버 예외 감지 (복구됨):', err.message);
});
process.on('unhandledRejection', (reason, promise) => {
    console.error('비동기 예외 감지 (복구됨):', reason);
});
