import json

log_path = r'C:\Users\user\.gemini\antigravity-ide\brain\44fedeb6-d481-41c6-970e-4d9f436acaaf\.system_generated\logs\transcript_full.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        data = json.loads(line)
        content = str(data.get('content', ''))
        if '<!DOCTYPE html>' in content and '탄탄한 논리로 상상하는' in content:
            pos = content.find('<section id="page-main"')
            pos_end = content.find('</section>', pos)
            extracted = content[pos:pos_end+10]
            with open('original_main_extracted.html', 'w', encoding='utf-8') as out:
                out.write(extracted)
            print(f"Extracted {len(extracted)} chars from DOCTYPE at line {idx}!")
            break
