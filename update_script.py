# build_index.py - 정밀 삼각 파라미터 비율 맞춤 & IGDB 실시간 연동 강화

import os

with open('build_index.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the Triangle Radar SVG with mathematically exact points and percentage grid lines
old_radar_svg = '''                    <svg viewBox="0 0 340 310" width="320" height="290" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#9281f7" stop-opacity="0.6"/>
                                <stop offset="100%" stop-color="#705cf6" stop-opacity="0.25"/>
                            </linearGradient>
                            <filter id="radarGlow" x="-20%" y="-20%" width="140%" height="140%">
                                <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#9281f7" flood-opacity="0.6"/>
                            </filter>
                        </defs>

                        <!-- Guide Triangles (100%, 75%, 50%, 25%) Center: (170, 160), R=110 -->
                        <!-- 0° Top=(170, 50), 120° Bottom-Right=(265, 215), 240° Bottom-Left=(75, 215) -->
                        <polygon points="170,50 265,215 75,215" fill="none" stroke="#2a2e3d" stroke-width="1.5" />
                        <polygon points="170,77.5 241.25,201.25 98.75,201.25" fill="none" stroke="#1f2330" stroke-width="1" />
                        <polygon points="170,105 217.5,187.5 122.5,187.5" fill="none" stroke="#1f2330" stroke-width="1" />
                        <polygon points="170,132.5 193.75,173.75 146.25,173.75" fill="none" stroke="#1f2330" stroke-width="1" />

                        <!-- Axis Lines -->
                        <line x1="170" y1="160" x2="170" y2="50" stroke="#353b4d" stroke-width="1.5" stroke-dasharray="3,3"/>
                        <line x1="170" y1="160" x2="265" y2="215" stroke="#353b4d" stroke-width="1.5" stroke-dasharray="3,3"/>
                        <line x1="170" y1="160" x2="75" y2="215" stroke="#353b4d" stroke-width="1.5" stroke-dasharray="3,3"/>

                        <!-- User Radar Data Polygon (Simulation 55% / Management 30% / RPG 25%) -->
                        <!-- Scaled points: Top: 50+(160-50)*0.1 = 61, BR: 160+(215-160)*0.75=201, BL: 160+(215-160)*0.7=198 -->
                        <polygon points="170,62 248,205 92,203" fill="url(#polyGrad)" stroke="#9281f7" stroke-width="2.5" filter="url(#radarGlow)" />

                        <!-- Vertex Dots -->
                        <circle cx="170,62" r="5" fill="#fff" stroke="#9281f7" stroke-width="2"/>
                        <circle cx="248,205" r="5" fill="#fff" stroke="#9281f7" stroke-width="2"/>
                        <circle cx="92,203" r="5" fill="#fff" stroke="#9281f7" stroke-width="2"/>

                        <!-- Labels -->
                        <text x="170" y="32" fill="#ffffff" font-size="12.5" font-weight="700" text-anchor="middle" font-family="Pretendard">시뮬레이션 / 전략 (55%)</text>
                        <text x="275" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">경영 / 샌드박스 (30%)</text>
                        <text x="65" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">RPG / 내러티브 (25%)</text>
                    </svg>'''

new_radar_svg = '''                    <svg viewBox="0 0 360 320" width="340" height="300" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#9281f7" stop-opacity="0.65"/>
                                <stop offset="100%" stop-color="#6452f0" stop-opacity="0.25"/>
                            </linearGradient>
                            <filter id="radarGlow" x="-20%" y="-20%" width="140%" height="140%">
                                <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#9281f7" flood-opacity="0.75"/>
                            </filter>
                        </defs>

                        <!-- 수학적 중심점: (180, 160), 최대 반경 R = 100 -->
                        <!-- 100% 가이드 정삼각형: Top(180, 60), BR(266.6, 210), BL(93.4, 210) -->
                        <polygon points="180,60 266.6,210 93.4,210" fill="none" stroke="#373c4e" stroke-width="1.5" />
                        <!-- 75% 가이드: Top(180, 85), BR(245, 197.5), BL(115, 197.5) -->
                        <polygon points="180,85 245,197.5 115,197.5" fill="none" stroke="#252937" stroke-width="1" />
                        <!-- 50% 가이드: Top(180, 110), BR(223.3, 185), BL(136.7, 185) -->
                        <polygon points="180,110 223.3,185 136.7,185" fill="none" stroke="#252937" stroke-width="1" stroke-dasharray="2,2" />
                        <!-- 25% 가이드: Top(180, 135), BR(201.7, 172.5), BL(158.3, 172.5) -->
                        <polygon points="180,135 201.7,172.5 158.3,172.5" fill="none" stroke="#252937" stroke-width="1" stroke-dasharray="2,2" />

                        <!-- 중심 축선 (Center to Vertices) -->
                        <line x1="180" y1="160" x2="180" y2="60" stroke="#484f66" stroke-width="1.5" stroke-dasharray="3,3"/>
                        <line x1="180" y1="160" x2="266.6" y2="210" stroke="#484f66" stroke-width="1.5" stroke-dasharray="3,3"/>
                        <line x1="180" y1="160" x2="93.4" y2="210" stroke="#484f66" stroke-width="1.5" stroke-dasharray="3,3"/>

                        <!-- 정밀 눈금 라벨 (50%, 100%) -->
                        <text x="184" y="112" fill="#71768a" font-size="9" font-family="Commit Mono">50%</text>
                        <text x="184" y="65" fill="#9281f7" font-size="9" font-family="Commit Mono">100%</text>
                        <text x="184" y="137" fill="#585c6c" font-size="8.5" font-family="Commit Mono">25%</text>

                        <!-- [수학적 정확 비율 적용 데이터 폴리곤] -->
                        <!-- 1. 시뮬레이션/전략 55%: y = 160 - (100 * 0.55) = 105 -> (180, 105) (50% 라인인 110 바로 위) -->
                        <!-- 2. 경영/샌드박스 30%: x = 180 + (100 * 0.30 * 0.866) = 206, y = 160 + (100 * 0.30 * 0.5) = 175 -> (206, 175) (25% 라인 바로 바깥) -->
                        <!-- 3. RPG/내러티브 25%: x = 180 - (100 * 0.25 * 0.866) = 158.3, y = 160 + (100 * 0.25 * 0.5) = 172.5 -> (158.3, 172.5) (25% 라인 정확히 일치) -->
                        <polygon points="180,105 206,175 158.3,172.5" fill="url(#polyGrad)" stroke="#9281f7" stroke-width="2.5" filter="url(#radarGlow)" />

                        <!-- 꼭짓점 데이터 마커 및 수치 태그 -->
                        <circle cx="180" cy="105" r="5" fill="#fff" stroke="#9281f7" stroke-width="2.5"/>
                        <circle cx="206" cy="175" r="5" fill="#fff" stroke="#9281f7" stroke-width="2.5"/>
                        <circle cx="158.3" cy="172.5" r="5" fill="#fff" stroke="#9281f7" stroke-width="2.5"/>

                        <!-- 정밀 장르 라벨 -->
                        <text x="180" y="38" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle" font-family="Pretendard">시뮬레이션 / 전략 (55%)</text>
                        <text x="282" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">경영 / 샌드박스 (30%)</text>
                        <text x="78" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">RPG / 내러티브 (25%)</text>
                    </svg>'''

if old_radar_svg in text:
    text = text.replace(old_radar_svg, new_radar_svg)
    print("Radar SVG replaced with mathematically exact scale!")
else:
    print("Warning: old_radar_svg exact string not found, will do substring replace")

# 2. Update the Search Modal to show live status badge and quick suggestion tags
old_search_modal_body = '''            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h3 style="color:#fff; font-size:18px;">🎮 IGDB 실시간 게임 데이터베이스 검색</h3>
                <button onclick="closeGameSearchModal()" style="background:transparent; border:none; color:var(--color-ash-gray); font-size:18px; cursor:pointer;">✕</button>
            </div>
            
            <div style="display:flex; gap:10px; margin-bottom:20px;">
                <input type="text" id="gameQueryInput" placeholder="게임 이름 입력 (예: 문명, 림월드, 젤다, 마리오, Zelda, Mario)" style="flex:1; background:#141722; border:1px solid var(--color-graphite-hairline); border-radius:8px; padding:12px 16px; color:#fff; font-size:14px; outline:none;" onkeyup="if(event.key==='Enter') executeGameSearch()" />
                <button onclick="executeGameSearch()" class="btn-ghost" style="background:var(--color-iris-violet); color:#fff; border-color:var(--color-iris-violet); padding:0 20px; font-weight:600;">검색</button>
            </div>

            <div id="gameSearchResults" style="max-height:420px; overflow-y:auto; border:1px solid var(--color-graphite-hairline); border-radius:10px; background:#07080c;">
                <div style="color:var(--color-ash-gray); text-align:center; padding:36px; font-size:13.5px;">한글 또는 영문 게임명을 입력하시면 IGDB 공식 데이터베이스에서 실시간으로 검색합니다.</div>
            </div>'''

new_search_modal_body = '''            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <h3 style="color:#fff; font-size:18px;">🎮 IGDB 실시간 게임 데이터베이스 검색</h3>
                    <span id="igdbLiveBadge" style="display:inline-flex; align-items:center; gap:6px; font-size:11px; font-family:var(--font-mono); color:#4ade80; background:rgba(74,222,128,0.12); padding:3px 10px; border-radius:12px; border:1px solid rgba(74,222,128,0.3);">
                        <span style="width:7px; height:7px; border-radius:50%; background:#4ade80; box-shadow:0 0 8px #4ade80;"></span>
                        LIVE CONNECTED
                    </span>
                </div>
                <button onclick="closeGameSearchModal()" style="background:transparent; border:none; color:var(--color-ash-gray); font-size:18px; cursor:pointer;">✕</button>
            </div>

            <!-- 빠른 검색 추천 키워드 태그 -->
            <div style="display:flex; gap:8px; margin-bottom:14px; flex-wrap:wrap; align-items:center;">
                <span style="font-size:12px; color:var(--color-ash-gray); font-family:var(--font-mono);">추천 검색:</span>
                <button type="button" class="btn-ghost" style="padding:3px 10px; font-size:11.5px;" onclick="quickSearchTag('Civilization VI')">문명 6</button>
                <button type="button" class="btn-ghost" style="padding:3px 10px; font-size:11.5px;" onclick="quickSearchTag('RimWorld')">림월드</button>
                <button type="button" class="btn-ghost" style="padding:3px 10px; font-size:11.5px;" onclick="quickSearchTag('Football Manager 2024')">FM 2024</button>
                <button type="button" class="btn-ghost" style="padding:3px 10px; font-size:11.5px;" onclick="quickSearchTag('Zelda')">젤다의 전설</button>
                <button type="button" class="btn-ghost" style="padding:3px 10px; font-size:11.5px;" onclick="quickSearchTag('Mario')">마리오</button>
                <button type="button" class="btn-ghost" style="padding:3px 10px; font-size:11.5px;" onclick="quickSearchTag('Cyberpunk 2077')">사이버펑크</button>
            </div>
            
            <div style="display:flex; gap:10px; margin-bottom:18px;">
                <input type="text" id="gameQueryInput" placeholder="게임 이름 입력 (예: 문명, 림월드, 젤다, 마리오, Zelda, Mario)" style="flex:1; background:#141722; border:1px solid var(--color-graphite-hairline); border-radius:8px; padding:12px 16px; color:#fff; font-size:14px; outline:none;" oninput="handleGameInputDebounce()" onkeyup="if(event.key==='Enter') executeGameSearch()" />
                <button onclick="executeGameSearch()" class="btn-ghost" style="background:var(--color-iris-violet); color:#fff; border-color:var(--color-iris-violet); padding:0 22px; font-weight:600;">검색</button>
            </div>

            <div id="gameSearchResults" style="max-height:420px; overflow-y:auto; border:1px solid var(--color-graphite-hairline); border-radius:10px; background:#07080c;">
                <div style="color:var(--color-ash-gray); text-align:center; padding:36px; font-size:13.5px;">⏳ 게임 목록을 불러오는 중입니다...</div>
            </div>'''

if old_search_modal_body in text:
    text = text.replace(old_search_modal_body, new_search_modal_body)
    print("Search modal UI updated with live badge & tags!")

# 3. Update the JavaScript functions for IGDB search to:
# - Use relative URL first (`/api/search-games?q=...`)
# - Load initial popular games automatically upon opening modal
# - Debounce live search on typing
old_script_search = '''        /* -------------------------------------------------------------
           IGDB 실시간 게임 검색 모달
        ------------------------------------------------------------- */
        function openGameSearchModal() {
            document.getElementById('gameSearchModal').style.display = 'block';
            document.getElementById('gameQueryInput').focus();
        }

        function closeGameSearchModal() {
            document.getElementById('gameSearchModal').style.display = 'none';
        }

        async function executeGameSearch() {
            const query = document.getElementById('gameQueryInput').value.trim();
            const container = document.getElementById('gameSearchResults');
            if (!query) {
                alert('검색어를 입력해주세요.');
                return;
            }

            container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;"><span style="font-size:24px;">⏳</span><br>IGDB 공식 데이터베이스에서 검색 중입니다...</div>';

            try {
                const res = await fetch(`${API_BASE}/api/search-games?q=${encodeURIComponent(query)}`);
                if (!res.ok) {
                    const errJson = await res.json().catch(() => ({}));
                    throw new Error(errJson.error || '서버 응답 오류');
                }
                const games = await res.json();

                if (!games || games.length === 0) {
                    container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;">검색 결과가 없습니다. 다른 게임명을 입력해보세요.</div>';
                    return;
                }

                container.innerHTML = '';
                games.forEach(game => {
                    const row = document.createElement('div');
                    row.style.cssText = 'display:flex; align-items:center; gap:14px; padding:12px 16px; border-bottom:1px solid var(--color-graphite-hairline); cursor:pointer; transition:background 0.2s;';
                    row.onmouseover = () => row.style.background = 'rgba(146,129,247,0.08)';
                    row.onmouseout = () => row.style.background = '';

                    const imgHtml = game.coverUrl 
                        ? `<img src="${game.coverUrl}" style="width:45px; height:60px; object-fit:cover; border-radius:6px; border:1px solid var(--color-graphite-hairline);" />`
                        : `<div style="width:45px; height:60px; background:#1a1c24; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:10px; color:#888;">NO IMG</div>`;

                    row.innerHTML = `
                        ${imgHtml}
                        <div style="flex:1; min-width:0;">
                            <div style="font-weight:600; color:#fff; font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                ${game.title} ${game.releaseYear ? `(${game.releaseYear})` : ''}
                            </div>
                            <div style="font-size:11px; color:var(--color-ash-gray); font-family:var(--font-mono); margin-top:2px;">
                                플랫폼: ${game.platform} | 장르: ${game.genre}
                            </div>
                        </div>
                        <button class="btn-ghost" style="padding:6px 14px; font-size:12px;" onclick="addGameToGrid(${JSON.stringify(game).replace(/"/g, '&quot;')})">히스토리 추가 +</button>
                    `;
                    container.appendChild(row);
                });

            } catch(e) {
                container.innerHTML = `<div style="color:#ff6b6b; text-align:center; padding:30px;">⚠️ 검색 오류: ${e.message}<br><small style="color:var(--color-ash-gray);">서버 상태: ${API_BASE}</small></div>`;
            }
        }'''

new_script_search = '''        /* -------------------------------------------------------------
           IGDB 실시간 게임 검색 모달 & 무중단 통신
        ------------------------------------------------------------- */
        let searchDebounceTimer = null;
        let isInitialGamesLoaded = false;

        function getApiUrl(endpoint) {
            // 현재 호스트가 웹서버(http/https)면 상대 경로를 써서 CORS/포트 불일치 원천 차단
            if (window.location.protocol.startsWith('http')) {
                return endpoint;
            }
            // file:// 프로토콜일 때는 localhost:3000 명시
            return 'http://localhost:3000' + endpoint;
        }

        function openGameSearchModal() {
            document.getElementById('gameSearchModal').style.display = 'block';
            document.getElementById('gameQueryInput').focus();
            
            // 모달 열 때 실시간 서버 연결 체크 및 추천 인기 게임 자동 표시
            checkServerHealth();
            if (!isInitialGamesLoaded) {
                loadInitialPopularGames();
            }
        }

        function closeGameSearchModal() {
            document.getElementById('gameSearchModal').style.display = 'none';
        }

        async function checkServerHealth() {
            const badge = document.getElementById('igdbLiveBadge');
            try {
                const res = await fetch(getApiUrl('/api/health'), { timeout: 3000 });
                if (res.ok) {
                    badge.innerHTML = '<span style="width:7px; height:7px; border-radius:50%; background:#4ade80; box-shadow:0 0 8px #4ade80;"></span>LIVE CONNECTED';
                    badge.style.color = '#4ade80';
                    badge.style.borderColor = 'rgba(74,222,128,0.3)';
                } else {
                    throw new Error('Server not ready');
                }
            } catch(e) {
                badge.innerHTML = '<span style="width:7px; height:7px; border-radius:50%; background:#f87171; box-shadow:0 0 8px #f87171;"></span>CONNECTING...';
                badge.style.color = '#f87171';
                badge.style.borderColor = 'rgba(248,113,113,0.3)';
            }
        }

        async function loadInitialPopularGames() {
            const container = document.getElementById('gameSearchResults');
            container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;"><span style="font-size:24px;">⏳</span><br>IGDB 공식 데이터베이스에서 추천 게임을 동기화 중입니다...</div>';
            
            try {
                const res = await fetch(getApiUrl('/api/search-games?q=Civilization'));
                if (res.ok) {
                    const games = await res.json();
                    renderGameSearchResults(games);
                    isInitialGamesLoaded = true;
                }
            } catch(e) {
                container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;">검색할 게임명을 입력하세요.</div>';
            }
        }

        function quickSearchTag(keyword) {
            document.getElementById('gameQueryInput').value = keyword;
            executeGameSearch();
        }

        function handleGameInputDebounce() {
            if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(() => {
                const query = document.getElementById('gameQueryInput').value.trim();
                if (query.length >= 2) {
                    executeGameSearch();
                }
            }, 350); // 0.35초 디바운스 실시간 검색
        }

        async function executeGameSearch() {
            const query = document.getElementById('gameQueryInput').value.trim();
            const container = document.getElementById('gameSearchResults');
            if (!query) {
                alert('검색어를 입력해주세요.');
                return;
            }

            container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;"><span style="font-size:24px;">⏳</span><br>IGDB 공식 데이터베이스에서 <strong>"' + query + '"</strong> 검색 중...</div>';

            try {
                const res = await fetch(getApiUrl('/api/search-games?q=' + encodeURIComponent(query)));
                if (!res.ok) {
                    const errJson = await res.json().catch(() => ({}));
                    throw new Error(errJson.error || ('서버 응답 오류: ' + res.status));
                }
                const games = await res.json();

                if (!games || games.length === 0) {
                    container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;">🔍 <strong>"' + query + '"</strong>에 대한 검색 결과가 없습니다.<br><small style="color:#71768a;">다른 게임명을 입력해보세요.</small></div>';
                    return;
                }

                renderGameSearchResults(games);

            } catch(e) {
                console.error('IGDB 검색 에러:', e);
                container.innerHTML = `<div style="color:#ff6b6b; text-align:center; padding:30px;">⚠️ IGDB 검색 실패: ${e.message}<br><small style="color:var(--color-ash-gray);">서버 주소: ${getApiUrl('/api/search-games')}</small></div>`;
            }
        }

        function renderGameSearchResults(games) {
            const container = document.getElementById('gameSearchResults');
            container.innerHTML = '';
            games.forEach(game => {
                const row = document.createElement('div');
                row.style.cssText = 'display:flex; align-items:center; gap:14px; padding:12px 16px; border-bottom:1px solid var(--color-graphite-hairline); cursor:pointer; transition:background 0.2s;';
                row.onmouseover = () => row.style.background = 'rgba(146,129,247,0.08)';
                row.onmouseout = () => row.style.background = '';

                const imgHtml = game.coverUrl 
                    ? `<img src="${game.coverUrl}" style="width:45px; height:60px; object-fit:cover; border-radius:6px; border:1px solid var(--color-graphite-hairline);" />`
                    : `<div style="width:45px; height:60px; background:#1a1c24; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:10px; color:#888;">NO IMG</div>`;

                // 안전한 게임 추가 버튼 (이벤트 리스너 직접 바인딩으로 따옴표 이스케이프 오류 방지)
                const addBtn = document.createElement('button');
                addBtn.className = 'btn-ghost';
                addBtn.style.cssText = 'padding:6px 14px; font-size:12px; flex-shrink:0;';
                addBtn.innerText = '히스토리 추가 +';
                addBtn.onclick = (e) => {
                    e.stopPropagation();
                    addGameToGrid(game);
                };

                const infoCol = document.createElement('div');
                infoCol.style.cssText = 'flex:1; min-width:0;';
                infoCol.innerHTML = `
                    <div style="font-weight:600; color:#fff; font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                        ${game.title} ${game.releaseYear ? `(${game.releaseYear})` : ''}
                    </div>
                    <div style="font-size:11px; color:var(--color-ash-gray); font-family:var(--font-mono); margin-top:2px;">
                        플랫폼: ${game.platform} | 장르: ${game.genre}
                    </div>
                `;

                row.innerHTML = imgHtml;
                row.appendChild(infoCol);
                row.appendChild(addBtn);
                container.appendChild(row);
            });
        }'''

if old_script_search in text:
    text = text.replace(old_script_search, new_script_search)
    print("Search script updated with auto-loading, debounce & relative endpoint!")

with open('build_index.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_index.py updated successfully!")
