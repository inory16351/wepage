# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS에 step-banner 관련 스타일 보강 (이미지 잘림 없는 contain 처리)
css_to_add = """
        /* Step Banner Wrap for main 1 and main 2 */
        .step-banner-wrap {
            width: 100%;
            margin-bottom: 24px;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--color-graphite-hairline);
            background: #060709;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
        }
        .step-banner-img {
            width: 100%;
            height: auto;
            max-height: 420px;
            object-fit: contain;
            display: block;
            transition: transform 0.4s ease;
        }
        .step-banner-wrap:hover .step-banner-img {
            transform: scale(1.015);
        }
"""

if '.step-banner-wrap' not in html:
    html = html.replace('</style>', css_to_add + '\n    </style>')

# 새롭게 복구 및 강화된 page-main 섹션
new_page_main = """        <!-- 1. 메인 페이지 (클릭 순환 3단계 소개 구성) -->
        <section id="page-main" class="page-section active">
            
            <!-- Step 1: 메인 인트로, main 1.png 배너 및 핵심 로그라인 -->
            <div class="main-step-container active" id="main-step-1" onclick="handleStepClick(2)">
                <div style="padding: 10px 0 20px;">
                    <!-- 메인 로비 비주얼 배너 (main 1.png 완벽 비율 연동) -->
                    <div class="step-banner-wrap">
                        <img src="main 1.png" alt="정승운 크리에이터 메인 비주얼" class="step-banner-img" onerror="this.style.display='none'">
                    </div>

                    <div class="hero-logline" contenteditable="false">
                        탄탄한 논리로 상상하는 <br><span>크리에이터 정승운</span>
                    </div>
                    <div class="hero-sub" contenteditable="false">
                        스토리보드와 시스템 기획, 유니티 바이브 코딩과 데이터 테이블 밸런싱까지.<br>
                        창작물의 핵심 뼈대를 구축하고 유저가 몰입할 수 있는 세계를 설계합니다.
                    </div>
                    <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                        <button class="btn-primary" onclick="event.stopPropagation(); switchPage('portfolio', document.querySelectorAll('nav button')[2])">
                            포트폴리오 & 기획서 보러가기 →
                        </button>
                        <button class="btn-ghost" onclick="event.stopPropagation(); switchPage('resume', document.querySelectorAll('nav button')[1])">
                            이력 및 경력 확인
                        </button>
                        <button class="btn-ghost" onclick="event.stopPropagation(); handleStepClick(2)" style="border-color:var(--color-iris-violet); color:var(--color-iris-violet);">
                            다음 소개 보기 (STEP 2) →
                        </button>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">STEP 01 / 03 [인트로 & 비전]</span>
                    <span>화면의 빈 공간을 클릭하면 [핵심 역량]으로 이동합니다 →</span>
                </div>
            </div>

            <!-- Step 2: 핵심 강점 (main 2 이미지 및 3대 핵심 역량) -->
            <div class="main-step-container" id="main-step-2" onclick="handleStepClick(3)">
                <div style="padding: 10px 0 20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                        <div>
                            <span class="live-search-badge" style="font-size:11px;">CORE COMPETENCE</span>
                            <h2 class="section-title" style="font-size:28px; margin:4px 0 0;">핵심 역량 및 강점</h2>
                        </div>
                        <div style="display:flex; gap:8px;">
                            <button class="home-shortcut-btn" onclick="event.stopPropagation(); handleStepClick(1)">← 이전 (STEP 1)</button>
                            <button class="btn-ghost" onclick="event.stopPropagation(); handleStepClick(3)" style="border-color:var(--color-iris-violet); color:var(--color-iris-violet);">다음 소개 (STEP 3) →</button>
                        </div>
                    </div>
                    <p class="section-desc" style="margin-bottom:20px;">논리적 시스템 기획과 창의적인 세계관 구성, 디테일한 수치 밸런싱을 아우릅니다.</p>

                    <!-- main 2 이미지 배너 완벽 비율 연동 -->
                    <div class="step-banner-wrap" style="max-height:340px; margin-bottom:28px;">
                        <img src="main2.png" alt="핵심 역량 시스템 큐브 아키텍처" class="step-banner-img" style="max-height:340px;" onerror="this.style.display='none'">
                    </div>

                    <div class="grid-3">
                        <div class="card-custom">
                            <div class="card-title" contenteditable="false">01. 시스템 설계 & 논리 구조</div>
                            <div class="card-desc" contenteditable="false">
                                AI 행동 트리(Behavior Tree) 구조 분리 및 상태 머신(FSM) 설계. 예외 상황을 원천 차단하고 시스템 간 상호작용을 정밀하게 기획합니다.
                            </div>
                        </div>
                        <div class="card-custom">
                            <div class="card-title" contenteditable="false">02. 데이터 테이블 & 밸런싱</div>
                            <div class="card-desc" contenteditable="false">
                                재배/제조/무역소/캐릭터 테이블을 직접 구조화하고 경제 순환 사이클과 시간 가치, 성장 곡선 밸런스 패치를 수행합니다.
                            </div>
                        </div>
                        <div class="card-custom">
                            <div class="card-title" contenteditable="false">03. 협업 총괄 & 프로덕션</div>
                            <div class="card-desc" contenteditable="false">
                                팀장 및 프로젝트 PD로서 일정 마일스톤 관리, QA 체크리스트 운용, 기획/아트/클라 간 명확한 커뮤니케이션으로 완성도를 극대화합니다.
                            </div>
                        </div>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">STEP 02 / 03 [핵심 역량]</span>
                    <span>화면을 클릭하면 [하이라이트 요약]으로 이동합니다 →</span>
                </div>
            </div>

            <!-- Step 3: 하이라이트 요약 (플레이 히스토리 & 대표 프로젝트) -->
            <div class="main-step-container" id="main-step-3" onclick="handleStepClick(1)">
                <div style="padding: 10px 0 20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:10px;">
                        <div>
                            <span class="live-search-badge" style="font-size:11px;">PORTFOLIO HIGHLIGHT</span>
                            <h2 class="section-title" style="font-size:28px; margin:4px 0 0;">하이라이트 요약</h2>
                        </div>
                        <div style="display:flex; gap:8px;">
                            <button class="home-shortcut-btn" onclick="event.stopPropagation(); handleStepClick(2)">← 이전 (STEP 2)</button>
                            <button class="btn-ghost" onclick="event.stopPropagation(); handleStepClick(1)">처음으로 ↺</button>
                        </div>
                    </div>
                    <p class="section-desc" style="margin-bottom:24px;">플레이 히스토리와 대표 프로젝트의 핵심 컴포넌트입니다.</p>

                    <!-- 컴포넌트 1: 플레이 히스토리 요약 (IGDB 포스터 비율 3:4 완벽 적용) -->
                    <div class="component-block">
                        <div class="component-header">
                            <span class="component-title">플레이 히스토리 하이라이트</span>
                            <div style="display:flex; gap:8px;">
                                <button class="btn-ghost disabled" id="mainAddGameBtn" onclick="event.stopPropagation(); openGameSearchModal()">+ 게임 검색 추가 (편집모드)</button>
                                <button class="btn-ghost" onclick="event.stopPropagation(); switchPage('playhistory', document.querySelectorAll('nav button')[3])">전체 보기 ></button>
                            </div>
                        </div>
                        <div class="play-grid" id="main-play-grid">
                            <div class="play-card">
                                <div class="play-thumb">
                                    <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqr.jpg" alt="Sid Meier's Civilization VI">
                                </div>
                                <div class="play-content">
                                    <div class="play-title" contenteditable="false">Sid Meier's Civilization VI</div>
                                    <div class="play-meta">
                                        <div class="play-meta-row"><span>플랫폼: PC</span><span>1,200h+</span></div>
                                        <div>장르: Strategy / Simulation</div>
                                    </div>
                                </div>
                            </div>
                            <div class="play-card">
                                <div class="play-thumb">
                                    <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co73z1.jpg" alt="Football Manager 2024">
                                </div>
                                <div class="play-content">
                                    <div class="play-title" contenteditable="false">Football Manager 2024</div>
                                    <div class="play-meta">
                                        <div class="play-meta-row"><span>플랫폼: PC</span><span>950h+</span></div>
                                        <div>장르: Sports / Simulation</div>
                                    </div>
                                </div>
                            </div>
                            <div class="play-card">
                                <div class="play-thumb">
                                    <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqj.jpg" alt="RimWorld">
                                </div>
                                <div class="play-content">
                                    <div class="play-title" contenteditable="false">RimWorld</div>
                                    <div class="play-meta">
                                        <div class="play-meta-row"><span>플랫폼: PC</span><span>800h+</span></div>
                                        <div>장르: Simulation / Survival</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 컴포넌트 2: 대표 프로젝트 요약 (이미지 잘림 없는 contain 박스 적용) -->
                    <div class="component-block" style="margin-bottom:0;">
                        <div class="component-header">
                            <span class="component-title">대표 프로젝트 하이라이트</span>
                            <button class="btn-ghost" onclick="event.stopPropagation(); switchPage('portfolio', document.querySelectorAll('nav button')[2])">전체 포트폴리오 ></button>
                        </div>
                        <div class="main-project-grid">
                            <div class="main-project-card" onclick="event.stopPropagation(); openModal('project1')">
                                <div class="main-project-imgbox">
                                    <img src="lastsanctuary.png" alt="LAST SANCTUARY">
                                </div>
                                <div style="padding:18px 20px;">
                                    <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); margin-bottom:4px;">PC RPG • SYSTEM PLANNING</div>
                                    <div class="project-title" style="font-size:17px; margin-bottom:6px;" contenteditable="false">PC 게임 &lt;LAST SANCTUARY&gt;</div>
                                    <div class="project-desc" style="font-size:13px; margin:0;" contenteditable="false">전체 게임 시스템 기획, AI 행동 트리 로직 설계, 유니티 바이브 코딩 및 PV 제작</div>
                                </div>
                            </div>
                            <div class="main-project-card" onclick="event.stopPropagation(); openModal('project2')">
                                <div class="main-project-imgbox">
                                    <img src="슬기로운재배생활.png" alt="슬기로운 재배생활">
                                </div>
                                <div style="padding:18px 20px;">
                                    <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); margin-bottom:4px;">PC SIMULATION • TEAM LEAD</div>
                                    <div class="project-title" style="font-size:17px; margin-bottom:6px;" contenteditable="false">PC 게임 &lt;슬기로운 재배생활&gt;</div>
                                    <div class="project-desc" style="font-size:13px; margin:0;" contenteditable="false">팀장 총괄, 재배/가공/무역 시스템 설계, 5종 데이터 테이블 및 경제 밸런스 패치</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">STEP 03 / 03 [포트폴리오 요약]</span>
                    <span>클릭 시 [처음 (STEP 1)]으로 순환 이동합니다 ↺</span>
                </div>
            </div>

        </section>"""

# 기존 <section id="page-main" ... </section> 교체
pos_start = html.find('<section id="page-main"')
pos_end = html.find('</section>', pos_start) + len('</section>')

if pos_start != -1 and pos_end != -1:
    updated_html = html[:pos_start] + new_page_main + html[pos_end:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print("Successfully updated page-main with main 1.png and main2.png!")
else:
    print("Could not find section id=page-main in index.html")
