import json

path = r'C:\Users\user\.gemini\antigravity-ide\brain\2feb59ec-ac43-4c4d-badd-cf6dec244250\.system_generated\logs\transcript_full.jsonl'

matches = []
with open(path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        data = json.loads(line)
        calls = data.get('tool_calls', [])
        for c in calls:
            name = c.get('name')
            if name == 'write_to_file':
                args = c.get('args', {})
                target = args.get('TargetFile', '')
                if 'build_index.py' in target:
                    matches.append((line_idx, len(args.get('CodeContent', '')), args.get('CodeContent', '')))

print(f"Found {len(matches)} matches for build_index.py")
if matches:
    # Look through matches
    for idx, length, content in matches:
        print(f"Match line {idx}, length: {length}")
    latest_line, length, content = matches[-1]
    with open('build_index_recovered.py', 'w', encoding='utf-8') as out:
        out.write(content)
    print("Saved build_index_recovered.py")
