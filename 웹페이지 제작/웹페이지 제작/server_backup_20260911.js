require('dotenv').config();
const express = require('express');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

const CLIENT_ID = process.env.TWITCH_CLIENT_ID;
const CLIENT_SECRET = process.env.TWITCH_CLIENT_SECRET;

// CORS 완전 허용
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
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

// 정적 파일 서빙
app.use(express.static(path.join(__dirname)));
app.use('/portfolio-assets', express.static(path.join(__dirname, '포폴 정리용')));

// 헬스체크 엔드포인트
app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        hasTwitchCredentials: !!(CLIENT_ID && CLIENT_SECRET)
    });
});

let cachedToken = null;
let tokenExpiry = null;

async function getAccessToken() {
    if (cachedToken && tokenExpiry && Date.now() < tokenExpiry - 60000) {
        return cachedToken;
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
        return cachedToken;
    } catch (error) {
        console.error('✗ 트위치 토큰 발급 실패:', error.response ? error.response.data : error.message);
        throw error;
    }
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
            const token = await getAccessToken();
            const headers = {
                'Client-ID': CLIENT_ID,
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'text/plain'
            };
            const defaultQuery = 'fields name, cover.image_id, platforms.name, genres.name, first_release_date, aggregated_rating_count; where aggregated_rating_count > 10 & cover != null; sort aggregated_rating_count desc; limit 20;';
            const igdbRes = await axios.post('https://api.igdb.com/v4/games', defaultQuery, { headers, timeout: 8000 });
            
            const games = (igdbRes.data || []).map(game => ({
                id: game.id,
                title: game.name,
                platform: game.platforms ? game.platforms.map(p => p.name).join(' / ') : '정보 없음',
                genre:    game.genres    ? game.genres.map(g => g.name).join(' / ')    : '정보 없음',
                coverUrl: game.cover     ? `https://images.igdb.com/igdb/image/upload/t_cover_big/${game.cover.image_id}.jpg` : null,
                releaseYear: game.first_release_date ? new Date(game.first_release_date * 1000).getFullYear() : null
            }));

            return res.json(games.length > 0 ? games : fallbackPopularGames);
        } catch (e) {
            console.warn('[IGDB 기본목록 오류 폴백]', e.message);
            return res.json(fallbackPopularGames);
        }
    }

    query = query.trim();
    const lowerQuery = query.toLowerCase();
    const mappedQuery = koreanGameMap[query] || koreanGameMap[lowerQuery] || query;
    console.log(`[IGDB 검색 요청] 원본: "${query}" -> 매핑: "${mappedQuery}"`);

    try {
        const token = await getAccessToken();
        const safeQuery = mappedQuery.replace(/"/g, '').trim();
        const headers = {
            'Client-ID': CLIENT_ID,
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'text/plain'
        };

        const searchQuery = `search "${safeQuery}"; fields name, cover.image_id, platforms.name, genres.name, first_release_date, aggregated_rating_count; limit 30;`;
        const nameQuery = `fields name, cover.image_id, platforms.name, genres.name, first_release_date, aggregated_rating_count; where name ~ *"${safeQuery}"*; sort aggregated_rating_count desc; limit 30;`;

        const [searchRes, nameRes] = await Promise.allSettled([
            axios.post('https://api.igdb.com/v4/games', searchQuery, { headers, timeout: 10000 }),
            axios.post('https://api.igdb.com/v4/games', nameQuery,   { headers, timeout: 10000 })
        ]);

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
        res.json(games);
    } catch (error) {
        console.error('✗ IGDB 검색 오류:', error.response ? error.response.data : error.message);
        // 오류 발생 시에도 사용자에게 빈 화면이나 500 에러 대신 폴백 추천 목록을 반환
        const filteredFallback = fallbackPopularGames.filter(g => 
            g.title.toLowerCase().includes(query.toLowerCase())
        );
        res.json(filteredFallback.length > 0 ? filteredFallback : fallbackPopularGames);
    }
});

