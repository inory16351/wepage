with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

ph_idx = text.find('id="page-playhistory"')
if ph_idx != -1:
    section = text[ph_idx+4000:ph_idx+12000]
    with open('dump_playhistory_cards.txt', 'w', encoding='utf-8') as out:
        out.write(section)
    print("Dumped cards of playhistory")
