import sys

with open('build_index_recovered.py', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('radar-svg-col')
print('idx of radar-svg-col:', idx)

html_idx = c.find('class="radar-svg-col"')
print('idx of class="radar-svg-col":', html_idx)

# Find playhistory page content
ph_idx = c.find('id="page-playhistory"')
print('idx of page-playhistory:', ph_idx)
if ph_idx != -1:
    with open('playhistory_section.html', 'w', encoding='utf-8') as out:
        out.write(c[ph_idx:ph_idx+4000])
    print("Wrote playhistory_section.html")