// 포트폴리오 문서 카테고리 정의
const docCategories = [
    {
        category: '공식 제출 서류 (이력서 및 자기소개서)',
        badge: 'CAREER & ESSAY',
        items: [
            {
                name: '20260901_12-3_이력서_Ver01_정승운.pdf',
                folder: 'root',
                title: '정승운 이력서 Ver01',
                desc: '인적사항, 기술 스택, 영화 및 게임 개발 프로젝트 이력, 학력 상세 기재 원본',
                project: '커리어 공식 서류',
                type: 'PDF'
            },
            {
                name: '20260904_13-1_자기소개서_Ver01_정승운.pdf',
                folder: 'root',
                title: '정승운 자기소개서 Ver01',
                desc: '지원 동기, AI 행동 트리 전투 로직 구축 역량, UI 리소스 갈등 조율 및 문제 해결 경험',
                project: '커리어 공식 서류',
                type: 'PDF'
            }
        ]
    },
    {
        category: '프로젝트 기획서 (슬기로운 재배생활 / 파송송계란탁)',
        badge: 'GDD & DESIGN',
        items: [
            {
                name: '0705_슬기로운재배생활컨셉기획서_Ver01.pdf',
                folder: 'portfolio',
                title: '슬기로운 재배생활 컨셉 기획서 Ver01',
                desc: '게임의 핵심 플레이 루프, 타겟층, 세계관 및 힐링 재배 시뮬레이션 초기 컨셉 정의',
                project: '슬기로운 재배생활',
                type: 'PDF'
            },
            {
                name: '0708_비주얼 가이드_Ver05.pdf',
                folder: 'portfolio',
                title: '슬기로운 재배생활 비주얼 가이드 Ver05',
                desc: '게임 내 아트 스타일 가이드라인, 컬러 팔레트, 타일셋 및 오브젝트 규격 정의',
                project: '슬기로운 재배생활',
                type: 'PDF'
            },
            {
                name: '0709_UI화면기획_ver05.pdf',
                folder: 'portfolio',
                title: '슬기로운 재배생활 UI 화면 기획서 Ver05',
                desc: '각 화면별 UI 플로우, 슬롯 타이머 표시 규격, 인벤토리/제작 화면 상세 와이어프레임',
                project: '슬기로운 재배생활',
                type: 'PDF'
            },
            {
                name: '0718_시스템기획서_Ver03.pdf',
                folder: 'portfolio',
                title: '슬기로운 재배생활 시스템 기획서 Ver03',
                desc: '재배, 수확, 가공, 무역 연계 경제 사이클 및 유한 상태 객체 인터랙션 시스템',
                project: '슬기로운 재배생활',
                type: 'PDF'
            },
            {
                name: '20260722_7-5_컨셉기획서_Ver05_파송송계란탁 (1).pdf',
                folder: 'portfolio',
                title: '파송송계란탁 컨셉 기획서 Ver05',
                desc: '팀 파송송계란탁 프로젝트 통합 컨셉 기획서 및 코어 메커니즘 정리',
                project: '파송송계란탁',
                type: 'PDF'
            }
        ]
    },
    {
        category: '캐릭터 & 세계관 가이드 (PPTX)',
        badge: 'CHARACTER & WORLD',
        items: [
            {
                name: '20260810_캐릭터가이드_Ver02_파송송계란탁.pptx',
                folder: 'portfolio',
                title: '캐릭터 가이드 Ver02',
                desc: '등장 캐릭터들의 전반적인 설정, 성격, 모션 및 대사 톤앤매너 통합 가이드',
                project: '파송송계란탁',
                type: 'PPTX'
            },
            {
                name: '20260828_세라피엘 기획서_Ver01_파송송계란탁.pptx',
                folder: 'portfolio',
                title: '캐릭터 기획서: 세라피엘 (Seraphiel)',
                desc: '세라피엘 캐릭터 설정, 외형 특징, 고유 스킬 및 배경 시나리오 기획서',
                project: '파송송계란탁',
                type: 'PPTX'
            },
            {
                name: '20260828_시안 기획서_Ver01_파송송계란탁.pptx',
                folder: 'portfolio',
                title: '캐릭터 기획서: 시안 (Cyan)',
                desc: '시안 캐릭터 성격, 전투 메커니즘, 기획 의도 및 상호작용 트리',
                project: '파송송계란탁',
                type: 'PPTX'
            },
            {
                name: '20260828_아르세니아 기획서_Ver01_파송송계란탁.pptx',
                folder: 'portfolio',
                title: '캐릭터 기획서: 아르세니아 (Arsenia)',
                desc: '아르세니아 캐릭터 컨셉, 스킬 셋, 그래픽 레퍼런스 및 밸런스 지표',
                project: '파송송계란탁',
                type: 'PPTX'
            },
            {
                name: '20260828_엘린 기획서_Ver01_파송송계란탁.pptx',
                folder: 'portfolio',
                title: '캐릭터 기획서: 엘린 (Elin)',
                desc: '엘린 캐릭터 프로필, 감정 표현 스프라이트 기획 및 퀘스트 연계',
                project: '파송송계란탁',
                type: 'PPTX'
            },
            {
                name: '20260901_유물발굴기획서_Ver01_파송송계란탁.pptx',
                folder: 'portfolio',
                title: '유물 발굴 시스템 기획서 Ver01',
                desc: '유물 탐색 및 발굴 미니게임 시스템, 보상 테이블 및 유물 도감 기획',
                project: '파송송계란탁',
                type: 'PPTX'
            }
        ]
    },
    {
        category: '시스템 밸런스 & 데이터 테이블 (XLSX)',
        badge: 'DATA & BALANCE',
        items: [
            {
                name: '재배테이블.xlsx',
                folder: 'portfolio',
                title: '작물 재배 데이터 테이블',
                desc: '작물별 생장 시간, 필요 영양분, 수확량, 단계별 스프라이트 매핑',
                project: '슬기로운 재배생활',
                type: 'XLSX'
            },
            {
                name: '제조테이블.xlsx',
                folder: 'portfolio',
                title: '가공 및 제조 레시피 테이블',
                desc: '조합 공식, 제조 소요 시간, 결과물 티어 및 숙련도별 보너스',
                project: '슬기로운 재배생활',
                type: 'XLSX'
            },
            {
                name: '무역소 테이블.xlsx',
                folder: 'portfolio',
                title: '무역소 경제 및 시세 변동 테이블',
                desc: '지역별 거래 품목, 기준 가격, 시세 변동 알고리즘 및 마진율',
                project: '슬기로운 재배생활',
                type: 'XLSX'
            },
            {
                name: '캐릭터테이블.xlsx',
                folder: 'portfolio',
                title: '캐릭터 스탯 및 성장 테이블',
                desc: '레벨별 스탯 성장 곡선, 필요 경험치, 특성 해금 조건',
                project: '파송송계란탁',
                type: 'XLSX'
            },
            {
                name: '설명 테이블.xlsx',
                folder: 'portfolio',
                title: '게임 내 툴팁 및 설명 텍스트 테이블',
                desc: '아이템, 버프/디버프, 도움말 텍스트 ID 및 다국어 대비 텍스트',
                project: '슬기로운 재배생활',
                type: 'XLSX'
            },
            {
                name: '0708_마일스톤_Ver01.xlsx',
                folder: 'portfolio',
                title: '개발 일정 마일스톤 관리 시트',
                desc: '주차별 개발 목표, 스프린트 관리, 파트별(기획/아트/클라) R&R 분배',
                project: '슬기로운 재배생활',
                type: 'XLSX'
            },
            {
                name: '0717_QA 구동 확인_Ver01.xlsx',
                folder: 'portfolio',
                title: 'QA 테스트 체크리스트 및 구동 확인 시트',
                desc: '빌드별 기능 검증 체크리스트, 발견된 버그 현황 및 해결 상태 추적',
                project: '슬기로운 재배생활',
                type: 'XLSX'
            }
        ]
    }
];

