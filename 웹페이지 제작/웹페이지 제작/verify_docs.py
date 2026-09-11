import os, re

portfolio_dir = os.path.join('포폴 정리용', '포트폴리오')
actual_files = set(os.listdir(portfolio_dir))

with open('server.js', 'r', encoding='utf-8') as f:
    code = f.read()

names = re.findall(r"name:\s*'([^']+)'", code)
print("Total names in server.js:", len(names))
all_found = True
for n in names:
    found = n in actual_files
    if not found:
        print("MISSING:", n)
        all_found = False
    else:
        print("OK:", n)

print("All matched:", all_found)
