"""Fix Stage 3 to use proper 2-column grid layout in one slide"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the exact stage 3 block and replace it
old_block = '''        <!-- [STAGE 3] 데블다이스 – LAST SANCTUARY (단독 풀 페이지) -->
        <div class="showcase-stage" id="resumeStage3">
                    <div class="project-show-card">
                        <img src="lastsanctuary.png" alt="LAST SANCTUARY" class="project-show-img">
                        <div class="project-show-body">
                            <div class="project-company-badge">
                                <img src="logo_devildice.png" alt="데블다이스 로고">
                                <span style="font-size:12px; color:var(--color-ash-gray); font-family:var(--font-mono);">데블다이스 (2023 - 2024)</span>
                            </div>
                            <div class="project-show-title">LAST SANCTUARY (라스트 생츄어리)</div>
                            <div class="project-show-desc">
                                포스트 아포칼립스 세계관 기반의 <strong>생존 기지 건설 &amp; 디펜스 시뮬레이션</strong>.<br>
                                • 자원 채집/정제/소모 3단계 순환 경제 및 타일 기반 기지 건설 메카닉 설계.<br>
                                • 몬스터 웨이브 주기 및 방어 타워 사거리/DPS 정밀 밸런싱 시트 구축.
                            </div>
                        </div>
                    </div>

                    <!-- 제임스텍 / 슬기로운 재배생활 -->
                    <div class="project-show-card">
                        <img src="슬기로운재배생활.png" alt="슬기로운 재배생활" class="project-show-img">
                        <div class="project-show-body">
                            <div class="project-company-badge">
                                <img src="logo_jamestech.png" alt="제임스텍 로고">
                                <span style="font-size:12px; color:var(--color-ash-gray); font-family:var(--font-mono);">제임스텍 (2024)</span>
                            </div>
                            <div class="project-show-title">슬기로운 재배생활 (Smart Farm Tycoon)</div>
                            <div class="project-show-desc">
                                스마트팜 농작물 재배 및 유통 시장 연계형 <strong>타이쿤 &amp; 경영 시뮬레이션</strong>.<br>
                                • 작물 성장 곡선, 온/습도 환경 계수 연산 및 장비 업그레이드 트리 기획.<br>
                                • 게임 내 시장 시세 변동 알고리즘 설계 및 유저 보상 체계 정립.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>'''

new_block = '''        <!-- [STAGE 3] 경력 & 프로젝트 (한 슬라이드 안에서 데블다이스 / 제임스텍 좌우 분리) -->
        <div class="showcase-stage" id="resumeStage3">
            <div class="stage-3-wrap" style="max-width:1200px; width:100%;">
                <div class="profile-tag" style="text-align:center;">CAREER &amp; MAJOR PROJECTS</div>
                <h2 style="font-size:32px; font-weight:800; text-align:center; margin-bottom:6px;">주요 경력 및 핵심 프로젝트</h2>
                <p style="color:var(--color-ash-gray); font-size:14px; text-align:center; margin-bottom:24px;">상용화 프로젝트 및 프로토타입 개발을 총괄 기획한 실무 경험</p>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:28px;">

                    <!-- 좌: 데블다이스 + 라스트 생츄어리 -->
                    <div style="background:rgba(15,17,23,0.88); border:1px solid rgba(146,129,247,0.2); border-radius:18px; overflow:hidden; display:flex; flex-direction:column;">
                        <div style="background:rgba(21,24,33,0.95); border-bottom:1px solid rgba(146,129,247,0.2); padding:14px 20px; display:flex; align-items:center; gap:12px;">
                            <img src="logo_devildice.png" alt="데블다이스" style="height:26px; background:#fff; padding:2px 8px; border-radius:5px; object-fit:contain;">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff;">데블다이스</div>
                                <div style="font-size:11.5px; color:var(--color-ash-gray); font-family:var(--font-mono);">게임 기획 · 정규직 (2023 – 2024)</div>
                            </div>
                        </div>
                        <img src="lastsanctuary.png" alt="LAST SANCTUARY" style="width:100%; height:175px; object-fit:cover; border-bottom:1px solid var(--color-graphite-hairline);">
                        <div style="padding:16px 20px; flex:1;">
                            <div style="font-size:17px; font-weight:800; color:#fff; margin-bottom:6px;">LAST SANCTUARY</div>
                            <div style="font-size:12.5px; color:var(--color-ash-gray); margin-bottom:12px;">포스트 아포칼립스 <strong style="color:#ccc;">생존 기지 건설 &amp; 디펜스 시뮬레이션</strong></div>
                            <div style="display:flex; flex-direction:column; gap:6px;">
                                <div style="font-size:12px; color:var(--color-ash-gray); padding:7px 11px; background:rgba(146,129,247,0.09); border-left:2px solid var(--color-iris-violet); border-radius:6px;">타일 기반 자원 순환 경제 시스템 설계 / FSM 적 AI 제어 기획</div>
                                <div style="font-size:12px; color:var(--color-ash-gray); padding:7px 11px; background:rgba(146,129,247,0.09); border-left:2px solid var(--color-iris-violet); border-radius:6px;">웨이브 주기 및 방어 타워 DPS 정밀 밸런싱 시트 구축</div>
                            </div>
                        </div>
                    </div>

                    <!-- 우: 제임스텍 + 슬기로운 재배생활 -->
                    <div style="background:rgba(15,17,23,0.88); border:1px solid rgba(126,200,227,0.2); border-radius:18px; overflow:hidden; display:flex; flex-direction:column;">
                        <div style="background:rgba(21,24,33,0.95); border-bottom:1px solid rgba(126,200,227,0.2); padding:14px 20px; display:flex; align-items:center; gap:12px;">
                            <img src="logo_jamestech.png" alt="제임스텍" style="height:26px; background:#fff; padding:2px 8px; border-radius:5px; object-fit:contain;">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff;">제임스텍</div>
                                <div style="font-size:11.5px; color:var(--color-ash-gray); font-family:var(--font-mono);">게임 기획 · 계약직 (2024 · 6개월)</div>
                            </div>
                        </div>
                        <img src="슬기로운재배생활.png" alt="슬기로운 재배생활" style="width:100%; height:175px; object-fit:cover; border-bottom:1px solid var(--color-graphite-hairline);">
                        <div style="padding:16px 20px; flex:1;">
                            <div style="font-size:17px; font-weight:800; color:#fff; margin-bottom:6px;">슬기로운 재배생활</div>
                            <div style="font-size:12.5px; color:var(--color-ash-gray); margin-bottom:12px;">스마트팜 농작물 재배 <strong style="color:#ccc;">타이쿤 &amp; 경영 시뮬레이션</strong></div>
                            <div style="display:flex; flex-direction:column; gap:6px;">
                                <div style="font-size:12px; color:var(--color-ash-gray); padding:7px 11px; background:rgba(126,200,227,0.09); border-left:2px solid #7ec8e3; border-radius:6px;">작물 성장 곡선 및 환경 계수 연산, 장비 업그레이드 트리 기획</div>
                                <div style="font-size:12px; color:var(--color-ash-gray); padding:7px 11px; background:rgba(126,200,227,0.09); border-left:2px solid #7ec8e3; border-radius:6px;">시장 시세 변동 알고리즘 설계 및 유저 보상 체계 정립</div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>'''

if old_block in content:
    content = content.replace(old_block, new_block)
    print("SUCCESS: Stage 3 block replaced!")
else:
    print("ERROR: Target block not found. Trying partial match...")
    # Find via markers
    start_marker = '<!-- [STAGE 3] 데블다이스'
    end_marker = '<!-- [STAGE 4]'
    s = content.find(start_marker)
    e = content.find(end_marker)
    if s != -1 and e != -1:
        print(f"Found from {s} to {e}")
        content = content[:s] + new_block + '\n\n        ' + content[e:]
        print("SUCCESS: Replaced via markers!")
    else:
        print(f"Start: {s}, End: {e}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done writing index.html")
