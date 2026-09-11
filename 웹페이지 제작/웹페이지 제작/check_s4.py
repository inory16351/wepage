with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s4_idx = text.find('id="resumeStage4"')
if s4_idx != -1:
    s5_idx = text.find('id="resumeStage5"')
    print(text[s4_idx:s5_idx])
