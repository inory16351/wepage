with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update play-card covers
old_civ = 'https://images.igdb.com/igdb/image/upload/t_cover_big/co49x5.jpg'
new_civ = 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqr.jpg'

old_fm = 'https://images.igdb.com/igdb/image/upload/t_cover_big/co73d7.jpg'
new_fm = 'https://images.igdb.com/igdb/image/upload/t_cover_big/co73z1.jpg'

old_rim = 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2k34.jpg'
new_rim = 'https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqj.jpg'

content = content.replace(old_civ, new_civ)
content = content.replace(old_fm, new_fm)
content = content.replace(old_rim, new_rim)

# 2. Update addGameToHistory to remove play-card-desc
old_add_game = '''            card.innerHTML = `
                <img src="${coverSrc}" alt="${game.title}" class="play-cover-img" onerror="this.src='lastsanctuary.png'">
                <div class="play-card-body">
                    <div class="play-card-title">${game.title}</div>
                    <div class="play-card-meta">${game.genre} / 신규 등록</div>
                    <div class="play-card-desc">IGDB 연동을 통해 추가된 분석 대상 타이틀 (${game.platform}).</div>
                </div>
            `;'''

new_add_game = '''            card.innerHTML = `
                <img src="${coverSrc}" alt="${game.title}" class="play-cover-img" onerror="this.src='lastsanctuary.png'">
                <div class="play-card-body">
                    <div class="play-card-title">${game.title}</div>
                    <div class="play-card-meta">${game.genre} / ${game.releaseYear || 'IGDB 등록'}</div>
                </div>
            `;'''

if old_add_game in content:
    content = content.replace(old_add_game, new_add_game)
    print("SUCCESS: Updated addGameToHistory!")
else:
    print("WARNING: old_add_game pattern not found exactly, checking partial...")
    target = '<div class="play-card-desc">IGDB 연동을 통해 추가된 분석 대상 타이틀 (${game.platform}).</div>'
    if target in content:
        content = content.replace(target, '')
        print("SUCCESS: Removed play-card-desc in addGameToHistory!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: index.html updated with correct thumbnails and clean card format!")
