with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update the HTML button in playhistory section
old_btn = '''            <button class="btn-ghost" onclick="openGameSearchModal()" style="padding:10px 18px; border-color:var(--color-iris-violet); background:rgba(146,129,247,0.18); font-weight:600;">
                <span>🔍 IGDB 게임 실시간 검색 및 추가</span>
            </button>'''

new_btn = '''            <button class="btn-ghost" id="openSearchModalBtn" onclick="openGameSearchModal()" style="padding:10px 18px; border-color:var(--color-iris-violet); border-style:dashed; background:rgba(146,129,247,0.08); font-weight:600; opacity:0.75; display:inline-flex; align-items:center; gap:8px; transition:all 0.3s ease; cursor:pointer;" title="상단 우측의 [편집 모드 ON]을 켜면 게임 추가가 활성화됩니다.">
                <span id="searchBtnIcon">🔒</span>
                <span id="searchBtnText">IGDB 게임 추가 (편집 모드 필요)</span>
            </button>'''

if old_btn in c:
    c = c.replace(old_btn, new_btn)
    print("SUCCESS: Updated search button HTML")
else:
    print("WARNING: old_btn not found exactly, trying search...")
    import re
    m = re.search(r'<button class="btn-ghost" onclick="openGameSearchModal\(\)"[^>]*>.*?<\/button>', c, re.DOTALL)
    if m:
        c = c[:m.start()] + new_btn + c[m.end():]
        print("SUCCESS: Replaced via regex!")

# 2. Update openGameSearchModal and addGameToHistory and toggleEditMode
old_modal_func = '''        function openGameSearchModal() {
            const modal = document.getElementById('igdbModal');
            modal.classList.add('active');
            // 모달 열릴 때 기본 추천 게임 20종 자동 로드!
            const input = document.getElementById('gameSearchInput');
            input.value = '';
            fetchAndRenderGames('');
            input.focus();
        }'''

new_modal_func = '''        function openGameSearchModal() {
            if (!isEditMode) {
                showToast('🔒 게임 추가는 상단 우측 [편집 모드 ON]을 켰을 때만 가능합니다.');
                const toggleBtn = document.getElementById('editToggleBtn');
                if (toggleBtn) {
                    toggleBtn.style.transform = 'scale(1.15)';
                    toggleBtn.style.boxShadow = '0 0 18px var(--color-iris-violet)';
                    toggleBtn.style.borderColor = 'var(--color-iris-violet)';
                    setTimeout(() => {
                        toggleBtn.style.transform = '';
                        toggleBtn.style.boxShadow = '';
                        toggleBtn.style.borderColor = '';
                    }, 900);
                }
                return;
            }
            const modal = document.getElementById('igdbModal');
            modal.classList.add('active');
            // 모달 열릴 때 기본 추천 게임 20종 자동 로드!
            const input = document.getElementById('gameSearchInput');
            input.value = '';
            fetchAndRenderGames('');
            input.focus();
        }'''

if old_modal_func in c:
    c = c.replace(old_modal_func, new_modal_func)
    print("SUCCESS: Updated openGameSearchModal")

# Update addGameToHistory
old_add_start = 'function addGameToHistory(game) {'
new_add_start = '''function addGameToHistory(game) {
            if (!isEditMode) {
                showToast('🔒 편집 모드가 켜져 있을 때만 게임을 추가할 수 있습니다.');
                return;
            }'''

if old_add_start in c and 'if (!isEditMode)' not in c[c.find(old_add_start):c.find(old_add_start)+200]:
    c = c.replace(old_add_start, new_add_start, 1)
    print("SUCCESS: Updated addGameToHistory guard")

# Update toggleEditMode
old_toggle = '''        let isEditMode = false;
        function toggleEditMode() {
            isEditMode = !isEditMode;
            const btn = document.getElementById('editToggleBtn');
            btn.textContent = isEditMode ? '편집 모드 ON' : '편집 모드 OFF';
            btn.classList.toggle('active', isEditMode);
            showToast(isEditMode ? '편집 모드가 활성화되었습니다. 텍스트를 직접 수정할 수 있습니다.' : '편집 모드가 비활성화되었습니다.');
            
            document.querySelectorAll('[contenteditable]').forEach(el => {
                el.contentEditable = isEditMode ? 'true' : 'false';
            });
        }'''

new_toggle = '''        let isEditMode = false;
        function updateEditModeUI() {
            const btn = document.getElementById('editToggleBtn');
            if (btn) {
                btn.textContent = isEditMode ? '편집 모드 ON' : '편집 모드 OFF';
                btn.classList.toggle('active', isEditMode);
            }

            // IGDB 게임 추가 버튼 상태 연동
            const modalBtn = document.getElementById('openSearchModalBtn');
            const searchIcon = document.getElementById('searchBtnIcon');
            const searchText = document.getElementById('searchBtnText');
            if (modalBtn && searchIcon && searchText) {
                if (isEditMode) {
                    searchIcon.textContent = '🔍';
                    searchText.textContent = 'IGDB 게임 실시간 검색 및 추가';
                    modalBtn.style.opacity = '1';
                    modalBtn.style.borderStyle = 'solid';
                    modalBtn.style.background = 'rgba(146, 129, 247, 0.25)';
                    modalBtn.style.boxShadow = '0 0 14px rgba(146, 129, 247, 0.45)';
                    modalBtn.title = 'IGDB 데이터베이스에서 원하는 게임을 검색하여 히스토리에 추가합니다.';
                } else {
                    searchIcon.textContent = '🔒';
                    searchText.textContent = 'IGDB 게임 추가 (편집 모드 필요)';
                    modalBtn.style.opacity = '0.75';
                    modalBtn.style.borderStyle = 'dashed';
                    modalBtn.style.background = 'rgba(146, 129, 247, 0.08)';
                    modalBtn.style.boxShadow = 'none';
                    modalBtn.title = '상단 우측의 [편집 모드 ON]을 켜면 게임 추가가 활성화됩니다.';
                }
            }

            document.querySelectorAll('[contenteditable]').forEach(el => {
                el.contentEditable = isEditMode ? 'true' : 'false';
            });
        }

        function toggleEditMode() {
            isEditMode = !isEditMode;
            updateEditModeUI();
            showToast(isEditMode 
                ? '✏️ 편집 모드가 켜졌습니다! IGDB 게임 추가 및 텍스트 편집이 가능합니다.' 
                : '🔒 편집 모드가 꺼졌습니다 (읽기 전용).');
        }'''

if old_toggle in c:
    c = c.replace(old_toggle, new_toggle)
    print("SUCCESS: Updated toggleEditMode and added updateEditModeUI")
else:
    print("WARNING: old_toggle not matched exactly, trying partial...")
    s_idx = c.find('let isEditMode = false;')
    e_idx = c.find('// 초기 데이터 로딩', s_idx)
    if s_idx != -1 and e_idx != -1:
        c = c[:s_idx] + new_toggle + '\n\n        ' + c[e_idx:]
        print("SUCCESS: Replaced toggle block via indices!")

# Update DOMContentLoaded to call updateEditModeUI()
old_dcl = '''        window.addEventListener('DOMContentLoaded', () => {
            loadPortfolioDocuments();
        });'''

new_dcl = '''        window.addEventListener('DOMContentLoaded', () => {
            loadPortfolioDocuments();
            updateEditModeUI();
        });'''

if old_dcl in c:
    c = c.replace(old_dcl, new_dcl)
    print("SUCCESS: Added updateEditModeUI to DOMContentLoaded")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Finished updating index.html!")