// 포트폴리오 문서 목록 API
app.get('/api/portfolio-documents', (req, res) => {
    const baseDir = path.join(__dirname, '포폴 정리용');
    const portfolioDir = path.join(baseDir, '포트폴리오');
    
    const enriched = docCategories.map(cat => ({
        ...cat,
        items: cat.items.map(item => {
            const targetFolder = item.folder === 'root' ? baseDir : portfolioDir;
            const filePath = path.join(targetFolder, item.name);
            let size = 0;
            let exists = false;
            try {
                if (fs.existsSync(filePath)) {
                    const stat = fs.statSync(filePath);
                    size = stat.size;
                    exists = true;
                }
            } catch (e) {}

            return {
                ...item,
                exists,
                sizeBytes: size,
                sizeFormatted: size > 1024 * 1024 
                    ? (size / (1024 * 1024)).toFixed(1) + ' MB' 
                    : (size / 1024).toFixed(0) + ' KB',
                url: `/api/download?file=${encodeURIComponent(item.name)}&folder=${item.folder || 'portfolio'}`
            };
        })
    }));

    res.json(enriched);
});

// 문서 다운로드 API
app.get('/api/download', (req, res) => {
    const filename = req.query.file;
    const folderType = req.query.folder || 'portfolio';
    if (!filename) {
        return res.status(400).send('파일명이 필요합니다.');
    }

    const safeFilename = path.basename(filename);
    const baseDir = path.join(__dirname, '포폴 정리용');
    const filePath = folderType === 'root'
        ? path.join(baseDir, safeFilename)
        : path.join(baseDir, '포트폴리오', safeFilename);

    if (!fs.existsSync(filePath)) {
        console.warn('다운로드 파일 없음:', filePath);
        return res.status(404).send('파일을 찾을 수 없습니다.');
    }

    const ext = path.extname(safeFilename).toLowerCase();
    
    if (ext === '.pdf') {
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', `inline; filename*=UTF-8''${encodeURIComponent(safeFilename)}`);
    } else {
        res.setHeader('Content-Disposition', `attachment; filename*=UTF-8''${encodeURIComponent(safeFilename)}`);
    }

    fs.createReadStream(filePath).pipe(res);
});

const server = app.listen(PORT, () => {
    console.log('🚀 서버가 http://localhost:' + PORT + ' 에서 안정적으로 가동 중입니다.');
    console.log('🌐 포트폴리오 웹페이지: http://localhost:' + PORT + '/index.html');
});

// 프로세스 예외 핸들링
process.on('uncaughtException', (err) => {
    console.error('서버 예외 감지 (복구됨):', err.message);
});
process.on('unhandledRejection', (reason, promise) => {
    console.error('비동기 예외 감지 (복구됨):', reason);
});
