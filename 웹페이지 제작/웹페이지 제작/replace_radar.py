import re

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

                        <!-- 정밀 눈금 라벨 (25%, 50%, 75%, 100%) -->
                        <text x="184" y="65" fill="#9281f7" font-size="9" font-family="Commit Mono">100%</text>
                        <text x="184" y="90" fill="#71768a" font-size="8.5" font-family="Commit Mono">75%</text>
                        <text x="184" y="114" fill="#71768a" font-size="8.5" font-family="Commit Mono">50%</text>
                        <text x="184" y="138" fill="#585c6c" font-size="8.5" font-family="Commit Mono">25%</text>

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

for target_file in ['index.html', 'build_index.py']:
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find radar-svg-col content
    pattern = r'(<div class="radar-svg-col">\s*)<svg[\s\S]*?</svg>'
    subbed = re.sub(pattern, r'\1' + new_radar_svg, content)
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(subbed)
    print(f"Replaced radar in {target_file} successfully!")
