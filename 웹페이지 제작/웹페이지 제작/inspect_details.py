import sys

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Inspect Stage 4
s4_idx = text.find('id="resumeStage4"')
if s4_idx != -1:
    print("--- STAGE 4 SNIPPET ---")
    sys.stdout.buffer.write(text[s4_idx:s4_idx+1500].encode('utf-8'))
    print("\n----------------------")

# Inspect Stage 5
s5_idx = text.find('id="resumeStage5"')
if s5_idx != -1:
    print("--- STAGE 5 SNIPPET ---")
    sys.stdout.buffer.write(text[s5_idx:s5_idx+1000].encode('utf-8'))
    print("\n----------------------")

# Inspect Play History Cards
ph_idx = text.find('id="playGrid"')
if ph_idx != -1:
    print("--- PLAY GRID SNIPPET ---")
    sys.stdout.buffer.write(text[ph_idx:ph_idx+1500].encode('utf-8'))
    print("\n-------------------------")
