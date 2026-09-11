import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

print("--- NAV / HEADER ---")
for i, line in enumerate(lines[:150]):
    if '<nav' in line or 'switchPage' in line or '<button' in line or '<a ' in line:
        print(f"{i+1}: {line.strip()}")

print("\n--- PAGE SECTIONS ---")
for i, line in enumerate(lines):
    if 'page-section' in line or 'id="page-' in line:
        print(f"{i+1}: {line.strip()}")

print("\n--- RESUME TABS ---")
for i, line in enumerate(lines):
    if 'resume' in line.lower() or '이력' in line or '경력' in line:
        print(f"{i+1}: {line.strip()[:120]}")
