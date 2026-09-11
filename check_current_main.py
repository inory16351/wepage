with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="page-main"')
end_pos = text.find('</section>', pos)

print(text[pos:end_pos+10])
