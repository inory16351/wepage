# index.html 이미지 잘림 방지 및 완벽 비율 맞춤 업데이트 스크립트

html_content = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>정승운 포트폴리오 - 탄탄한 논리로 상상하는 크리에이터</title>
    <!-- Pretendard 폰트 및 Commit Mono, Inter 로드 -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <link href="https://fonts.googleapis.com/css2?family=Commit+Mono:ital,wght@0,400..700;1,400..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Design Tokens based on DESIGN_BLACK.md & Resend Style */
        :root {
            --color-void-black: #000000;
            --color-graphite-hairline: #292d30;
            --color-white: #ffffff;
            --color-bone-white: #f0f0f0;
            --color-ash-gray: #a1a4a5;
            --color-iris-violet: #9281f7;
            --font-main: 'Pretendard', var(--font-inter), -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'Commit Mono', monospace;
            --radius-cards: 16px;
            --radius-buttons: 6px;
            --max-width: 1200px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background-color: var(--color-void-black);
            color: var(--color-bone-white);
            font-family: var(--font-main);
            line-height: 1.5;
            overflow-x: hidden;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        /* Navigation Bar */
        header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--color-graphite-hairline);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 32px;
        }

        .logo {
            font-family: var(--font-mono);
            font-size: 14px;
            color: var(--color-white);
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .logo:hover {
            color: var(--color-iris-violet);
        }

        nav {
            display: flex;
            gap: 16px;
            align-items: center;
        }

        .nav-link {
            background: transparent;
            border: none;
            color: var(--color-bone-white);
            font-size: 14px;
            font-family: var(--font-main);
            cursor: pointer;
            transition: color 0.2s ease;
            padding: 6px 10px;
            border-radius: var(--radius-buttons);
        }

        .nav-link:hover, .nav-link.active {
            color: var(--color-white);
            background: rgba(255, 255, 255, 0.05);
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }

        .home-shortcut-btn {
            background: rgba(146, 129, 247, 0.1);
            border: 1px solid var(--color-iris-violet);
            color: var(--color-iris-violet);
            padding: 6px 12px;
            border-radius: var(--radius-buttons);
            font-size: 12px;
            font-family: var(--font-mono);
            cursor: pointer;
            transition: all 0.2s;
        }

        .home-shortcut-btn:hover {
            background: var(--color-iris-violet);
            color: #000;
        }

        /* 편집 모드 토글 스위치 버튼 */
        .edit-toggle-btn {
            background: transparent;
            border: 1px dashed var(--color-ash-gray);
            color: var(--color-ash-gray);
            padding: 5px 12px;
            border-radius: var(--radius-buttons);
            font-size: 12px;
            font-family: var(--font-mono);
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .edit-toggle-btn.active {
            background: rgba(255, 75, 75, 0.15);
            border-color: #ff4b4b;
            color: #ff4b4b;
            font-weight: 600;
        }

        .edit-toggle-btn:hover {
            border-color: var(--color-white);
            color: var(--color-white);
        }

        /* Container Layout */
        .container {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 100px 24px 60px;
            min-height: 100vh;
        }

        /* Common Elements */
        .section-title {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 12px;
            color: var(--color-white);
        }

        .section-desc {
            color: var(--color-ash-gray);
            font-size: 16px;
            margin-bottom: 40px;
        }

        /* Contenteditable styling when active */
        [contenteditable="true"] {
            outline: 1px dashed rgba(146, 129, 247, 0.6);
            background: rgba(146, 129, 247, 0.05);
            border-radius: 4px;
            cursor: text;
        }

        /* Main Page Steps Architecture */
        .main-step-container {
            display: none;
            min-height: 65vh;
            flex-direction: column;
            justify-content: center;
            animation: fadeIn 0.4s ease-in-out;
            cursor: pointer;
        }
        .main-step-container.active {
            display: flex;
        }

        .main-nav-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 48px;
            border-top: 1px solid var(--color-graphite-hairline);
            padding-top: 20px;
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--color-ash-gray);
        }

        .step-indicator {
            color: var(--color-iris-violet);
            font-weight: 600;
        }

        /* Hero Banner Wrap: Title.png 잘림 방지 및 원본 비율 완벽 표시 */
        .hero-banner-wrap {
            margin-bottom: 28px;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--color-graphite-hairline);
            background: #08090c;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        .hero-banner-img {
            width: 100%;
            height: auto;
            max-height: 480px;
            object-fit: contain;
            display: block;
            transition: transform 0.4s ease;
        }
        .hero-banner-wrap:hover .hero-banner-img {
            transform: scale(1.01);
        }

        .hero-logline {
            font-size: 48px;
            font-weight: 700;
            line-height: 1.25;
            letter-spacing: -0.03em;
            color: var(--color-white);
            margin-bottom: 24px;
        }

        .hero-logline span {
            color: var(--color-iris-violet);
        }

        .hero-sub {
            font-size: 18px;
            color: var(--color-ash-gray);
            max-width: 720px;
            line-height: 1.6;
            margin-bottom: 32px;
        }

        /* Grid Layouts */
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 32px;
        }

        .card-custom {
            background: var(--color-void-black);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: var(--radius-cards);
            padding: 24px;
            transition: border-color 0.2s, transform 0.2s;
        }

        .card-custom:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-2px);
        }

        .card-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--color-white);
            margin-bottom: 8px;
        }

        .card-desc {
            font-size: 14px;
            color: var(--color-ash-gray);
            line-height: 1.6;
        }

        /* Component Block in Step 3 */
        .component-block {
            border: 1px solid var(--color-graphite-hairline);
            border-radius: var(--radius-cards);
            padding: 24px;
            margin-bottom: 24px;
            background: rgba(255, 255, 255, 0.01);
        }

        .component-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }

        .component-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--color-white);
        }

        /* Buttons */
        .btn-ghost {
            background: transparent;
            border: 1px solid var(--color-graphite-hairline);
            color: var(--color-bone-white);
            padding: 6px 14px;
            border-radius: var(--radius-buttons);
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
            font-family: var(--font-mono);
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .btn-ghost:hover {
            border-color: var(--color-iris-violet);
            color: var(--color-white);
            background: rgba(146, 129, 247, 0.08);
        }

        .btn-ghost.disabled {
            opacity: 0.4;
            cursor: not-allowed;
            pointer-events: none;
        }

        .btn-primary {
            background: var(--color-iris-violet);
            border: 1px solid var(--color-iris-violet);
            color: #000;
            padding: 8px 18px;
            border-radius: var(--radius-buttons);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: var(--font-main);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .btn-primary:hover {
            background: #a596f9;
            transform: translateY(-1px);
        }

        /* Play History Grid: 3:4 세로 포스터 비율 적용으로 IGDB 커버 잘림 완벽 방지 */
        .play-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 18px;
        }

        .play-card {
            background: #0a0b0e;
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.25s ease;
            display: flex;
            flex-direction: column;
        }

        .play-card:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-3px);
            box-shadow: 0 10px 24px rgba(146, 129, 247, 0.15);
        }

        /* IGDB cover_big의 3:4 비율 정확히 반영 */
        .play-thumb {
            width: 100%;
            aspect-ratio: 3 / 4;
            background: #07080a;
            border-bottom: 1px solid var(--color-graphite-hairline);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }

        .play-thumb img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .play-card:hover .play-thumb img {
            transform: scale(1.04);
        }

        .play-content {
            padding: 14px;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: #0a0b0e;
        }

        .play-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--color-white);
            margin-bottom: 8px;
            line-height: 1.35;
        }

        .play-meta {
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 11px;
            color: var(--color-ash-gray);
            font-family: var(--font-mono);
        }

        .play-meta-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Main Page Project Grid: 2열 카드 이미지 잘림 방지 */
        .main-project-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .main-project-card {
            background: #0a0b0e;
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 14px;
            overflow: hidden;
            transition: all 0.25s ease;
            cursor: pointer;
            display: flex;
            flex-direction: column;
        }

        .main-project-card:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-3px);
            box-shadow: 0 10px 24px rgba(146, 129, 247, 0.15);
        }

        .main-project-imgbox {
            width: 100%;
            height: 240px;
            background: #060709;
            border-bottom: 1px solid var(--color-graphite-hairline);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px;
            overflow: hidden;
        }

        .main-project-imgbox img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            transition: transform 0.3s ease;
        }

        .main-project-card:hover .main-project-imgbox img {
            transform: scale(1.03);
        }

        /* Portfolio Page: 가로형 와이드 프로젝트 카드 (좌측 완벽 비율 이미지 + 우측 상세 설명) */
        .project-card-horizontal {
            display: grid;
            grid-template-columns: 420px 1fr;
            background: #0a0b0e;
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 24px;
            transition: all 0.25s ease;
            cursor: pointer;
        }

        .project-card-horizontal:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-3px);
            box-shadow: 0 12px 28px rgba(146, 129, 247, 0.16);
        }

        .project-horizontal-imgbox {
            width: 100%;
            min-height: 270px;
            background: #060709;
            border-right: 1px solid var(--color-graphite-hairline);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
            overflow: hidden;
        }

        .project-horizontal-imgbox img {
            width: 100%;
            height: 100%;
            max-height: 250px;
            object-fit: contain;
            transition: transform 0.3s ease;
        }

        .project-card-horizontal:hover .project-horizontal-imgbox img {
            transform: scale(1.03);
        }

        .project-card-body {
            padding: 28px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .project-title {
            font-size: 20px;
            font-weight: 600;
            color: var(--color-white);
            margin-bottom: 10px;
        }

        .project-desc {
            font-size: 14px;
            color: var(--color-ash-gray);
            line-height: 1.65;
            margin-bottom: 20px;
        }

        /* Resume & Sub Tabs */
        .resume-tabs, .portfolio-tabs {
            display: flex;
            gap: 12px;
            margin-bottom: 28px;
            border-bottom: 1px solid var(--color-graphite-hairline);
            padding-bottom: 12px;
        }

        .sub-tab-btn {
            background: transparent;
            border: none;
            color: var(--color-ash-gray);
            font-size: 15px;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: var(--radius-buttons);
            cursor: pointer;
            transition: all 0.2s;
        }

        .sub-tab-btn:hover {
            color: var(--color-white);
            background: rgba(255, 255, 255, 0.04);
        }

        .sub-tab-btn.active {
            color: var(--color-white);
            background: rgba(146, 129, 247, 0.15);
            border: 1px solid rgba(146, 129, 247, 0.4);
            font-weight: 600;
        }

        .sub-content {
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }

        .sub-content.active {
            display: block;
        }

        .resume-section-box {
            border: 1px solid var(--color-graphite-hairline);
            border-radius: var(--radius-cards);
            padding: 24px;
            margin-bottom: 24px;
            background: rgba(255, 255, 255, 0.01);
        }

        .resume-section-box h3 {
            font-size: 17px;
            color: var(--color-white);
            margin-bottom: 16px;
            border-left: 3px solid var(--color-iris-violet);
            padding-left: 10px;
        }

        /* Custom Table */
        .table-custom {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }

        .table-custom th, .table-custom td {
            border: 1px solid var(--color-graphite-hairline);
            padding: 12px 16px;
            text-align: left;
        }

        .table-custom th {
            background: rgba(255, 255, 255, 0.03);
            color: var(--color-ash-gray);
            font-weight: 500;
            font-family: var(--font-mono);
            font-size: 13px;
        }

        .table-custom td {
            color: var(--color-bone-white);
        }

        /* Stats Overview */
        .stats-overview {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 32px;
        }

        .stat-box {
            border: 1px solid var(--color-graphite-hairline);
            border-radius: var(--radius-cards);
            padding: 20px;
            background: rgba(255, 255, 255, 0.01);
        }

        .stat-box h4 {
            font-size: 14px;
            color: var(--color-ash-gray);
            margin-bottom: 16px;
            font-family: var(--font-mono);
        }

        .stat-bar-item {
            margin-bottom: 12px;
        }

        .stat-bar-label {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            margin-bottom: 4px;
        }

        .bar-bg {
            height: 6px;
            background: #1a1a1a;
            border-radius: 3px;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            background: var(--color-iris-violet);
            border-radius: 3px;
        }

        /* Documents Archive Section */
        .doc-category-block {
            margin-bottom: 40px;
        }

        .doc-category-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }

        .doc-category-title {
            font-size: 19px;
            font-weight: 600;
            color: var(--color-white);
        }

        .doc-category-badge {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--color-iris-violet);
            background: rgba(146, 129, 247, 0.12);
            border: 1px solid rgba(146, 129, 247, 0.35);
            padding: 3px 10px;
            border-radius: 4px;
            letter-spacing: 0.05em;
        }

        .doc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 16px;
        }

        .doc-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s ease;
        }

        .doc-card:hover {
            border-color: rgba(146, 129, 247, 0.6);
            background: rgba(146, 129, 247, 0.04);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }

        .doc-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
            gap: 10px;
        }

        .doc-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--color-white);
            line-height: 1.4;
        }

        .doc-desc {
            font-size: 13px;
            color: var(--color-ash-gray);
            line-height: 1.5;
            margin-bottom: 16px;
            flex: 1;
        }

        .doc-footer-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 12px;
            font-family: var(--font-mono);
            color: var(--color-ash-gray);
        }

        .doc-type-badge {
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            letter-spacing: 0.05em;
            flex-shrink: 0;
        }

        .doc-type-badge.pdf {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }

        .doc-type-badge.pptx {
            background: rgba(249, 115, 22, 0.15);
            color: #fb923c;
            border: 1px solid rgba(249, 115, 22, 0.4);
        }

        .doc-type-badge.xlsx {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.4);
        }

        .doc-btn-group {
            display: flex;
            gap: 8px;
        }

        /* Modals: 배너 이미지 완벽 맞춤 */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 2000;
            overflow-y: auto;
            padding: 40px 20px;
        }

        .modal-content {
            background: #09090b;
            border: 1px solid var(--color-graphite-hairline);
            border-radius: var(--radius-cards);
            max-width: 860px;
            margin: 0 auto;
            padding: 32px;
            position: relative;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
            animation: fadeIn 0.25s ease-out;
        }

        .modal-close {
            position: absolute;
            top: 24px;
            right: 24px;
            background: transparent;
            border: none;
            color: var(--color-ash-gray);
            font-size: 13px;
            cursor: pointer;
            font-family: var(--font-mono);
            padding: 4px 8px;
            border-radius: 4px;
        }

        .modal-close:hover {
            color: var(--color-white);
            background: rgba(255, 255, 255, 0.1);
        }

        .detail-block {
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.015);
        }

        .detail-block h4 {
            font-size: 15px;
            color: var(--color-white);
            margin-bottom: 8px;
            font-family: var(--font-mono);
        }

        .detail-block p, .detail-block ul {
            font-size: 14px;
            color: var(--color-ash-gray);
            line-height: 1.65;
        }

        .detail-block ul {
            padding-left: 20px;
        }

        .modal-banner-wrap {
            width: 100%;
            background: #060709;
            border-radius: 12px;
            border: 1px solid var(--color-graphite-hairline);
            margin-bottom: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 12px;
            overflow: hidden;
        }

        .modal-banner-wrap img {
            max-width: 100%;
            max-height: 400px;
            object-fit: contain;
            display: block;
        }

        .modal-doc-links {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 12px;
        }

        /* Game Search Modal */
        .game-search-box {
            margin-bottom: 20px;
        }

        .game-search-input {
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: var(--radius-buttons);
            padding: 12px 16px;
            color: #fff;
            font-size: 15px;
            font-family: var(--font-main);
            outline: none;
            transition: border-color 0.2s;
        }

        .game-search-input:focus {
            border-color: var(--color-iris-violet);
        }

        .game-search-results {
            max-height: 420px;
            overflow-y: auto;
            border: 1px solid var(--color-graphite-hairline);
            border-radius: var(--radius-buttons);
            background: #000;
        }

        .live-search-badge {
            font-size: 9px;
            font-family: var(--font-mono);
            background: rgba(146, 129, 247, 0.15);
            color: var(--color-iris-violet);
            border: 1px solid var(--color-iris-violet);
            padding: 2px 6px;
            border-radius: 4px;
            margin-bottom: 4px;
            display: inline-block;
        }

        /* Page Section Display */
        .page-section {
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }

        .page-section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 900px) {
            .project-card-horizontal { grid-template-columns: 1fr; }
            .project-horizontal-imgbox { border-right: none; border-bottom: 1px solid var(--color-graphite-hairline); min-height: 220px; }
            .main-project-grid { grid-template-columns: 1fr; }
        }

        @media (max-width: 768px) {
            header { padding: 12px 16px; }
            nav { gap: 8px; }
            .nav-link { font-size: 12px; padding: 4px 6px; }
            .hero-logline { font-size: 32px; }
            .grid-3, .stats-overview, .doc-grid { grid-template-columns: 1fr; }
            .container { padding: 80px 16px 40px; }
        }
    </style>
