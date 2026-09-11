with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find portfolio section
ph_idx = text.find('id="page-portfolio"')
if ph_idx == -1:
    ph_idx = text.find('id="page-docs"')
if ph_idx == -1:
    ph_idx = text.find('포트폴리오')

ph_end_idx = text.find('</section>', ph_idx)

with open('dump_portfolio.txt', 'w', encoding='utf-8') as f:
    f.write(text[ph_idx:ph_end_idx+50])

print(f"Found at idx {ph_idx}, end {ph_end_idx}")
print("First 2000 chars:")
import sys
sys.stdout.buffer.write(text[ph_idx:ph_idx+2000].encode('utf-8'))
