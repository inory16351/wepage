import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pages = re.findall(r'<div[^>]*id=["\'](?:page|section)-[^"\']+["\']', text)
print('Pages/Sections:', pages)

navs = re.findall(r'<button[^>]*class=["\'][^"\']*nav-link[^"\']*["\'][^>]*>([^<]+)</button>', text)
print('Nav links:', navs)

# Check play history
ph_idx = text.find('id="page-playhistory"')
if ph_idx == -1:
    ph_idx = text.find('id="playhistory"')
print('Play history container idx:', ph_idx)

# Check triangle radar
print('radar-triangle-container count:', text.count('radar-triangle-container'))

# Check server.js status
with open('server.js', 'r', encoding='utf-8') as f:
    sjs = f.read()
print('server.js lines:', len(sjs.splitlines()))
print('server.js has IGDB:', 'igdb' in sjs.lower())
