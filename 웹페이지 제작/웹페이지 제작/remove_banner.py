import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 메인 로비 hero-banner-wrap 및 주석 제거
pattern = r'<!--\s*메인 비주얼 타이틀 배너[\s\S]*?</div>\s*</div>'
match = re.search(r'<!--\s*메인 비주얼 타이틀 배너[\s\S]*?</div>\s*</div>', content)

if not match:
    # 혹시 주석 형식이 다를 경우 div 직접 탐색
    match = re.search(r'<div class="hero-banner-wrap">[\s\S]*?</div>', content)

if match:
    content = content.replace(match.group(0), '')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Main lobby banner successfully removed!")
else:
    print("Banner not found, checking lines...")
