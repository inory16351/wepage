# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS 스타일 정의: 메인 이미지 빈 공간에 텍스트 오버레이 배치 & 글래스모피즘
css_overlay = """
        /* Hero Canvas & Overlay Styles (빈 공간 텍스트 배치) */
        .hero-canvas-step1 {
            width: 100%;
            min-height: 580px;
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--color-graphite-hairline);
            background-color: #030406;
            background-image: url('main 1.png');
            background-repeat: no-repeat;
            background-position: right center;
            background-size: contain;
            display: flex;
            align-items: center;
            padding: 50px 60px;
            position: relative;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
            cursor: pointer;
            transition: border-color 0.3s ease;
        }

        .hero-canvas-step1:hover {
            border-color: rgba(146, 129, 247, 0.4);
        }

        /* 좌측 50% 어두운 빈 공간에 텍스트 완벽 배치 */
        .hero-text-overlay {
            max-width: 520px;
            z-index: 2;
        }

        .hero-canvas-step2 {
            width: 100%;
            min-height: 580px;
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--color-graphite-hairline);
            background-color: #030406;
            background-image: url('main2.png');
            background-repeat: no-repeat;
            background-position: center center;
            background-size: cover;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 44px 50px 36px;
            position: relative;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
            cursor: pointer;
            transition: border-color 0.3s ease;
        }

        .hero-canvas-step2:hover {
            border-color: rgba(146, 129, 247, 0.4);
        }

        /* Step 2 글래스 카드 */
        .card-glass {
            background: rgba(8, 9, 14, 0.75);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(146, 129, 247, 0.25);
            border-radius: 14px;
            padding: 22px;
            transition: all 0.25s ease;
        }

        .card-glass:hover {
            border-color: var(--color-iris-violet);
            background: rgba(14, 15, 24, 0.85);
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(146, 129, 247, 0.15);
        }

        @media (max-width: 900px) {
            .hero-canvas-step1 {
                background-position: center bottom;
                background-size: cover;
                padding: 30px 24px;
                min-height: 500px;
                align-items: flex-start;
            }
            .hero-text-overlay {
                max-width: 100%;
                background: rgba(0, 0, 0, 0.6);
                padding: 20px;
                border-radius: 12px;
            }
            .hero-canvas-step2 {
                padding: 30px 20px;
                background-size: cover;
            }
        }
"""

# 기존 CSS 뒤에 추가
if '.hero-canvas-step1' not in html:
    html = html.replace('</style>', css_overlay + '\n    </style>')

# 새로운 메인 섹션:
# 1. Step 1: main 1.png 배경, 좌측 빈 공간에 로그라인만 배치 (버튼 일체 삭제)
# 2. Step 2: main2.png 배경, 상단/하단 빈 공간에 3대 핵심 역량 배치
# 3. 대표 프로젝트 & 플레이 히스토리는 메인에서 완전 분리 (상단 메뉴 전용 페이지로)
new_page_main = """        <!-- 1. 메인 페이지 (간결한 2단계 소개 구성 / 대표 프로젝트·플레이 히스토리는 독립 페이지로 분리) -->
        <section id="page-main" class="page-section active">
            
            <!-- Step 1: main 1.png의 좌측 빈 공간에 로그라인만 심플하게 배치 -->
            <div class="main-step-container active" id="main-step-1" onclick="handleStepClick(2)">
                <div class="hero-canvas-step1">
                    <div class="hero-text-overlay">
                        <div class="hero-logline" style="margin-bottom:18px;" contenteditable="false">
                            탄탄한 논리로 상상하는 <br><span>크리에이터 정승운</span>
                        </div>
                        <div class="hero-sub" style="margin-bottom:0;" contenteditable="false">
                            스토리보드와 시스템 기획, 유니티 바이브 코딩과 데이터 테이블 밸런싱까지.<br>
                            창작물의 핵심 뼈대를 구축하고 유저가 몰입할 수 있는 세계를 설계합니다.
                        </div>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">01 / 02 [비전 & 로그라인]</span>
                    <span>화면을 클릭하면 [핵심 역량 소개]로 전환됩니다 →</span>
                </div>
            </div>

            <!-- Step 2: main2.png의 빈 공간에 3대 핵심 역량 카드 배치 -->
            <div class="main-step-container" id="main-step-2" onclick="handleStepClick(1)">
                <div class="hero-canvas-step2">
                    <div>
                        <span class="live-search-badge" style="font-size:11px; margin-bottom:8px;">CORE COMPETENCE</span>
                        <h2 class="section-title" style="font-size:28px; margin:0 0 6px;">핵심 역량 및 강점</h2>
                        <p class="section-desc" style="margin-bottom:0; font-size:14px;">논리적 시스템 기획과 창의적인 세계관 구성, 디테일한 수치 밸런싱을 아우릅니다.</p>
                    </div>

                    <div class="grid-3" style="margin-top:28px; margin-bottom:0;">
                        <div class="card-glass">
                            <div class="card-title" style="font-size:16px; margin-bottom:8px;" contenteditable="false">01. 시스템 설계 & 논리 구조</div>
                            <div class="card-desc" style="font-size:13px; line-height:1.6;" contenteditable="false">
                                AI 행동 트리(Behavior Tree) 구조 분리 및 상태 머신(FSM) 설계. 예외 상황을 원천 차단하고 시스템 간 상호작용을 정밀하게 기획합니다.
                            </div>
                        </div>
                        <div class="card-glass">
                            <div class="card-title" style="font-size:16px; margin-bottom:8px;" contenteditable="false">02. 데이터 테이블 & 밸런싱</div>
                            <div class="card-desc" style="font-size:13px; line-height:1.6;" contenteditable="false">
                                재배/제조/무역소/캐릭터 테이블을 직접 구조화하고 경제 순환 사이클과 시간 가치, 성장 곡선 밸런스 패치를 수행합니다.
                            </div>
                        </div>
                        <div class="card-glass">
                            <div class="card-title" style="font-size:16px; margin-bottom:8px;" contenteditable="false">03. 협업 총괄 & 프로덕션</div>
                            <div class="card-desc" style="font-size:13px; line-height:1.6;" contenteditable="false">
                                팀장 및 프로젝트 PD로서 일정 마일스톤 관리, QA 체크리스트 운용, 기획/아트/클라 간 명확한 커뮤니케이션으로 완성도를 극대화합니다.
                            </div>
                        </div>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">02 / 02 [핵심 역량]</span>
                    <span>화면을 클릭하면 [메인 첫 화면]으로 돌아갑니다 ↺</span>
                </div>
            </div>

        </section>"""

# index.html의 page-main 교체
pos_start = html.find('<section id="page-main"')
pos_end = html.find('</section>', pos_start) + len('</section>')

if pos_start != -1 and pos_end != -1:
    updated_html = html[:pos_start] + new_page_main + html[pos_end:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print("Successfully updated index.html with overlay text and separated sections!")
else:
    print("Could not find section id=page-main")
