with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import sys

# Find logos in stage 3
s3_idx = text.find('id="resumeStage3"')
s4_idx = text.find('id="resumeStage4"')
sys.stdout.buffer.write(text[s3_idx:s4_idx].encode('utf-8'))