</head>
<body>

    <!-- 헤더 및 통합 네비게이션 바 -->
    <header>
        <div class="logo" onclick="switchPage('main')">
            <span>SEUNGWOON.DEV</span>
            <span style="font-size:10px; color:var(--color-iris-violet); background:rgba(146,129,247,0.15); padding:2px 6px; border-radius:4px;">PORTFOLIO</span>
        </div>
        <nav>
            <button class="nav-link active" onclick="switchPage('main', this)">메인</button>
            <button class="nav-link" onclick="switchPage('resume', this)">이력/자기소개서</button>
            <button class="nav-link" onclick="switchPage('portfolio', this)">포트폴리오</button>
            <button class="nav-link" onclick="switchPage('playhistory', this)">플레이 히스토리</button>
            <button class="edit-toggle-btn" id="editToggleBtn" onclick="toggleEditMode()">편집 모드 OFF</button>
        </nav>
    </header>

    <div class="container">

        <!-- 1. 메인 페이지 (3단계 구성) -->
        <section id="page-main" class="page-section active">
            
            <!-- Step 1: 메인 인트로 및 핵심 로그라인 -->
            <div class="main-step-container active" id="main-step-1" onclick="handleStepClick(2)">
                <div style="padding: 10px 0 20px;">
                    <!-- 메인 비주얼 타이틀 배너: Title.png 원본 비율 완벽 유지 (잘림 없음) -->
                    <div class="hero-banner-wrap">
                        <img src="Title.png" alt="포트폴리오 타이틀 배너" class="hero-banner-img" onerror="this.style.display='none'">
                    </div>

                    <div class="hero-logline" contenteditable="false">
                        탄탄한 논리로 상상하는 <br><span>크리에이터 정승운</span>
                    </div>
                    <div class="hero-sub" contenteditable="false">
                        스토리보드와 시스템 기획, 유니티 바이브 코딩과 데이터 테이블 밸런싱까지.<br>
                        창작물의 핵심 뼈대를 구축하고 유저가 몰입할 수 있는 세계를 설계합니다.
                    </div>
                    <div style="display:flex; gap:12px; align-items:center;">
                        <button class="btn-primary" onclick="event.stopPropagation(); switchPage('portfolio', document.querySelectorAll('nav button')[2])">
                            포트폴리오 & 기획서 보러가기 →
                        </button>
                        <button class="btn-ghost" onclick="event.stopPropagation(); switchPage('resume', document.querySelectorAll('nav button')[1])">
                            이력 및 경력 확인
                        </button>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">STEP 01 / 03</span>
                    <span>화면의 빈 공간을 클릭하면 [핵심 강점]으로 이동합니다 →</span>
                </div>
            </div>

            <!-- Step 2: 핵심 강점 (3대 역량) -->
            <div class="main-step-container" id="main-step-2" onclick="handleStepClick(3)">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <h2 class="section-title" style="font-size:28px; margin:0;">핵심 역량 및 강점</h2>
                        <button class="home-shortcut-btn" onclick="event.stopPropagation(); handleStepClick(1)">처음으로 (STEP 1)</button>
                    </div>
                    <p class="section-desc">논리적 시스템 기획과 창의적인 세계관 구성, 디테일한 밸런싱을 아우릅니다.</p>

                    <div class="grid-3">
                        <div class="card-custom">
                            <div class="card-title" contenteditable="false">01. 시스템 설계 & 논리 구조</div>
                            <div class="card-desc" contenteditable="false">
                                AI 행동 트리(Behavior Tree) 구조 분리 및 상태 머신(FSM) 설계. 예외 상황을 원천 차단하고 시스템 간 상호작용을 정밀하게 기획합니다.
                            </div>
                        </div>
                        <div class="card-custom">
                            <div class="card-title" contenteditable="false">02. 데이터 테이블 & 밸런싱</div>
                            <div class="card-desc" contenteditable="false">
                                재배/제조/무역소/캐릭터 테이블을 직접 구조화하고 경제 순환 사이클과 시간 가치, 성장 곡선 밸런스 패치를 수행합니다.
                            </div>
                        </div>
                        <div class="card-custom">
                            <div class="card-title" contenteditable="false">03. 협업 총괄 & 프로덕션</div>
                            <div class="card-desc" contenteditable="false">
                                팀장 및 프로젝트 PD로서 일정 마일스톤 관리, QA 체크리스트 운용, 기획/아트/클라 간 명확한 커뮤니케이션으로 완성도를 극대화합니다.
                            </div>
                        </div>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">STEP 02 / 03</span>
                    <span>화면을 클릭하면 [하이라이트 요약]으로 이동합니다 →</span>
                </div>
            </div>

            <!-- Step 3: 하이라이트 요약 (플레이 히스토리 & 대표 프로젝트) -->
            <div class="main-step-container" id="main-step-3" onclick="handleStepClick(1)">
                <div>
                    <h2 class="section-title" style="font-size:28px; margin-bottom:8px;">하이라이트 요약</h2>
                    <p class="section-desc">플레이 히스토리와 대표 프로젝트의 핵심 컴포넌트입니다.</p>

                    <!-- 컴포넌트 1: 플레이 히스토리 요약 (IGDB 포스터 비율 3:4 완벽 적용) -->
                    <div class="component-block">
                        <div class="component-header">
                            <span class="component-title">플레이 히스토리 하이라이트</span>
                            <div style="display:flex; gap:8px;">
                                <button class="btn-ghost disabled" id="mainAddGameBtn" onclick="event.stopPropagation(); openGameSearchModal()">+ 게임 검색 추가 (편집모드)</button>
                                <button class="btn-ghost" onclick="event.stopPropagation(); switchPage('playhistory', document.querySelectorAll('nav button')[3])">전체 보기 ></button>
                            </div>
                        </div>
                        <div class="play-grid" id="main-play-grid">
                            <div class="play-card">
                                <div class="play-thumb">
                                    <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqr.jpg" alt="Sid Meier's Civilization VI">
                                </div>
                                <div class="play-content">
                                    <div class="play-title" contenteditable="false">Sid Meier's Civilization VI</div>
                                    <div class="play-meta">
                                        <div class="play-meta-row"><span>플랫폼: PC</span><span>1,200h+</span></div>
                                        <div>장르: Strategy / Simulation</div>
                                    </div>
                                </div>
                            </div>
                            <div class="play-card">
                                <div class="play-thumb">
                                    <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co73z1.jpg" alt="Football Manager 2024">
                                </div>
                                <div class="play-content">
                                    <div class="play-title" contenteditable="false">Football Manager 2024</div>
                                    <div class="play-meta">
                                        <div class="play-meta-row"><span>플랫폼: PC</span><span>950h+</span></div>
                                        <div>장르: Sports / Simulation</div>
                                    </div>
                                </div>
                            </div>
                            <div class="play-card">
                                <div class="play-thumb">
                                    <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqj.jpg" alt="RimWorld">
                                </div>
                                <div class="play-content">
                                    <div class="play-title" contenteditable="false">RimWorld</div>
                                    <div class="play-meta">
                                        <div class="play-meta-row"><span>플랫폼: PC</span><span>800h+</span></div>
                                        <div>장르: Simulation / Survival</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 컴포넌트 2: 대표 프로젝트 요약 (이미지 잘림 없는 contain 박스 적용) -->
                    <div class="component-block" style="margin-bottom:0;">
                        <div class="component-header">
                            <span class="component-title">대표 프로젝트 하이라이트</span>
                            <button class="btn-ghost" onclick="event.stopPropagation(); switchPage('portfolio', document.querySelectorAll('nav button')[2])">전체 포트폴리오 ></button>
                        </div>
                        <div class="main-project-grid">
                            <div class="main-project-card" onclick="event.stopPropagation(); openModal('project1')">
                                <div class="main-project-imgbox">
                                    <img src="lastsanctuary.png" alt="LAST SANCTUARY">
                                </div>
                                <div style="padding:18px 20px;">
                                    <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); margin-bottom:4px;">PC RPG • SYSTEM PLANNING</div>
                                    <div class="project-title" style="font-size:17px; margin-bottom:6px;" contenteditable="false">PC 게임 &lt;LAST SANCTUARY&gt;</div>
                                    <div class="project-desc" style="font-size:13px; margin:0;" contenteditable="false">전체 게임 시스템 기획, AI 행동 트리 로직 설계, 유니티 바이브 코딩 및 PV 제작</div>
                                </div>
                            </div>
                            <div class="main-project-card" onclick="event.stopPropagation(); openModal('project2')">
                                <div class="main-project-imgbox">
                                    <img src="슬기로운재배생활.png" alt="슬기로운 재배생활">
                                </div>
                                <div style="padding:18px 20px;">
                                    <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); margin-bottom:4px;">PC SIMULATION • TEAM LEAD</div>
                                    <div class="project-title" style="font-size:17px; margin-bottom:6px;" contenteditable="false">PC 게임 &lt;슬기로운 재배생활&gt;</div>
                                    <div class="project-desc" style="font-size:13px; margin:0;" contenteditable="false">팀장 총괄, 재배/가공/무역 시스템 설계, 5종 데이터 테이블 및 경제 밸런스 패치</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="main-nav-footer">
                    <span class="step-indicator">STEP 03 / 03</span>
                    <span>클릭 시 [처음 (STEP 1)]으로 순환 이동합니다 ↺</span>
                </div>
            </div>

        </section>

        <!-- 2. 이력 및 자기소개서 페이지 -->
        <section id="page-resume" class="page-section">
            <h1 class="section-title">이력 및 자기소개서</h1>
            <p class="section-desc">정승운의 회사 및 실무 경력, 학력, 보유 기술, 프로젝트 활동 내역입니다.</p>

            <div class="resume-tabs">
                <button class="sub-tab-btn active" onclick="switchResumeTab('resume-content', this)">이력서 정보 (회사 경력 포함)</button>
                <button class="sub-tab-btn" onclick="switchResumeTab('coverletter-content', this)">자기소개서</button>
            </div>

            <!-- 이력서 정보 탭 -->
            <div id="resume-content" class="sub-content active">
                <div class="resume-section-box">
                    <h3>인적 사항 및 연락처</h3>
                    <table class="table-custom">
                        <tr><th>성명</th><td contenteditable="false">정승운</td><th>생년월일</th><td contenteditable="false">2000.04.11</td></tr>
                        <tr><th>연락처</th><td contenteditable="false">010-9822-7714</td><th>이메일</th><td contenteditable="false">caddman771144@gmail.com</td></tr>
                        <tr><th>주소</th><td contenteditable="false" colspan="3">서울특별시 중구 동호로 28길 21 202호</td></tr>
                        <tr><th>병역</th><td contenteditable="false" colspan="3">군필 (육군 만기전역)</td></tr>
                    </table>
                </div>

                <div class="resume-section-box">
                    <h3>보유 기술 (사용 프로그램 및 툴)</h3>
                    <table class="table-custom">
                        <thead><tr><th>프로그램</th><th>숙련도</th><th>상세 역량 및 활용 범위</th></tr></thead>
                        <tbody>
                            <tr><td contenteditable="false">Unity (유니티)</td><td contenteditable="false" style="color:var(--color-iris-violet); font-weight:600;">중급</td><td contenteditable="false">바이브 코딩 및 C# 객체 시스템 구조 설정, FSM / 행동 트리 연동, UI 캔버스 구성</td></tr>
                            <tr><td contenteditable="false">Adobe Premiere Pro</td><td contenteditable="false" style="color:var(--color-iris-violet); font-weight:600;">고급 (상)</td><td contenteditable="false">게임 PV 티저 제작, 영상 컷 편집, 색보정(Lumetri), 사운드 믹싱 등 마스터링 가능</td></tr>
                            <tr><td contenteditable="false">Excel (데이터 테이블)</td><td contenteditable="false" style="color:var(--color-iris-violet); font-weight:600;">고급 (상)</td><td contenteditable="false">게임 시스템 밸런스 시트 수식 설계, 작물/제조/무역/캐릭터 수치 테이블 구축 및 검증</td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- 회사 및 실무 경력 -->
                <div class="resume-section-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <h3 style="margin-bottom:0;">회사 및 실무 경력 (Work Experience)</h3>
                        <span style="font-size:12px; font-family:var(--font-mono); color:var(--color-iris-violet);">* 정식 이력서 인증</span>
                    </div>
                    <table class="table-custom">
                        <thead>
                            <tr>
                                <th>회사 / 소속명</th>
                                <th>근무 부서 / 직책</th>
                                <th>담당 업무 및 주요 성과</th>
                                <th>근무 기간</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td contenteditable="false" style="font-weight:600; color:#fff;">디벨로켓</td>
                                <td contenteditable="false"><span style="color:var(--color-iris-violet);">팀장</span> / 게임 기획</td>
                                <td contenteditable="false">
                                    <strong>PC 게임 &lt;슬기로운 재배생활&gt; 팀장</strong><br>
                                    • 전체 게임 시스템 기획 및 코어 루프 설계<br>
                                    • 유니티 바이브 코딩 기반 인터랙션 구현<br>
                                    • 재배/제조/무역/설명 테이블 작업 및 경제 밸런스 패치 총괄
                                </td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2026.06 ~ 2026.11</td>
                            </tr>
                            <tr>
                                <td contenteditable="false" style="font-weight:600; color:#fff;">디벨로켓</td>
                                <td contenteditable="false">팀원 / 시스템 기획</td>
                                <td contenteditable="false">
                                    <strong>PC 게임 &lt;LAST SANCTUARY&gt; 핵심 기획</strong><br>
                                    • 전체 게임 시스템 기획 및 전투 AI 행동 트리 설계<br>
                                    • 유니티 바이브 코딩 로직 구현 및 테이블 시트 연동<br>
                                    • 퀘스트 기획, 캐릭터 기획, 밸런스 패치 및 번역 작업<br>
                                    • 게임 메인 공식 프로모션 비디오(PV) 제작
                                </td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2026.07 ~ 2026.11</td>
                            </tr>
                            <tr>
                                <td contenteditable="false" style="font-weight:600; color:#fff;">데블다이스 (Devildice)</td>
                                <td contenteditable="false">매장 관리 / 운영</td>
                                <td contenteditable="false">
                                    • 보드게임 매장 현장 운영 및 고객 응대<br>
                                    • 수백 종의 게임 룰 파악 및 고객 맞춤형 룰 설명(티칭)<br>
                                    • 재고 입출고 및 매장 자원 유지 관리
                                </td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2025.01 ~ 현재</td>
                            </tr>
                            <tr>
                                <td contenteditable="false" style="font-weight:600; color:#fff;">제임스 텍 (James Tech)</td>
                                <td contenteditable="false">구매팀 / 사원</td>
                                <td contenteditable="false">
                                    • 물류 관리 및 상품 입출고, 발송 프로세스 총괄<br>
                                    • 재고 수불 관리 및 배송 데이터베이스 트래킹<br>
                                    • 납기 일정 준수 및 공급사/고객사 커뮤니케이션
                                </td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2021.11 ~ 2024.01<br><small style="color:var(--color-ash-gray);">(2년 3개월)</small></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- 프로젝트 및 영상 제작 / 대외 활동 -->
                <div class="resume-section-box">
                    <h3>프로젝트 및 대외 활동 (Projects & Activities)</h3>
                    <table class="table-custom">
                        <thead><tr><th>소속 / 프로젝트명</th><th>담당 역할</th><th>주요 활동 내용</th><th>기간</th></tr></thead>
                        <tbody>
                            <tr>
                                <td contenteditable="false">2026 동국영화제</td>
                                <td contenteditable="false"><span style="color:var(--color-iris-violet);">운영팀장</span></td>
                                <td contenteditable="false">행사 현장 운영 총괄 및 계획 수립, 자원봉사자 모집/교육, MD 굿즈 발주 및 판매 관리</td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2025.09 ~ 2026.02</td>
                            </tr>
                            <tr>
                                <td contenteditable="false">동국대학교 졸업영화 &lt;개인 전시&gt;</td>
                                <td contenteditable="false"><strong>프로듀서 (PD)</strong></td>
                                <td contenteditable="false">로케이션 헌팅, 전체 예산 관리, 촬영 계획 수립, 현장 미술 지원 및 운영 총괄</td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2026.06 ~ 2026.11</td>
                            </tr>
                            <tr>
                                <td contenteditable="false">동국대학교 졸업영화 &lt;유산을 넘겨라, 아니!&gt;</td>
                                <td contenteditable="false"><strong>프로듀서 (PD)</strong></td>
                                <td contenteditable="false">로케이션 헌팅, 전체 예산 수립 및 실행, 촬영 현장 총괄 운영</td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2024.05 ~ 2024.12</td>
                            </tr>
                            <tr>
                                <td contenteditable="false">동국대학교 졸업영화 &lt;그날의 음모&gt;</td>
                                <td contenteditable="false"><strong>프로듀서 (PD)</strong></td>
                                <td contenteditable="false">예산 편성, 엑스트라 관리, 현장 스틸 촬영, 최종 보고서 취합 및 작성</td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2024.06 ~ 2024.12</td>
                            </tr>
                            <tr>
                                <td contenteditable="false">서울예술대학교 영화 &lt;각질&gt;</td>
                                <td contenteditable="false">데이터매니저</td>
                                <td contenteditable="false">촬영 현장 데이터 백업 및 무결성 관리, 현장 실시간 컷 편집 지원</td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2025.10 ~ 2025.12</td>
                            </tr>
                            <tr>
                                <td contenteditable="false">유튜브 채널 'PAPIC'</td>
                                <td contenteditable="false">크루원</td>
                                <td contenteditable="false">영상 콘텐츠 기획, 현장 촬영, 유튜브 영상 컷 편집 및 발행</td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2021.01 ~ 2022.01</td>
                            </tr>
                            <tr>
                                <td contenteditable="false">2020 동국영화제</td>
                                <td contenteditable="false">홍보팀원</td>
                                <td contenteditable="false">SNS 홍보 이벤트 기획, 공식 MD 굿즈 디자인, DUFF 홍보영상 제작</td>
                                <td contenteditable="false" style="font-family:var(--font-mono); font-size:13px;">2019.10 ~ 2020.02</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="resume-section-box">
                    <h3>학력 사항</h3>
                    <table class="table-custom">
                        <thead><tr><th>학교명</th><th>전공 / 학위</th><th>재학 기간</th><th>소재지</th><th>학점</th></tr></thead>
                        <tbody>
                            <tr><td contenteditable="false">동국대학교</td><td contenteditable="false">영화영상학과 (학사 졸업예정)</td><td contenteditable="false" style="font-family:var(--font-mono);">2019.01 ~ 현재</td><td contenteditable="false">서울 중구</td><td contenteditable="false">3.46 / 4.5</td></tr>
                            <tr><td contenteditable="false">광양제철고등학교</td><td contenteditable="false">인문계 졸업</td><td contenteditable="false" style="font-family:var(--font-mono);">2016.01 ~ 2019.01</td><td contenteditable="false">전남 광양시</td><td contenteditable="false">-</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 자기소개서 탭 -->
            <div id="coverletter-content" class="sub-content">
                <div class="resume-section-box">
                    <h3 contenteditable="false">1. 지원 동기: 상상을 실현하는 장으로서의 게임</h3>
                    <p contenteditable="false" style="line-height:1.7;">
                        상상력은 많은 것들을 가능하게 합니다. 어릴 때부터 책과 영화를 좋아했던 저는 언제나 상상 속의 세계에 빠져 있었고, 이런 공간을 창조하는 일을 하고 있는 저를 막연하게 떠올리곤 했습니다. 처음으로 접한 게임은 수동적으로 주어진 세계를 받아들일 수밖에 없는 이전의 문화 매체들과 다르게, 유저가 스스로 성장하고 다른 이들과 이야기를 나누며 세계를 창조하거나 이야기의 운명을 바꾸는 것도 가능하게 해주었습니다.<br><br>
                        능동적으로 행동하고 그에 따라 반응하는 유기적인 세계의 매력에 매료되었고, 영화와 영상 제작을 거쳐 게임 기획이라는 더 넓고 상호작용적인 무대에서 저만의 세계를 정밀하게 구축하고자 지원하게 되었습니다.
                    </p>
                </div>

                <div class="resume-section-box">
                    <h3 contenteditable="false">2. 직무 역량: 집요한 논리와 구조화된 데이터 설계</h3>
                    <p contenteditable="false" style="line-height:1.7;">
                        시스템 기획자에게 가장 중요한 것은 '아이디어를 수치와 규칙으로 번역하는 힘'입니다. PC 게임 &lt;LAST SANCTUARY&gt; 개발 중 유한 상태 기계의 한계로 인한 전투 버그를 발견했을 때, 저는 AI 로직을 행동 트리(Behavior Tree) 구조로 분리하고 각 노드의 실행 조건을 명확히 재정의하여 버그를 완벽히 해결했습니다.<br><br>
                        또한 &lt;슬기로운 재배생활&gt;에서는 작물 밸런스, 제조 레시피, 무역 시세 변동 등 복잡한 경제 수치를 엑셀 시트 수식으로 구조화하여 디벨로켓 프로젝트를 성공적으로 이끌었습니다.
                    </p>
                </div>

                <div class="resume-section-box">
                    <h3 contenteditable="false">3. 소통 및 협업 역량: 경청과 중재로 완성도를 높이다</h3>
                    <p contenteditable="false" style="line-height:1.7;">
                        영화 프로듀서(PD)와 게임 프로젝트 팀장을 거치며, 개발 과정의 갈등은 서로 다른 관점에서 게임을 더 좋게 만들려는 열정에서 비롯된다는 것을 배웠습니다. UI 리소스 과다 문제로 팀원 간 충돌이 일어났을 때, 타이머 시스템의 메커니즘을 시각적 다이어그램으로 설명하고 기존 리소스를 재가공하는 절충안을 제시하여 팀의 합의를 이끌어냈습니다.
                    </p>
                </div>

                <div class="resume-section-box">
                    <h3 contenteditable="false">4. 목표와 포부</h3>
                    <p contenteditable="false" style="line-height:1.7;">
                        기획은 단순히 만들고 싶은 것만 만드는 것이 아니라 판매할 상품을 만들고 대다수의 인원에게 흥미롭게 받아들여져야 합니다. 제가 창조한 세계의 문제점을 파악하고 피드백을 적극 수용하여 끊임없이 보완해 나감으로써, 노력의 진가를 증명하는 인정받는 기획자가 되겠습니다.
                    </p>
                </div>
            </div>
        </section>

        <!-- 3. 포트폴리오 페이지 (프로젝트 상세 + 기획서 문서함 탭) -->
        <section id="page-portfolio" class="page-section">
            <h1 class="section-title">포트폴리오 & 기획서 아카이브</h1>
            <p class="section-desc">직접 진행한 게임 개발 프로젝트와 실무 기획서·데이터 테이블 문서 일체를 열람하고 다운로드할 수 있습니다.</p>

            <!-- 포트폴리오 내부 서브 탭 -->
            <div class="portfolio-tabs">
                <button class="sub-tab-btn active" onclick="switchPortfolioTab('portfolio-projects', this)">대표 프로젝트 기획 (2종 + 영상)</button>
                <button class="sub-tab-btn" onclick="switchPortfolioTab('portfolio-docs', this)">기획서 및 데이터 문서함 (총 18종 연동)</button>
            </div>

            <!-- 3-1. 프로젝트 기획 목록 서브 탭: 이미지 잘림 없는 좌우 분할 와이드 카드 적용 -->
            <div id="portfolio-projects" class="sub-content active">
                
                <!-- 프로젝트 1: LAST SANCTUARY (630x500 이미지 원본 비율 완벽 수용) -->
                <div class="project-card-horizontal" onclick="openModal('project1')">
                    <div class="project-horizontal-imgbox">
                        <img src="lastsanctuary.png" alt="PC 게임 LAST SANCTUARY">
                    </div>
                    <div class="project-card-body">
                        <div>
                            <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-bottom:6px;">PC RPG / SYSTEM PLANNING & AI LOGIC</div>
                            <div class="project-title">PC 게임 &lt;LAST SANCTUARY&gt; 프로젝트 기획</div>
                            <div class="project-desc">
                                전체 게임 시스템 기획, 유니티 바이브 코딩, AI 행동 트리(Behavior Tree) 로직 설계, 캐릭터/퀘스트 기획 및 공식 프로모션 비디오(PV) 제작.
                            </div>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="btn-ghost" style="font-size:12px;">상세 기획서 열람 & 연동 문서 →</span>
                            <span style="font-family:var(--font-mono); font-size:11px; color:var(--color-ash-gray);">디벨로켓 (2026)</span>
                        </div>
                    </div>
                </div>

                <!-- 프로젝트 2: 슬기로운 재배생활 (941x627 이미지 원본 비율 완벽 수용) -->
                <div class="project-card-horizontal" onclick="openModal('project2')">
                    <div class="project-horizontal-imgbox">
                        <img src="슬기로운재배생활.png" alt="PC 게임 슬기로운 재배생활">
                    </div>
                    <div class="project-card-body">
                        <div>
                            <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-bottom:6px;">PC SIMULATION / TEAM LEAD & GAME DESIGN</div>
                            <div class="project-title">PC 게임 &lt;슬기로운 재배생활&gt; 프로젝트 기획</div>
                            <div class="project-desc">
                                팀장 총괄, 프로젝트 전체 시스템 기획, 유니티 바이브 코딩, 작물/제조/무역 데이터 시트 수립 및 경제 밸런스 패치 총괄.
                            </div>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="btn-ghost" style="font-size:12px;">상세 기획서 열람 & 연동 문서 →</span>
                            <span style="font-family:var(--font-mono); font-size:11px; color:var(--color-ash-gray);">팀 파송송계란탁 (2026)</span>
                        </div>
                    </div>
                </div>

                <!-- 프로젝트 3: 영화 제작 -->
                <div class="project-card-horizontal" onclick="openModal('project3')" style="grid-template-columns: 1fr;">
                    <div class="project-card-body">
                        <div>
                            <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-bottom:6px;">FILM PRODUCTION & PD / MANAGEMENT</div>
                            <div class="project-title">동국대학교 졸업 영화 &lt;개인 전시&gt; 및 다수 영상 프로덕션</div>
                            <div class="project-desc">
                                프로듀서(PD) 및 프로덕션 총괄: 예산안 수립 및 로케이션 헌팅, 타임테이블 관리, 미술 세팅 및 영화제 출품 운영.
                            </div>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="btn-ghost" style="font-size:12px;">제작 상세 내용 확인 →</span>
                            <span style="font-family:var(--font-mono); font-size:11px; color:var(--color-ash-gray);">동국대학교 영화영상학과</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3-2. 기획서 및 데이터 문서함 서브 탭 -->
            <div id="portfolio-docs" class="sub-content">
                <div style="margin-bottom:24px; padding:16px 20px; background:rgba(146,129,247,0.06); border:1px solid rgba(146,129,247,0.25); border-radius:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                    <div>
                        <div style="font-weight:600; color:#fff; font-size:15px; margin-bottom:4px;">📂 포트폴리오 문서 보관소 (실제 파일 연동 완료)</div>
                        <div style="font-size:13px; color:var(--color-ash-gray);">
                            포폴 정리용 폴더에 있는 모든 기획서 및 엑셀 데이터 테이블을 즉시 다운로드하거나 브라우저에서 바로 열람할 수 있습니다.
                        </div>
                    </div>
                    <div style="display:flex; gap:8px;">
                        <span style="font-size:12px; font-family:var(--font-mono); color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 10px; border-radius:4px; border:1px solid rgba(146,129,247,0.3);">
                            총 18개 문서 연동
                        </span>
                    </div>
                </div>

                <!-- 동적 렌더링 컨테이너 -->
                <div id="documentsArchiveContainer">
                    <div style="color:var(--color-ash-gray); text-align:center; padding:40px;">
                        ⏳ 문서를 불러오는 중입니다...
                    </div>
                </div>
            </div>

        </section>

        <!-- 4. 플레이 히스토리 페이지: IGDB 커버 3:4 세로 포스터 비율 적용 -->
        <section id="page-playhistory" class="page-section">
            <h1 class="section-title">플레이 히스토리</h1>
            <p class="section-desc">깊이 있게 플레이하며 게임 시스템과 기획적 인사이트를 얻은 게임 목록입니다. (IGDB 실시간 연동)</p>

            <div class="stats-overview">
                <div class="stat-box">
                    <h4>장르별 플레이 비중</h4>
                    <div class="stat-bar-item">
                        <div class="stat-bar-label"><span>시뮬레이션 / 전략 (Simulation / Strategy)</span><span>55%</span></div>
                        <div class="bar-bg"><div class="bar-fill" style="width: 55%;"></div></div>
                    </div>
                    <div class="stat-bar-item">
                        <div class="stat-bar-label"><span>RPG / 내러티브 (RPG / Narrative)</span><span>30%</span></div>
                        <div class="bar-bg"><div class="bar-fill" style="width: 30%;"></div></div>
                    </div>
                    <div class="stat-bar-item">
                        <div class="stat-bar-label"><span>기타 (Puzzle / Indie)</span><span>15%</span></div>
                        <div class="bar-bg"><div class="bar-fill" style="width: 15%;"></div></div>
                    </div>
                </div>
                <div class="stat-box">
                    <h4>플랫폼별 플레이 비중</h4>
                    <div class="stat-bar-item">
                        <div class="stat-bar-label"><span>PC (Steam / Simulation)</span><span>85%</span></div>
                        <div class="bar-bg"><div class="bar-fill" style="width: 85%;"></div></div>
                    </div>
                    <div class="stat-bar-item">
                        <div class="stat-bar-label"><span>Console / Mobile</span><span>15%</span></div>
                        <div class="bar-bg"><div class="bar-fill" style="width: 15%;"></div></div>
                    </div>
                </div>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
                <h3 style="font-size:18px; color:var(--color-white);">전체 플레이 게임 목록</h3>
                <button class="btn-ghost disabled" id="fullAddGameBtn" onclick="openGameSearchModal()">+ 게임 검색 추가 (편집모드용)</button>
            </div>

            <!-- 문명 6, FM 2024, 림월드, 팩토리오 등 IGDB 3:4 규격 포스터 완벽 표시 -->
            <div class="play-grid" id="full-play-grid">
                <div class="play-card">
                    <div class="play-thumb">
                        <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqr.jpg" alt="Sid Meier's Civilization VI">
                    </div>
                    <div class="play-content">
                        <div class="play-title" contenteditable="false">Sid Meier's Civilization VI (문명 6)</div>
                        <div class="play-meta">
                            <div class="play-meta-row"><span>플랫폼: PC</span><span style="color:#fff; font-weight:600;">1,200h+</span></div>
                            <div>장르: Turn-based Strategy</div>
                        </div>
                    </div>
                </div>
                <div class="play-card">
                    <div class="play-thumb">
                        <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co73z1.jpg" alt="Football Manager 2024">
                    </div>
                    <div class="play-content">
                        <div class="play-title" contenteditable="false">Football Manager 2024 (FM 2024)</div>
                        <div class="play-meta">
                            <div class="play-meta-row"><span>플랫폼: PC</span><span style="color:#fff; font-weight:600;">950h+</span></div>
                            <div>장르: Sports / Simulation</div>
                        </div>
                    </div>
                </div>
                <div class="play-card">
                    <div class="play-thumb">
                        <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqj.jpg" alt="RimWorld">
                    </div>
                    <div class="play-content">
                        <div class="play-title" contenteditable="false">RimWorld (림월드)</div>
                        <div class="play-meta">
                            <div class="play-meta-row"><span>플랫폼: PC</span><span style="color:#fff; font-weight:600;">800h+</span></div>
                            <div>장르: Simulation / Strategy</div>
                        </div>
                    </div>
                </div>
                <div class="play-card">
                    <div class="play-thumb">
                        <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co1tfy.jpg" alt="Factorio">
                    </div>
                    <div class="play-content">
                        <div class="play-title" contenteditable="false">Factorio (팩토리오)</div>
                        <div class="play-meta">
                            <div class="play-meta-row"><span>플랫폼: PC</span><span style="color:#fff; font-weight:600;">600h+</span></div>
                            <div>장르: Automation / Strategy</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

    <!-- 프로젝트 상세 모달 창 (배너 이미지 contain 처리로 잘림 방지) -->
    <div class="modal" id="projectModal">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal()">닫기 [X]</button>
            <div id="modalBody"></div>
        </div>
    </div>

    <!-- 게임 검색 및 추가 모달 창 (IGDB 실시간 연동) -->
    <div class="modal" id="gameSearchModal">
        <div class="modal-content" style="max-width: 680px;">
            <button class="modal-close" onclick="closeGameSearchModal()">닫기 [X]</button>
            <h2 style="font-size:22px; color:#fff; margin-bottom:8px;">IGDB 글로벌 게임 DB 실시간 검색</h2>
            <p style="font-size:13px; color:var(--color-ash-gray); margin-bottom:20px;">Twitch & IGDB 실시간 데이터베이스와 연동하여 커버 아트, 출시년도, 플랫폼, 장르를 검색해 플레이 목록에 추가합니다.</p>
            <div class="game-search-box">
                <input type="text" id="gameQueryInput" class="game-search-input" placeholder="게임 이름 입력 (예: Civilization, GTA, Dark Souls, Cyberpunk, 팰월드...)" oninput="filterGameListLive()">
            </div>
            <div class="game-search-results" id="gameSearchResults">
                <!-- 동적 렌더링 -->
            </div>
        </div>
    </div>

    <!-- JavaScript 기능 구현 -->
    <script>
        const API_BASE = 'http://localhost:3000';

        // 상단 네비게이션 페이지 전환
        function switchPage(pageId, btnElement) {
            document.querySelectorAll('.page-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('nav .nav-link').forEach(btn => btn.classList.remove('active'));
            
            const target = document.getElementById('page-' + pageId);
            if(target) target.classList.add('active');

            if(btnElement && btnElement.classList.contains('nav-link')) {
                btnElement.classList.add('active');
            } else if(pageId === 'main') {
                document.querySelectorAll('nav .nav-link')[0].classList.add('active');
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });

            if (pageId === 'portfolio') {
                loadPortfolioDocuments();
            }
        }

        // 메인 페이지 내부 스텝 전환
        function handleStepClick(nextStepNum) {
            if (isEditMode) return;

            document.querySelectorAll('.main-step-container').forEach(step => step.classList.remove('active'));
            document.getElementById('main-step-' + nextStepNum).classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // 이력/자기소개서 서브 탭 전환
        function switchResumeTab(tabId, btn) {
            document.querySelectorAll('#page-resume .sub-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('#page-resume .sub-tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }

        // 포트폴리오 서브 탭 전환 (프로젝트 / 기획서 문서함)
        function switchPortfolioTab(tabId, btn) {
            document.querySelectorAll('#page-portfolio .sub-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('#page-portfolio .sub-tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');

            if(tabId === 'portfolio-docs') {
                loadPortfolioDocuments();
            }
        }

        // 편집 모드 토글
        let isEditMode = false;
        function toggleEditMode() {
            isEditMode = !isEditMode;
            const btn = document.getElementById('editToggleBtn');
            const editables = document.querySelectorAll('[contenteditable]');
            const mainAddBtn = document.getElementById('mainAddGameBtn');
            const fullAddBtn = document.getElementById('fullAddGameBtn');
            
            if(isEditMode) {
                btn.classList.add('active');
                btn.innerText = '편집 모드 ON (저장)';
                editables.forEach(el => el.setAttribute('contenteditable', 'true'));
                
                mainAddBtn.classList.remove('disabled');
                mainAddBtn.innerText = '+ 게임 검색 추가';
                fullAddBtn.classList.remove('disabled');
                fullAddBtn.innerText = '+ 게임 검색 추가';
                
                alert('편집 모드가 활성화되었습니다. 텍스트 수정 및 IGDB 게임 추가가 가능합니다.');
            } else {
                btn.classList.remove('active');
                btn.innerText = '편집 모드 OFF';
                editables.forEach(el => el.setAttribute('contenteditable', 'false'));
                
                mainAddBtn.classList.add('disabled');
                mainAddBtn.innerText = '+ 게임 검색 추가 (편집모드)';
                fullAddBtn.classList.add('disabled');
                fullAddBtn.innerText = '+ 게임 검색 추가 (편집모드)';
                
                alert('편집 내용이 저장되고 편집 모드가 종료되었습니다.');
            }
        }

        // debounce 유틸
        let debounceTimer = null;
        function debounce(fn, delay) {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(fn, delay);
        }

        // 게임 검색 모달
        function openGameSearchModal() {
            if (!isEditMode) {
                alert('게임 추가 기능은 상단의 [편집 모드 ON] 상태에서만 이용할 수 있습니다.');
                return;
            }
            document.getElementById('gameSearchModal').style.display = 'block';
            document.getElementById('gameQueryInput').value = '';
            const container = document.getElementById('gameSearchResults');
            container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:30px; font-size:14px;">🔍 게임 이름을 입력하면 IGDB에서 실시간으로 검색합니다.</div>';
        }

        function closeGameSearchModal() {
            document.getElementById('gameSearchModal').style.display = 'none';
            clearTimeout(debounceTimer);
        }

        function renderGameSearchResults(games) {
            const container = document.getElementById('gameSearchResults');
            container.innerHTML = '';

            if (games.length === 0) {
                container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:24px;">일치하는 게임이 없습니다. 다른 검색어를 시도해보세요.</div>';
                return;
            }

            games.forEach(game => {
                const item = document.createElement('div');
                item.className = 'game-search-item';
                item.style.cssText = 'display:flex; align-items:center; gap:14px; padding:12px 16px; border-bottom:1px solid var(--color-graphite-hairline); cursor:pointer; transition:background 0.2s;';
                item.onmouseover = () => item.style.background = 'rgba(146,129,247,0.07)';
                item.onmouseout = () => item.style.background = '';

                const coverHtml = game.coverUrl
                    ? `<img src="${game.coverUrl}" alt="${game.title}" style="width:48px; height:64px; object-fit:cover; border-radius:6px; flex-shrink:0; border:1px solid var(--color-graphite-hairline);">`
                    : `<div style="width:48px; height:64px; background:#18181b; border-radius:6px; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:10px; color:var(--color-ash-gray); text-align:center;">NO<br>IMG</div>`;

                const yearText = game.releaseYear ? ` (${game.releaseYear})` : '';
                const platformText = game.platform !== '정보 없음' ? game.platform : '-';
                const genreText = game.genre !== '정보 없음' ? game.genre : '-';

                item.innerHTML = `
                    ${coverHtml}
                    <div style="flex:1; min-width:0;">
                        <span class="live-search-badge">IGDB LIVE</span>
                        <div style="font-weight:600; color:#fff; font-size:14px; margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${game.title}${yearText}</div>
                        <div style="font-size:11px; color:var(--color-ash-gray); font-family:var(--font-mono); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">플랫폼: ${platformText}</div>
                        <div style="font-size:11px; color:var(--color-ash-gray); font-family:var(--font-mono); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">장르: ${genreText}</div>
                    </div>
                    <button class="btn-ghost" style="padding:6px 14px; font-size:12px; flex-shrink:0;">추가</button>
                `;
                item.onclick = () => addSelectedGame(game);
                container.appendChild(item);
            });
        }

        async function filterGameListLive() {
            const query = document.getElementById('gameQueryInput').value.trim();
            const container = document.getElementById('gameSearchResults');

            if (!query) {
                container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:30px; font-size:14px;">🔍 게임 이름을 입력하면 IGDB에서 실시간으로 검색합니다.</div>';
                return;
            }

            debounce(async () => {
                container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:30px;"><span style="font-size:20px;">⏳</span><br>IGDB에서 검색 중...</div>';
                try {
                    const res = await fetch(`${API_BASE}/api/search-games?q=${encodeURIComponent(query)}`);
                    if (!res.ok) {
                        const err = await res.json();
                        throw new Error(err.error || '서버 오류');
                    }
                    const games = await res.json();
                    renderGameSearchResults(games);
                } catch (e) {
                    container.innerHTML = `<div style="color:#ff6b6b; text-align:center; padding:20px;">⚠️ 검색 실패: ${e.message}<br><small style="color:var(--color-ash-gray);">서버가 실행 중인지 확인해주세요 (node server.js)</small></div>`;
                }
            }, 300);
        }

        function addSelectedGame(game) {
            const mainGrid = document.getElementById('main-play-grid');
            if (mainGrid) mainGrid.appendChild(createPlayCardElement(game));

            const fullGrid = document.getElementById('full-play-grid');
            if (fullGrid) fullGrid.appendChild(createPlayCardElement(game));

            closeGameSearchModal();
            alert(`[${game.title}] 게임이 플레이 히스토리에 성공적으로 추가되었습니다.`);
        }

        function createPlayCardElement(game) {
            const card = document.createElement('div');
            card.className = 'play-card';

            const thumbContent = game.coverUrl
                ? `<img src="${game.coverUrl}" alt="${game.title}">`
                : `<span style="font-family:var(--font-mono); font-size:12px; color:var(--color-ash-gray);">${game.title.split(' ')[0].toUpperCase()}</span>`;

            const genreFirst = game.genre && game.genre !== '정보 없음'
                ? game.genre.split('/')[0].trim()
                : '-';
            const platformText = game.platform && game.platform !== '정보 없음'
                ? game.platform.split('/')[0].trim()
                : '-';
            const yearText = game.releaseYear ? ` (${game.releaseYear})` : '';
            const hoursText = game.hours || '추가됨';

            card.innerHTML = `
                <div class="play-thumb">${thumbContent}</div>
                <div class="play-content">
                    <div class="play-title" contenteditable="${isEditMode}">${game.title}${yearText}</div>
                    <div class="play-meta">
                        <div class="play-meta-row"><span contenteditable="${isEditMode}">플랫폼: ${platformText}</span><span contenteditable="${isEditMode}">${hoursText}</span></div>
                        <div contenteditable="${isEditMode}">장르: ${genreFirst}</div>
                    </div>
                </div>
            `;
            return card;
        }

        // 포트폴리오 기획서 문서 로드
        let documentsLoaded = false;
        async function loadPortfolioDocuments() {
            const container = document.getElementById('documentsArchiveContainer');
            if (!container || documentsLoaded) return;

            try {
                const res = await fetch(`${API_BASE}/api/portfolio-documents`);
                if (!res.ok) throw new Error('문서 목록을 불러오지 못했습니다.');
                const categories = await res.json();
                renderPortfolioDocuments(categories);
                documentsLoaded = true;
            } catch (e) {
                console.error('문서 로드 실패:', e);
                renderFallbackDocuments();
            }
        }

        function renderPortfolioDocuments(categories) {
            const container = document.getElementById('documentsArchiveContainer');
            container.innerHTML = '';

            categories.forEach(cat => {
                const block = document.createElement('div');
                block.className = 'doc-category-block';

                let itemsHtml = '';
                cat.items.forEach(item => {
                    const typeLower = item.type.toLowerCase();
                    const badgeClass = typeLower === 'pdf' ? 'pdf' : (typeLower === 'pptx' ? 'pptx' : 'xlsx');
                    
                    const previewBtn = item.type === 'PDF'
                        ? `<a href="${item.url}" target="_blank" class="btn-ghost" style="padding:4px 10px; font-size:11px;">열람 ↗</a>`
                        : '';
                    const downloadBtn = `<a href="${item.url}" class="btn-primary" style="padding:4px 12px; font-size:11px; text-decoration:none;">다운로드</a>`;

                    itemsHtml += `
                        <div class="doc-card">
                            <div>
                                <div class="doc-header-row">
                                    <div class="doc-title">${item.title}</div>
                                    <span class="doc-type-badge ${badgeClass}">${item.type}</span>
                                </div>
                                <div class="doc-desc">${item.desc}</div>
                            </div>
                            <div class="doc-footer-row">
                                <span>${item.sizeFormatted || ''} • ${item.project}</span>
                                <div class="doc-btn-group">
                                    ${previewBtn}
                                    ${downloadBtn}
                                </div>
                            </div>
                        </div>
                    `;
                });

                block.innerHTML = `
                    <div class="doc-category-header">
                        <div class="doc-category-title">${cat.category}</div>
                        <span class="doc-category-badge">${cat.badge}</span>
                    </div>
                    <div class="doc-grid">
                        ${itemsHtml}
                    </div>
                `;
                container.appendChild(block);
            });
        }

        function renderFallbackDocuments() {
            const container = document.getElementById('documentsArchiveContainer');
            container.innerHTML = `
                <div style="padding:20px; border:1px dashed var(--color-graphite-hairline); border-radius:12px; text-align:center;">
                    <div style="color:#fff; font-weight:600; margin-bottom:8px;">기획서 및 데이터 테이블 파일 바로가기</div>
                    <p style="color:var(--color-ash-gray); font-size:13px; margin-bottom:16px;">서버(node server.js)를 실행하시면 실시간 미리보기 및 다운로드가 활성화됩니다.</p>
                    <a href="/portfolio-assets/포트폴리오/" target="_blank" class="btn-primary">폴더 파일 직접 보기</a>
                </div>
            `;
        }

        // 프로젝트 상세 모달 데이터 (모달 배너 이미지도 잘림 없이 contain 처리)
        const projectData = {
            project1: `
                <div class="modal-banner-wrap">
                    <img src="lastsanctuary.png" alt="PC 게임 LAST SANCTUARY">
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                    <div>
                        <span class="live-search-badge" style="font-size:11px;">PC RPG • SYSTEM DESIGN</span>
                        <h2 style="font-size:24px; color:#fff; margin-top:4px;">PC 게임 &lt;LAST SANCTUARY&gt; 상세 기획서</h2>
                    </div>
                </div>

                <div class="detail-block">
                    <h4>1. 프로젝트 개요 및 기획서 연동</h4>
                    <p>
                        • 장르: PC 로그라이크/전략 RPG<br>
                        • 담당 업무: 전체 게임 시스템 기획, 유니티 바이브 코딩, AI 행동 트리 설계, 퀘스트/캐릭터 기획, 밸런스 패치, 공식 PV 티저 제작<br>
                        • 기획 연동: 행동 트리 기반 전투 AI 분리 설계 및 수치 테이블 시트 연동 완료
                    </p>
                    <div style="margin-top:12px;">
                        <span style="font-size:12px; color:var(--color-white); font-weight:600;">📁 관련 기획서 및 테이블 바로가기:</span>
                        <div class="modal-doc-links">
                            <a href="/api/download?file=20260722_7-5_%EC%BB%A8%EC%85%89%EA%B8%B0%ED%9A%8D%EC%84%9C_Ver05_%ED%8C%8C%EC%86%A1%EC%86%A1%EA%B3%84%EB%9E%80%ED%83%81%20(1).pdf" target="_blank" class="btn-ghost" style="font-size:11px;">📄 컨셉 기획서 (PDF 열람)</a>
                            <a href="/api/download?file=20260810_%EC%BA%90%EB%A6%AD%ED%84%B0%EA%B0%80%EC%9D%B4%EB%93%9C_Ver02_%ED%8C%8C%EC%86%A1%EC%86%A1%EA%B3%84%EB%9E%80%ED%83%81.pptx" class="btn-ghost" style="font-size:11px;">📊 캐릭터 가이드 (PPTX)</a>
                            <a href="/api/download?file=%EC%BA%90%EB%A6%AD%ED%84%B0%ED%85%8C%EC%9D%B4%EB%B8%94.xlsx" class="btn-ghost" style="font-size:11px;">📈 캐릭터 스탯 테이블 (XLSX)</a>
                        </div>
                    </div>
                </div>

                <div class="detail-block">
                    <h4>2. 문제 인식 및 목표</h4>
                    <p>전투 시뮬레이션 과정에서 유한 상태 머신(FSM)이 단일 로직으로 통합되어 있어 돌발 예외 상황 발생 시 캐릭터가 오동작하고 멈추는 문제 확인. 전투 AI의 정밀한 상태 분리 및 완벽한 시스템 안정성 확보가 목표.</p>
                </div>

                <div class="detail-block">
                    <h4>3. 해결 방법 및 시스템 구축</h4>
                    <ul>
                        <li>하나로 통합되어 있던 AI 스크립트를 행동 트리(Behavior Tree) 구조로 분리 재설계</li>
                        <li>Selector, Sequence, Condition 노드를 명확히 계층화하여 우선순위 기반 판단 로직 구성</li>
                        <li>기능별 단위 테스트 체크리스트 작성 및 반복 빌드 테스트를 통해 버그 완벽 차단</li>
                    </ul>
                </div>

                <div class="detail-block">
                    <h4>4. 개선점 및 성과</h4>
                    <p>명확한 논리 구조 설계와 예외 사전 처리의 절대적 중요성을 체득하였으며, 유니티 바이브 코딩을 통해 직관적이고 견고한 게임 시스템을 완성함.</p>
                </div>
            `,
            project2: `
                <div class="modal-banner-wrap">
                    <img src="슬기로운재배생활.png" alt="PC 게임 슬기로운 재배생활">
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                    <div>
                        <span class="live-search-badge" style="font-size:11px;">PC SIMULATION • TEAM LEAD</span>
                        <h2 style="font-size:24px; color:#fff; margin-top:4px;">PC 게임 &lt;슬기로운 재배생활&gt; 상세 기획서</h2>
                    </div>
                </div>

                <div class="detail-block">
                    <h4>1. 프로젝트 개요 및 기획서 연동</h4>
                    <p>
                        • 장르: 힐링 농업 & 경영 시뮬레이션 PC 게임<br>
                        • 담당 업무: 팀장 총괄, 전체 게임 코어 루프 기획, UI 화면 와이어프레임, 유니티 바이브 코딩, 5개 데이터 테이블 및 밸런스 패치 총괄<br>
                        • 연동 문서: 컨셉 기획서, 비주얼 가이드, UI화면기획, 시스템기획서, 마일스톤, QA시트, 엑셀 5종 테이블
                    </p>
                    <div style="margin-top:12px;">
                        <span style="font-size:12px; color:var(--color-white); font-weight:600;">📁 연동 기획서 및 데이터 시트 다운로드:</span>
                        <div class="modal-doc-links">
                            <a href="/api/download?file=0705_%EC%8A%AC%EA%B8%B0%EB%A1%9C%EC%9A%B4%EC%9E%AC%EB%B0%B0%EC%83%9D%ED%99%9C%EC%BB%A8%EC%85%89%EA%B8%B0%ED%9A%8D%EC%84%9C_Ver01.pdf" target="_blank" class="btn-ghost" style="font-size:11px;">📄 컨셉기획서 (PDF)</a>
                            <a href="/api/download?file=0709_UI%ED%99%94%EB%A9%B4%EA%B8%B0%ED%9A%8D_ver05.pdf" target="_blank" class="btn-ghost" style="font-size:11px;">🖥️ UI화면기획서 (PDF)</a>
                            <a href="/api/download?file=0718_%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B8%B0%ED%9A%8D%EC%84%9C_Ver03.pdf" target="_blank" class="btn-ghost" style="font-size:11px;">⚙️ 시스템기획서 (PDF)</a>
                            <a href="/api/download?file=%EC%9E%AC%EB%B0%B0%ED%85%8C%EC%9D%B4%EB%B8%94.xlsx" class="btn-ghost" style="font-size:11px;">🌱 재배 테이블 (XLSX)</a>
                            <a href="/api/download?file=%EB%AC%B4%EC%97%AD%EC%86%8C%20%ED%85%8C%EC%9D%B4%EB%B8%94.xlsx" class="btn-ghost" style="font-size:11px;">💰 무역소 시세 테이블 (XLSX)</a>
                        </div>
                    </div>
                </div>

                <div class="detail-block">
                    <h4>2. 문제 인식 및 목표</h4>
                    <p>각 생산 슬롯별 타이머 UI 표기 과정에서 리소스 과다 사용 우려로 팀원 간 의견 충돌 발생. 시각적 가독성과 게임 엔진 리소스 절감을 동시에 충족하는 최적화 구조 도출이 목표.</p>
                </div>

                <div class="detail-block">
                    <h4>3. 해결 방법</h4>
                    <ul>
                        <li>타이머 시간이 상이한 시스템 특성을 논리적으로 설명하고 데이터 시트로 팀원 설득</li>
                        <li>기존 타 UI 타이머 리소스를 쉐이더 및 색상만 변경하여 재활용하는 절충안 도출</li>
                        <li>팀원 간 충분한 소통과 마일스톤 관리를 통해 일정 내 전 기능 완성</li>
                    </ul>
                </div>

                <div class="detail-block">
                    <h4>4. 개선점 및 배운 점</h4>
                    <p>팀장으로서 갈등 상황을 상호 이해와 기획 완성도를 높이는 기회로 삼는 능동적인 소통 방식을 확립함.</p>
                </div>
            `,
            project3: `
                <h2 style="font-size:24px; color:#fff; margin-bottom:16px;">동국대학교 졸업 영화 &lt;개인 전시&gt; 프로덕션 및 영상 제작</h2>
                <div class="detail-block">
                    <h4>1. 작업 문서 및 연동</h4>
                    <p>• 예산안 및 촬영 계획서 (PDF / Excel 연동 완료)<br>• 2026 동국영화제 운영 관리 계획서</p>
                </div>
                <div class="detail-block">
                    <h4>2. 프로듀서(PD) 담당 업무</h4>
                    <ul>
                        <li>로케이션 헌팅 및 촬영 현장 운영 총괄</li>
                        <li>전체 예산 편성, 지출 통제 및 최종 예산안 작성·보고</li>
                        <li>현장 미술 지원 및 카메라/조명/배우 타임테이블 조율</li>
                    </ul>
                </div>
                <div class="detail-block">
                    <h4>3. 배운 점</h4>
                    <p>돌발 변수가 많은 현장을 논리적으로 통제하는 예산 관리 능력과 팀원 간 협업 조율 능력을 체득하여 게임 프로젝트 관리에도 동일하게 적용함.</p>
                </div>
            `
        };

        function openModal(projectId) {
            const modal = document.getElementById('projectModal');
            document.getElementById('modalBody').innerHTML = projectData[projectId] || "<p>내용이 없습니다.</p>";
            modal.style.display = 'block';
        }

        function closeModal() {
            document.getElementById('projectModal').style.display = 'none';
        }

        window.onclick = function(event) {
            const modal = document.getElementById('projectModal');
            const gameModal = document.getElementById('gameSearchModal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
            if (event.target === gameModal) {
                gameModal.style.display = 'none';
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            loadPortfolioDocuments();
        });
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("index.html successfully updated with perfect image aspect ratios and fit!")
