// ─────────────────────────────────────────────
// 포트폴리오 폴더 스캔: '포폴 정리용/<번호_프로젝트>/<기획서|데이터 테이블|게임>/파일'
//  - server.js 의 /api/portfolio-documents 가 실시간으로 사용
//  - 직접 실행하면 data/portfolio.json 을 다시 만든다 (GitHub Pages 처럼 서버 없이 볼 때 사용)
//      node tools/portfolio-scan.js
//  - 제목/설명은 data/portfolio-meta.json, 없으면 파일명에서 자동 생성
// ─────────────────────────────────────────────
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const BASE_DIR = path.join(ROOT, '포폴 정리용');
const META_FILE = path.join(ROOT, 'data', 'portfolio-meta.json');
const OUT_FILE = path.join(ROOT, 'data', 'portfolio.json');

const ALLOWED_EXT = ['.pdf', '.pptx', '.ppt', '.xlsx', '.xls', '.csv', '.docx', '.doc', '.hwp', '.md', '.zip', '.html', '.png', '.jpg', '.mp4'];
// 하위 폴더 이름 → 종류 (게임은 파일로 올리지 않고 portfolio-meta.json 의 play.url 웹빌드로 연결)
const KIND_BY_FOLDER = { '기획서': 'plan', '데이터 테이블': 'data', '게임': 'game' };
const KIND_ORDER = ['game', 'career', 'plan', 'data', 'etc'];

function loadMeta() {
    try { return JSON.parse(fs.readFileSync(META_FILE, 'utf-8')); } catch (e) { return { projects: {}, docs: {} }; }
}

function formatSize(size) {
    return size > 1024 * 1024 ? (size / (1024 * 1024)).toFixed(1) + ' MB' : Math.max(1, Math.round(size / 1024)) + ' KB';
}

function autoTitle(name) {
    const ext = path.extname(name);
    return path.basename(name, ext)
        .replace(/^\d{4,8}[_\s-]*(\d+-\d+[_\s-]*)?/, '')   // 날짜/번호 접두어
        .replace(/[_\s]*\(\d+\)$/, '')                      // (1) 같은 복사본 표시
        .replace(/_?파송송계란탁|_?정승운/g, '')
        .replace(/_/g, ' ')
        .trim() || name;
}

function listFiles(dir) {
    try {
        return fs.readdirSync(dir, { withFileTypes: true })
            .filter(d => d.isFile() && !d.name.startsWith('.') && !d.name.startsWith('~$')
                && ALLOWED_EXT.includes(path.extname(d.name).toLowerCase()));
    } catch (e) { return []; }
}

function scanPortfolio() {
    const meta = loadMeta();
    let folders = [];
    try {
        folders = fs.readdirSync(BASE_DIR, { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name).sort((a, b) => a.localeCompare(b, 'ko'));
    } catch (e) { return { projects: [] }; }

    const projects = folders.map(folder => {
        const pm = meta.projects[folder] || meta.projects[folder.normalize('NFC')] || {};
        const projectTitle = pm.title || folder.replace(/^\d+_/, '');
        const docs = [];
        const add = (dirParts, entry, kind) => {
            const rel = ['포폴 정리용', folder, ...dirParts, entry.name].join('/');
            const stat = fs.statSync(path.join(BASE_DIR, folder, ...dirParts, entry.name));
            const dm = meta.docs[entry.name] || meta.docs[entry.name.normalize('NFC')] || {};
            docs.push({
                name: entry.name,
                path: rel,
                subfolder: dirParts.join('/'),
                kind,
                project: projectTitle,
                title: dm.title || autoTitle(entry.name),
                desc: dm.desc || `${path.extname(entry.name).replace('.', '').toUpperCase()} 원본 파일`,
                type: path.extname(entry.name).replace('.', '').toUpperCase(),
                sizeBytes: stat.size,
                sizeFormatted: formatSize(stat.size)
            });
        };
        // 프로젝트 폴더 바로 아래 파일 (공식 서류 등)
        listFiles(path.join(BASE_DIR, folder)).forEach(f => add([], f, pm.id === 'career' ? 'career' : 'etc'));
        // 하위 폴더 (기획서 / 데이터 테이블 / 게임 / 기타)
        try {
            fs.readdirSync(path.join(BASE_DIR, folder), { withFileTypes: true }).filter(d => d.isDirectory()).forEach(sub => {
                listFiles(path.join(BASE_DIR, folder, sub.name)).forEach(f => add([sub.name], f, KIND_BY_FOLDER[sub.name] || 'etc'));
            });
        } catch (e) {}
        const rank = k => { const i = KIND_ORDER.indexOf(k); return i < 0 ? 99 : i; };
        docs.sort((a, b) => rank(a.kind) - rank(b.kind) || a.name.localeCompare(b.name, 'ko'));
        return { id: pm.id || folder, folder, title: projectTitle, kicker: pm.kicker || '', desc: pm.desc || '', cover: pm.cover || '', play: pm.play || null, docs };
    }).filter(p => p.docs.length > 0);

    return { generatedAt: new Date().toISOString(), projects };
}

module.exports = { scanPortfolio };

if (require.main === module) {
    const data = scanPortfolio();
    fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
    fs.writeFileSync(OUT_FILE, JSON.stringify(data, null, 2), 'utf-8');
    const total = data.projects.reduce((n, p) => n + p.docs.length, 0);
    console.log(`portfolio.json 생성: 프로젝트 ${data.projects.length}개 · 파일 ${total}개`);
    data.projects.forEach(p => console.log(`  ${p.folder}: ${p.docs.length}개`));
}
