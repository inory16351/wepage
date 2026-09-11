import urllib.request, urllib.parse, json

queries = ['civilization', 'zelda', 'league of legends', 'dark souls', 'starcraft', 'overwatch', 'gta', 'pokemon', 'fifa', '마리오', '피파', '롤', '배그', '하스스톤', '디아블로']

for q in queries:
    url = f'http://localhost:3000/api/search-games?q={urllib.parse.quote(q)}'
    try:
        req = urllib.request.urlopen(url, timeout=5)
        data = json.loads(req.read().decode('utf-8'))
        print(f'OK: "{q}" -> {len(data)} results (Top: {data[0]["title"] if data else "None"})')
    except Exception as e:
        print(f'FAIL: "{q}" -> {e}')
