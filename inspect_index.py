with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("File size:", len(text))
print("DOCTYPE count:", text.count("<!DOCTYPE html>"))
print("page-main count:", text.count('id="page-main"'))
print("main-step-1 count:", text.count('id="main-step-1"'))
print("main-step-2 count:", text.count('id="main-step-2"'))
print("main-step-3 count:", text.count('id="main-step-3"'))

lines = text.splitlines()
for i, line in enumerate(lines):
    if 'id="page-main"' in line or 'id="page-resume"' in line:
        print(f"Line {i+1}: {line[:60]}")
