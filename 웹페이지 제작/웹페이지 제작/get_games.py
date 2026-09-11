import urllib.request
import urllib.parse
import json

games = ['Civilization VI', 'RimWorld', 'Football Manager 2024']
results = {}

for g in games:
    url = f"http://localhost:3000/api/search-games?q={urllib.parse.quote(g)}"
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))
        # find best matching
        best = data[0] if data else None
        results[g] = best
        print(f"[{g}]")
        if best:
            print("  Title:", best.get('title'))
            print("  Cover:", best.get('coverUrl'))
            print("  Platform:", best.get('platform'))
            print("  Genre:", best.get('genre'))
            print("  Year:", best.get('releaseYear'))
        else:
            print("  Not found")
    except Exception as e:
        print(f"Error fetching {g}: {e}")

with open('igdb_top_games.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
