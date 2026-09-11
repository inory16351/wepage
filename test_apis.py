import urllib.request, json

print("Testing portfolio documents API...")
try:
    res = urllib.request.urlopen('http://localhost:3000/api/portfolio-documents')
    data = json.loads(res.read().decode('utf-8'))
    print("Portfolio docs categories count:", len(data))
    for cat in data:
        print("  -", cat["category"], f"({len(cat['items'])} items)")
except Exception as e:
    print("Docs API Error:", e)

print("\nTesting search games API (q=mario)...")
try:
    res = urllib.request.urlopen('http://localhost:3000/api/search-games?q=mario')
    games = json.loads(res.read().decode('utf-8'))
    print("Search games result count:", len(games))
    if games:
        print("  Top result:", games[0]['title'], f"({games[0].get('releaseYear')})")
        print("  Cover:", games[0].get('coverUrl'))
except Exception as e:
    print("Search API Error:", e)
