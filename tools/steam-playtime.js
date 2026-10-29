// ─────────────────────────────────────────────
// 스팀 플레이 시간 DB 갱신: data/steam-playtime.json
//  - 이 PC 스팀 클라이언트 기록(userdata/<계정>/config/localconfig.vdf)의 게임별 Playtime(분)을 읽음
//    (스팀 프로필의 게임 목록이 비공개여도 동작)
//  - 게임 이름 · 장르는 스팀 상점 공개 API 로 조회
//  - 실행: node tools/steam-playtime.js
// ─────────────────────────────────────────────
const fs = require('fs');
const path = require('path');

const STEAM_ID64 = '76561198112205675';               // 스팀 프로필 (MITAKE RAN)
const ACCOUNT_ID = String(BigInt(STEAM_ID64) - 76561197960265728n);
const STEAM_DIR = process.env.STEAM_DIR || 'C:/Program Files (x86)/Steam';
const VDF_FILE = path.join(STEAM_DIR, 'userdata', ACCOUNT_ID, 'config', 'localconfig.vdf');
const OUT_FILE = path.join(__dirname, '..', 'data', 'steam-playtime.json');
const MIN_MINUTES = 60;                                 // 1시간 미만은 제외

// 플레이 히스토리 레이더 3축 분류 (없으면 'etc')
const CATEGORY = {
    strategy: [289070, 268500, 1158310, 1054490, 2438990, 646570, 2868840, 570, 1049590, 286160],
    management: [1904540, 1569040, 1263850, 1100600, 703080, 413150, 322330, 1623730, 892970, 648800, 1301390],
    rpg: [1086940, 262060, 527230]
};
// 게임이 아닌 앱 · 에디터 (백그라운드 실행 시간이 쌓여 제외)
const EXCLUDE = [431960, 2066750, 1624110, 1100760, 1436120];
// 표시 이름 다듬기
const NAME_OVERRIDE = {
    289070: "Sid Meier's Civilization VI", 268500: 'XCOM 2', 262060: 'Darkest Dungeon', 1054490: 'Wingspan (윙스팬)',
    1623730: 'Palworld (팰월드)', 1238810: 'Battlefield V', 1172620: 'Sea of Thieves', 271590: 'Grand Theft Auto V', 1049590: '이터널 리턴'
};

function readPlaytimes() {
    const text = fs.readFileSync(VDF_FILE, 'utf-8');
    const out = [];
    for (const m of text.matchAll(/"(\d+)"\s*\{([^{}]*)\}/g)) {
        const p = /"Playtime"\s*"(\d+)"/.exec(m[2]);
        if (!p || +p[1] < MIN_MINUTES) continue;
        const appid = +m[1];
        if (EXCLUDE.includes(appid)) continue;
        const lp = /"LastPlayed"\s*"(\d+)"/.exec(m[2]);
        out.push({ appid, minutes: +p[1], lastPlayed: lp && +lp[1] ? new Date(+lp[1] * 1000).toISOString().slice(0, 10) : null });
    }
    return out.sort((a, b) => b.minutes - a.minutes);
}

async function storeInfo(appid) {
    try {
        const r = await fetch(`https://store.steampowered.com/api/appdetails?appids=${appid}&l=koreana&filters=basic,genres`);
        const j = await r.json();
        const d = j[appid] && j[appid].data;
        return d ? { name: d.name, genres: (d.genres || []).map(g => g.description) } : null;
    } catch (e) { return null; }
}

(async () => {
    const prev = fs.existsSync(OUT_FILE) ? JSON.parse(fs.readFileSync(OUT_FILE, 'utf-8')) : { games: [] };
    const prevById = Object.fromEntries((prev.games || []).map(g => [g.appid, g]));
    const games = [];
    for (const g of readPlaytimes()) {
        const info = (prevById[g.appid] && prevById[g.appid].name) ? prevById[g.appid] : await storeInfo(g.appid);
        const category = Object.keys(CATEGORY).find(k => CATEGORY[k].includes(g.appid)) || 'etc';
        games.push({
            appid: g.appid,
            name: NAME_OVERRIDE[g.appid] || (info && info.name) || `App ${g.appid}`,
            genres: (info && info.genres) || [],
            category,
            hours: Math.round(g.minutes / 6) / 10,
            lastPlayed: g.lastPlayed,
            cover: `https://cdn.cloudflare.steamstatic.com/steam/apps/${g.appid}/library_600x900.jpg`,
            store: `https://store.steampowered.com/app/${g.appid}/`
        });
    }
    const data = {
        source: 'Steam 클라이언트 기록 (localconfig.vdf)',
        profile: `https://steamcommunity.com/profiles/${STEAM_ID64}`,
        updatedAt: new Date().toISOString().slice(0, 10),
        totalHours: Math.round(games.reduce((n, g) => n + g.hours, 0)),
        games
    };
    fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
    fs.writeFileSync(OUT_FILE, JSON.stringify(data, null, 2), 'utf-8');
    console.log(`steam-playtime.json 갱신: 게임 ${games.length}개 · 총 ${data.totalHours.toLocaleString()}시간`);
    games.slice(0, 10).forEach(g => console.log(`  ${g.hours.toString().padStart(7)}h  ${g.name}`));
})();
