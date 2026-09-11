import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Check stage structure
stages = re.findall(r'id="resumeStage(\d+)"', c)
print('Stages found:', stages)

# Check navs
navs = re.findall(r'id="resumeNav(\d+)"', c)
print('Navs found:', navs)

# Check totalResumeStages
m = re.search(r'totalResumeStages\s*=\s*(\d+)', c)
print('totalResumeStages JS:', m.group(1) if m else 'NOT FOUND')

# Check for stage 3 and 4 content
s3_idx = c.find('id="resumeStage3"')
s4_idx = c.find('id="resumeStage4"')
print(f'Stage 3 at idx: {s3_idx}')
print(f'Stage 4 at idx: {s4_idx}')

if s3_idx > 0:
    snippet = c[s3_idx:s3_idx+300]
    import sys
    sys.stdout.buffer.write(('Stage3 snippet: ' + snippet + '\n').encode('utf-8'))
