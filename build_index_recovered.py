# build_index.py - 완전 개편: 이력 소개(5단계 풀캔버스 순환) / 자기소개서 분리 / 삼각 파라미터 복구 / 밝아진 main2

html_code = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>정승운 포트폴리오 - 탄탄한 논리로 상상하는 크리에이터</title>
    <!-- Pretendard 및 Google Fonts 로드 -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <link href="https://fonts.googleapis.com/css2?family=Commit+Mono:ital,wght@0,400..700;1,400..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --color-void-black: #000000;
            --color-carbon: #08090d;
            --color-dark-panel: #10121a;
            --color-graphite-hairline: #292d30;
            --color-white: #ffffff;
            --color-bone-white: #f0f0f0;
            --color-ash-gray: #a1a4a5;
            --color-iris-violet: #9281f7;
            --color-iris-glow: rgba(146, 129, 247, 0.3);
            --font-main: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'Commit Mono', monospace;
            --radius-cards: 16px;
            --radius-buttons: 8px;
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
            background-image: radial-gradient(circle at 50% 0%, rgba(146, 129, 247, 0.09) 0%, transparent 65%);
            background-attachment: fixed;
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
            background: rgba(0, 0, 0, 0.93);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--color-graphite-hairline);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 36px;
        }

        .logo {
            font-family: var(--font-mono);
            font-size: 14px;
            color: var(--color-white);
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: 0.05em;
        }

        .logo:hover {
            color: var(--color-iris-violet);
        }

        nav {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .nav-link {
            background: transparent;
            border: none;
            color: var(--color-bone-white);
            font-size: 14px;
            font-family: var(--font-main);
            cursor: pointer;
            transition: all 0.25s ease;
            padding: 8px 14px;
            border-radius: var(--radius-buttons);
            font-weight: 500;
        }

        .nav-link:hover, .nav-link.active {
            color: var(--color-white);
            background: rgba(146, 129, 247, 0.16);
            border: 1px solid rgba(146, 129, 247, 0.4);
            text-shadow: 0 0 10px rgba(146, 129, 247, 0.5);
        }

        .edit-toggle-btn {
            background: transparent;
            border: 1px dashed var(--color-ash-gray);
            color: var(--color-ash-gray);
            padding: 6px 14px;
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

        .container {
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 100px 24px 80px;
            min-height: 100vh;
        }

        .section-title {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 8px;
            color: var(--color-white);
        }

        .section-desc {
            color: var(--color-ash-gray);
            font-size: 15px;
            margin-bottom: 32px;
        }

        [contenteditable="true"] {
            outline: 1px dashed rgba(146, 129, 247, 0.7);
            background: rgba(146, 129, 247, 0.08);
            border-radius: 4px;
            cursor: text;
        }

        /* -------------------------------------------------------------------
           메인 페이지 캔버스 (Step 1, Step 2)
        ------------------------------------------------------------------- */
        .main-step-container {
            display: none;
            min-height: 70vh;
            flex-direction: column;
            justify-content: center;
            animation: fadeIn 0.4s ease-in-out;
            cursor: pointer;
        }
        .main-step-container.active {
            display: flex;
        }

        .canvas-step-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
            border-top: 1px solid var(--color-graphite-hairline);
            padding-top: 18px;
            font-family: var(--font-mono);
            font-size: 13px;
            color: var(--color-ash-gray);
        }

        .step-indicator-tag {
            color: var(--color-iris-violet);
            font-weight: 600;
        }

        .hero-canvas-step1 {
            width: 100%;
            min-height: 600px;
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--color-graphite-hairline);
            background-color: #030406;
            background-image: url('main 1.png');
            background-repeat: no-repeat;
            background-position: right center;
            background-size: contain;
            display: flex;
            align-items: center;
            padding: 50px 60px;
            position: relative;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
            cursor: pointer;
            transition: border-color 0.3s ease;
        }

        .hero-text-overlay {
            max-width: 50%;
            width: 100%;
            z-index: 2;
            display: flex;
            flex-direction: column;
        }

        .hero-logline {
            font-size: 42px;
            font-weight: 700;
            line-height: 1.28;
            letter-spacing: -0.03em;
            color: var(--color-white);
            margin-bottom: 20px;
        }

        .hero-logline span {
            color: var(--color-iris-violet);
            text-shadow: 0 0 20px rgba(146, 129, 247, 0.5);
        }

        .hero-sub {
            font-size: 16px;
            color: var(--color-ash-gray);
            line-height: 1.75;
            word-break: keep-all;
        }

        /* 메인 2 캔버스: 사용자 요청에 따라 어둡지 않고 밝게 가시성 개선 */
        .hero-canvas-step2 {
            width: 100%;
            min-height: 600px;
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--color-graphite-hairline);
            background-color: #05070a;
            background-image: linear-gradient(180deg, rgba(3,4,6,0.35) 0%, rgba(3,4,6,0.45) 100%), url('main2.png');
            background-repeat: no-repeat;
            background-position: center center;
            background-size: cover;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 44px 50px;
            position: relative;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
            cursor: pointer;
            text-align: center;
        }

        .ph-nav-buttons {
            display: flex;
            gap: 16px;
            justify-content: center;
            margin-top: 32px;
            flex-wrap: wrap;
        }

        .ph-nav-btn {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 13px 26px;
            border-radius: 12px;
            border: 1px solid var(--color-graphite-hairline);
            background: rgba(10,12,18,0.75);
            backdrop-filter: blur(10px);
            color: var(--color-bone-white);
            font-family: var(--font-main);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .ph-nav-btn:hover {
            border-color: var(--color-iris-violet);
            background: rgba(146,129,247,0.2);
            transform: translateY(-2px);
            color: var(--color-white);
            box-shadow: 0 8px 24px rgba(146, 129, 247, 0.25);
        }

        .ph-nav-btn-primary {
            border-color: var(--color-iris-violet);
            background: rgba(146,129,247,0.3);
            color: #fff;
            box-shadow: 0 0 16px rgba(146, 129, 247, 0.35);
        }

        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 22px;
            margin-bottom: 24px;
        }

        .card-glass {
            background: rgba(8, 10, 16, 0.82);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(146, 129, 247, 0.3);
            border-radius: 14px;
            padding: 24px;
            transition: all 0.25s ease;
        }

        .card-glass:hover {
            border-color: var(--color-iris-violet);
            background: rgba(16, 19, 30, 0.92);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(146, 129, 247, 0.25);
        }

        .card-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--color-white);
            margin-bottom: 10px;
        }

        .card-desc {
            font-size: 13.5px;
            color: var(--color-ash-gray);
            line-height: 1.65;
        }

        /* -------------------------------------------------------------------
           이력 소개 풀 캔버스 5단계 인터랙티브 쇼케이스
           (메인 페이지처럼 화면 꽉 차게, 숫자로 순서 표시, 5단계 후 1단계 순환)
        ------------------------------------------------------------------- */
        .resume-step-canvas {
            display: none;
            min-height: 640px;
            width: 100%;
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--color-graphite-hairline);
            padding: 50px 60px;
            position: relative;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
            cursor: pointer;
            animation: fadeIn 0.4s ease-in-out;
            background-size: cover;
            background-position: center;
        }

        .resume-step-canvas.active {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* 상단 순서 탭 바 (01 ~ 05) */
        .resume-step-navigator {
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
            align-items: center;
        }

        .step-num-pill {
            font-family: var(--font-mono);
            font-size: 13px;
            font-weight: 600;
            padding: 8px 18px;
            border-radius: 20px;
            border: 1px solid var(--color-graphite-hairline);
            background: rgba(255, 255, 255, 0.04);
            color: var(--color-ash-gray);
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .step-num-pill:hover, .step-num-pill.active {
            background: rgba(146, 129, 247, 0.2);
            border-color: var(--color-iris-violet);
            color: #fff;
            box-shadow: 0 0 12px rgba(146, 129, 247, 0.3);
        }

        /* Slide 1: Profile (main 2 밝은 배경 + 좌측 투명배경 인물 + 우측 인적사항) */
        .resume-canvas-1 {
            background-color: #06080d;
            background-image: linear-gradient(90deg, rgba(4,6,9,0.7) 0%, rgba(4,6,9,0.5) 50%, rgba(4,6,9,0.7) 100%), url('main2.png');
        }

        .profile-flex-wrap {
            display: flex;
            align-items: center;
            gap: 50px;
            width: 100%;
        }

        .profile-photo-wrap {
            flex-shrink: 0;
            width: 290px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .profile-glow-circle {
            position: absolute;
            width: 280px;
            height: 360px;
            background: radial-gradient(circle, rgba(146, 129, 247, 0.4) 0%, transparent 70%);
            z-index: 0;
            filter: blur(24px);
        }

        .profile-cutout-img {
            position: relative;
            z-index: 1;
            width: 100%;
            max-height: 440px;
            object-fit: contain;
            filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        }

        .profile-content-wrap {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            z-index: 2;
        }

        .stagger-item {
            opacity: 0;
            transform: translateY(14px);
            animation: staggerFade 0.55s ease forwards;
        }
        .stagger-1 { animation-delay: 0.1s; }
        .stagger-2 { animation-delay: 0.25s; }
        .stagger-3 { animation-delay: 0.4s; }
        .stagger-4 { animation-delay: 0.55s; }
        .stagger-5 { animation-delay: 0.7s; }

        @keyframes staggerFade {
            to { opacity: 1; transform: translateY(0); }
        }

        .profile-title-name {
            font-size: 40px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 6px;
            letter-spacing: -0.02em;
        }

        .profile-title-name span {
            color: var(--color-iris-violet);
            font-family: var(--font-mono);
            font-size: 18px;
            font-weight: 500;
            margin-left: 12px;
        }

        .role-badge-pill {
            display: inline-block;
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--color-iris-violet);
            background: rgba(146, 129, 247, 0.15);
            border: 1px solid rgba(146, 129, 247, 0.35);
            padding: 4px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
            width: fit-content;
        }

        .profile-table-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            background: rgba(12, 14, 22, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 22px;
            backdrop-filter: blur(12px);
        }

        .info-cell {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .info-label-txt {
            font-size: 11.5px;
            font-family: var(--font-mono);
            color: var(--color-ash-gray);
            text-transform: uppercase;
        }

        .info-val-txt {
            font-size: 14.5px;
            font-weight: 600;
            color: #fff;
        }

        /* Slide 2: 보유 기술 및 툴 아이콘 중앙 정렬 */
        .resume-canvas-2, .resume-canvas-3, .resume-canvas-5 {
            background-color: #07080d;
            text-align: center;
            align-items: center;
        }

        .tools-center-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 24px;
            margin: 32px 0 34px;
            flex-wrap: wrap;
        }

        .tool-icon-box {
            width: 135px;
            background: rgba(14, 16, 24, 0.85);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 16px;
            padding: 22px 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            transition: all 0.25s ease;
        }

        .tool-icon-box:hover {
            border-color: var(--color-iris-violet);
            background: rgba(24, 27, 40, 0.95);
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(146, 129, 247, 0.25);
        }

        .tool-icon-box img, .tool-icon-box svg {
            width: 54px;
            height: 54px;
            object-fit: contain;
            filter: drop-shadow(0 4px 10px rgba(0,0,0,0.6));
        }

        .tool-tag-txt {
            font-size: 13px;
            font-weight: 600;
            color: #fff;
        }

        .tool-level-badge {
            font-size: 11px;
            font-family: var(--font-mono);
            color: var(--color-iris-violet);
            background: rgba(146, 129, 247, 0.15);
            padding: 2px 8px;
            border-radius: 4px;
        }

        .tools-desc-grid {
            max-width: 960px;
            width: 100%;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            text-align: left;
        }

        .tool-desc-card {
            background: rgba(11, 13, 20, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 18px 20px;
        }

        .tool-desc-card h4 {
            font-size: 14.5px;
            color: #fff;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tool-desc-card p {
            font-size: 12.5px;
            color: var(--color-ash-gray);
            line-height: 1.6;
        }

        /* Slide 3: 프로젝트 & 경력 로고 */
        .project-logos-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            width: 100%;
            max-width: 1100px;
            margin-top: 32px;
        }

        .career-milestone-box {
            background: rgba(13, 15, 22, 0.88);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 16px;
            padding: 24px 18px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            transition: all 0.3s ease;
        }

        .career-milestone-box:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(146, 129, 247, 0.22);
        }

        .career-logo-container {
            width: 100%;
            height: 90px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 10px;
        }

        .career-logo-container img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        /* Slide 4: 영화 연출 & 카메라 애니메이션 (방향 수정: 왼쪽 영화 목록을 향하도록) */
        .resume-canvas-4 {
            background-color: #040508;
        }

        .cinema-flex-container {
            display: flex;
            align-items: center;
            gap: 40px;
            width: 100%;
        }

        .movie-scroll-col {
            flex: 1.25;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 480px;
            overflow-y: auto;
            padding-right: 14px;
        }

        .movie-scroll-col::-webkit-scrollbar {
            width: 6px;
        }
        .movie-scroll-col::-webkit-scrollbar-thumb {
            background: var(--color-graphite-hairline);
            border-radius: 3px;
        }

        .movie-strip-item {
            background: rgba(13, 15, 23, 0.92);
            border: 1px solid var(--color-graphite-hairline);
            border-left: 4px solid var(--color-iris-violet);
            border-radius: 10px;
            padding: 14px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.25s ease;
        }

        .movie-strip-item:hover {
            border-color: var(--color-iris-violet);
            background: rgba(22, 25, 38, 0.98);
            transform: translateX(6px);
        }

        /* 35mm 카메라 애니메이션 (왼쪽 영사 방향으로 반전) */
        .camera-anim-col {
            flex: 0.85;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .camera-facing-left {
            transform: scaleX(-1); /* 카메라와 렌즈 방향을 왼쪽 영화 목록으로 반전 */
            width: 250px;
            height: 250px;
        }

        .lens-light-beam-left {
            position: absolute;
            right: 180px; /* 반전된 렌즈에서 왼쪽 영화 목록 쪽으로 뻗는 빛 */
            top: 90px;
            width: 240px;
            height: 140px;
            background: linear-gradient(270deg, rgba(146, 129, 247, 0.5) 0%, rgba(146, 129, 247, 0) 100%);
            clip-path: polygon(100% 40%, 0 0, 0 100%, 100% 60%);
            pointer-events: none;
            animation: flickerBeam 2.2s infinite alternate;
            z-index: 1;
        }

        .reel-spin-cw {
            animation: spinReel 4s linear infinite;
            transform-origin: 90px 80px;
        }
        .reel-spin-ccw {
            animation: spinReel 4s linear infinite reverse;
            transform-origin: 170px 80px;
        }

        @keyframes spinReel {
            100% { transform: rotate(360deg); }
        }

        @keyframes flickerBeam {
            0% { opacity: 0.35; }
            50% { opacity: 0.85; }
            100% { opacity: 0.5; }
        }

        /* Slide 5: 학력 */
        .univ-center-card {
            background: rgba(12, 14, 21, 0.92);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 20px;
            padding: 46px 40px;
            max-width: 820px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        }

        .univ-logo-box-white {
            width: 260px;
            height: 110px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
            background: #fff;
            padding: 16px;
            border-radius: 12px;
        }

        .univ-logo-box-white img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        /* -------------------------------------------------------------------
           자기소개서 전용 단독 페이지 (#page-coverletter)
        ------------------------------------------------------------------- */
        .coverletter-grid {
            display: flex;
            flex-direction: column;
            gap: 24px;
            margin-top: 10px;
        }

        .essay-card {
            background: rgba(11, 13, 20, 0.85);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 18px;
            padding: 32px 36px;
            transition: all 0.25s ease;
            position: relative;
        }

        .essay-card:hover {
            border-color: var(--color-iris-violet);
            box-shadow: 0 10px 30px rgba(146, 129, 247, 0.15);
        }

        .essay-num-tag {
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--color-iris-violet);
            background: rgba(146, 129, 247, 0.15);
            border: 1px solid rgba(146, 129, 247, 0.3);
            padding: 4px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 12px;
        }

        .essay-title {
            font-size: 20px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 16px;
            border-left: 3px solid var(--color-iris-violet);
            padding-left: 12px;
        }

        .essay-body {
            font-size: 15px;
            color: var(--color-bone-white);
            line-height: 1.85;
            word-break: keep-all;
        }

        /* -------------------------------------------------------------------
           플레이 히스토리: 삼각 파라미터 다이어그램 복구
        ------------------------------------------------------------------- */
        .radar-triangle-container {
            background: rgba(11, 13, 20, 0.85);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 20px;
            padding: 36px 40px;
            margin-bottom: 36px;
            display: flex;
            align-items: center;
            gap: 40px;
            flex-wrap: wrap;
        }

        .radar-svg-col {
            flex: 1;
            min-width: 320px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .radar-desc-col {
            flex: 1.2;
            min-width: 320px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .radar-axis-card {
            background: rgba(16, 19, 28, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 16px 20px;
            border-left: 3px solid var(--color-iris-violet);
        }

        .radar-axis-title {
            font-size: 15px;
            font-weight: 600;
            color: #fff;
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }

        .radar-axis-txt {
            font-size: 13px;
            color: var(--color-ash-gray);
            line-height: 1.6;
        }

        .play-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .play-card {
            background: rgba(11, 13, 18, 0.85);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 14px;
            overflow: hidden;
            display: flex;
            transition: all 0.25s ease;
        }

        .play-card:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(146, 129, 247, 0.2);
        }

        .play-thumb {
            width: 100px;
            min-height: 135px;
            background: #050608;
            border-right: 1px solid var(--color-graphite-hairline);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            flex-shrink: 0;
        }

        .play-thumb img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .play-content {
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            flex: 1;
            min-width: 0;
        }

        .play-title {
            font-size: 15px;
            font-weight: 600;
            color: #fff;
            margin-bottom: 6px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .play-meta {
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--color-iris-violet);
            margin-bottom: 8px;
        }

        .play-insight {
            font-size: 12px;
            color: var(--color-ash-gray);
            line-height: 1.5;
        }

        /* -------------------------------------------------------------------
           포트폴리오 페이지 & 문서함
        ------------------------------------------------------------------- */
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
            padding: 20px;
            overflow: hidden;
        }

        .project-horizontal-imgbox img {
            width: 100%;
            height: 100%;
            max-height: 240px;
            object-fit: contain;
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

        .btn-ghost {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: var(--radius-buttons);
            border: 1px solid var(--color-graphite-hairline);
            color: var(--color-bone-white);
            font-size: 13px;
            font-weight: 500;
            background: rgba(255,255,255,0.03);
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-ghost:hover {
            border-color: var(--color-iris-violet);
            background: rgba(146, 129, 247, 0.15);
            color: #fff;
        }

        .doc-category-section {
            margin-bottom: 32px;
        }

        .doc-cat-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }

        .doc-cat-title {
            font-size: 18px;
            font-weight: 700;
            color: #fff;
        }

        .doc-badge {
            font-family: var(--font-mono);
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 4px;
            background: rgba(146, 129, 247, 0.15);
            color: var(--color-iris-violet);
            border: 1px solid rgba(146, 129, 247, 0.3);
        }

        .doc-cards-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }

        .doc-item-card {
            background: rgba(12, 14, 20, 0.8);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 12px;
            padding: 18px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            transition: all 0.2s ease;
        }

        .doc-item-card:hover {
            border-color: var(--color-iris-violet);
            background: rgba(18, 21, 32, 0.9);
            transform: translateY(-2px);
        }

        .doc-info {
            flex: 1;
            min-width: 0;
        }

        .doc-title-row {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
        }

        .doc-title {
            font-size: 14.5px;
            font-weight: 600;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .doc-type-badge {
            font-family: var(--font-mono);
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.08);
            color: var(--color-ash-gray);
        }

        .doc-desc {
            font-size: 12px;
            color: var(--color-ash-gray);
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .doc-actions {
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex-shrink: 0;
        }

        /* 탭 버튼 */
        .sub-tab-btn {
            background: transparent;
            border: none;
            color: var(--color-ash-gray);
            font-size: 15px;
            font-weight: 500;
            padding: 8px 18px;
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
            background: rgba(146, 129, 247, 0.18);
            border: 1px solid rgba(146, 129, 247, 0.45);
            font-weight: 600;
        }

        .sub-content {
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }

        .sub-content.active {
            display: block;
        }

        .page-section {
            display: none;
            animation: fadeIn 0.35s ease-in-out;
        }

        .page-section.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 960px) {
            .hero-canvas-step1 { background-size: cover; padding: 30px 24px; min-height: 520px; }
            .hero-text-overlay { max-width: 100%; background: rgba(0,0,0,0.65); padding: 20px; border-radius: 12px; }
            .grid-3 { grid-template-columns: 1fr; }
            .profile-flex-wrap { flex-direction: column; text-align: center; }
            .profile-table-grid { grid-template-columns: 1fr; text-align: left; }
            .project-logos-grid { grid-template-columns: 1fr 1fr; }
            .cinema-flex-container { flex-direction: column; }
            .radar-triangle-container { flex-direction: column; }
            .doc-cards-grid { grid-template-columns: 1fr; }
            .play-grid { grid-template-columns: 1fr; }
            .project-card-horizontal { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <!-- 상단 네비게이션 바 (사용자 요청: 이력소개와 자기소개서 분리) -->
    <header>
        <div class="logo" onclick="switchPage('main')">
            <span>SEUNGWOON.DEV</span>
            <span style="font-size:10px; color:var(--color-iris-violet); background:rgba(146,129,247,0.15); padding:2px 6px; border-radius:4px;">PORTFOLIO</span>
        </div>
        <nav>
            <button class="nav-link active" id="nav-btn-main" onclick="switchPage('main', this)">메인</button>
            <button class="nav-link" id="nav-btn-resume" onclick="switchPage('resume', this)">이력 소개</button>
            <button class="nav-link" id="nav-btn-coverletter" onclick="switchPage('coverletter', this)">자기소개서</button>
            <button class="nav-link" id="nav-btn-portfolio" onclick="switchPage('portfolio', this)">포트폴리오</button>
            <button class="nav-link" id="nav-btn-playhistory" onclick="switchPage('playhistory', this)">플레이 히스토리</button>
            <button class="edit-toggle-btn" id="editToggleBtn" onclick="toggleEditMode()">편집 모드 OFF</button>
        </nav>
    </header>

    <div class="container">

        <!-- =================================================================
             1. 메인 페이지 (10초 자동 전환 후 2페이지 정지, 복귀 시 1페이지 초기화)
        ================================================================== -->
        <section id="page-main" class="page-section active">
            
            <!-- Step 1: 메인 첫 화면 -->
            <div class="main-step-container active" id="main-step-1" onclick="handleMainStepClick(2)">
                <div class="hero-canvas-step1">
                    <div class="hero-text-overlay">
                        <div class="hero-logline" contenteditable="false">
                            탄탄한 논리로 상상하는 <br><span>크리에이터 정승운</span>
                        </div>
                        <div class="hero-sub" contenteditable="false">
                            스토리보드와 시스템 기획, 유니티 바이브 코딩과 데이터 테이블 밸런싱까지.<br>
                            창작물의 핵심 뼈대를 구축하고 유저가 몰입할 수 있는 세계를 설계합니다.
                        </div>
                    </div>
                </div>
                <div class="canvas-step-footer">
                    <span class="step-indicator-tag">01 / 02 [비전 &amp; 로그라인]</span>
                    <span>10초 후 핵심 역량 화면으로 자동 전환됩니다 (화면 클릭 시 즉시 이동 →)</span>
                </div>
            </div>

            <!-- Step 2: 메인 두 번째 화면 (밝아진 main2 배경 + 자기소개서 전용 버튼 포함) -->
            <div class="main-step-container" id="main-step-2" onclick="handleMainStepClick(1)">
                <div class="hero-canvas-step2">
                    <div style="width:100%; max-width:1080px;">
                        <span style="font-size:11px; font-family:var(--font-mono); color:var(--color-iris-violet); background:rgba(146,129,247,0.18); padding:4px 12px; border-radius:4px; font-weight:600;">CORE COMPETENCE</span>
                        <h2 class="section-title" style="font-size:28px; margin:12px 0 6px;">핵심 역량 및 강점</h2>
                        <p class="section-desc" style="margin-bottom:28px; font-size:14px; color:#d4d7dc;">시스템 설계부터 데이터 밸런싱, 협업 총괄까지 아우르는 크리에이티브 파이프라인입니다.</p>

                        <div class="grid-3" style="text-align:left;">
                            <div class="card-glass">
                                <div class="card-title" contenteditable="false">01. 시스템 설계 &amp; 논리 구조</div>
                                <div class="card-desc" contenteditable="false">
                                    AI 행동 트리(Behavior Tree) 구조 분리 및 상태 머신(FSM) 설계. 예외 상황을 원천 차단하고 시스템 간 상호작용을 정밀하게 기획합니다.
                                </div>
                            </div>
                            <div class="card-glass">
                                <div class="card-title" contenteditable="false">02. 데이터 테이블 &amp; 밸런싱</div>
                                <div class="card-desc" contenteditable="false">
                                    재배/제조/무역소 테이블을 직접 구조화하고 경제 순환 사이클과 시간 가치, 성장 곡선 밸런스 패치를 수행합니다.
                                </div>
                            </div>
                            <div class="card-glass">
                                <div class="card-title" contenteditable="false">03. 협업 총괄 &amp; 프로덕션</div>
                                <div class="card-desc" contenteditable="false">
                                    팀장 및 프로젝트 PD로서 일정 마일스톤 관리, QA 체크리스트 운용, 기획/아트/클라 간 커뮤니케이션을 조율합니다.
                                </div>
                            </div>
                        </div>

                        <!-- 사용자 요청: 두 번째 페이지에 자기소개서 버튼 포함 주요 바로가기 -->
                        <div class="ph-nav-buttons" onclick="event.stopPropagation()">
                            <button class="ph-nav-btn ph-nav-btn-primary" onclick="switchPage('coverletter')">
                                <span>📋 자기소개서 보기</span>
                            </button>
                            <button class="ph-nav-btn" onclick="switchPage('resume')">
                                <span>👤 이력 소개 보기</span>
                            </button>
                            <button class="ph-nav-btn" onclick="switchPage('portfolio')">
                                <span>🗂️ 포트폴리오 기획서</span>
                            </button>
                            <button class="ph-nav-btn" onclick="switchPage('playhistory')">
                                <span>🎮 플레이 히스토리</span>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="canvas-step-footer">
                    <span class="step-indicator-tag">02 / 02 [핵심 역량]</span>
                    <span>화면을 클릭하면 첫 화면으로 이동합니다 ↺</span>
                </div>
            </div>

        </section>


        <!-- =================================================================
             2. 이력 소개 페이지: 5단계 풀캔버스 인터랙티브 쇼케이스
             (화면 꽉 차게, 숫자로 순서 표기, 5번 슬라이드 클릭 시 1번으로 순환)
        ================================================================== -->
        <section id="page-resume" class="page-section">
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; flex-wrap:wrap; gap:12px;">
                <div>
                    <h1 class="section-title">이력 소개</h1>
                    <p class="section-desc" style="margin-bottom:0;">정승운의 인적사항, 기술 스택, 실무 프로젝트, 영화제작 및 학력 쇼케이스입니다.</p>
                </div>
                <!-- 상단 순서 탭 바 (01 ~ 05) -->
                <div class="resume-step-navigator">
                    <div class="step-num-pill active" id="resume-pill-1" onclick="jumpResumeStep(1)">01 인적사항</div>
                    <div class="step-num-pill" id="resume-pill-2" onclick="jumpResumeStep(2)">02 기술 스택</div>
                    <div class="step-num-pill" id="resume-pill-3" onclick="jumpResumeStep(3)">03 프로젝트&amp;경력</div>
                    <div class="step-num-pill" id="resume-pill-4" onclick="jumpResumeStep(4)">04 영화 연출</div>
                    <div class="step-num-pill" id="resume-pill-5" onclick="jumpResumeStep(5)">05 학력&amp;비전</div>
                </div>
            </div>

            <!-- Slide 1: 인적사항 및 비전 (밝은 main2 배경 + 좌측 투명배경 인물 + 우측 순차 인적사항) -->
            <div class="resume-step-canvas resume-canvas-1 active" id="resume-step-1" onclick="handleResumeCanvasClick(2)">
                <div class="profile-flex-wrap">
                    <div class="profile-photo-wrap stagger-item stagger-1">
                        <div class="profile-glow-circle"></div>
                        <img src="profile_cutout.png" alt="정승운" class="profile-cutout-img" />
                    </div>
                    <div class="profile-content-wrap">
                        <span class="role-badge-pill stagger-item stagger-2">GAME SYSTEM PLANNER &amp; CREATOR</span>
                        <div class="profile-title-name stagger-item stagger-2">
                            정승운 <span>SEUNGWOON JEONG</span>
                        </div>
                        <p style="color:#cfd3db; font-size:15px; margin-bottom:20px; line-height:1.6;" class="stagger-item stagger-3">
                            영화의 탄탄한 서사 구조와 게임의 능동적인 인터랙션을 융합하는 시스템 기획자.<br>
                            복잡한 경제 로직과 행동 트리를 체계적으로 정의하고 유저의 깊은 몰입을 이끌어냅니다.
                        </p>

                        <div class="profile-table-grid stagger-item stagger-4">
                            <div class="info-cell">
                                <span class="info-label-txt">생년월일</span>
                                <span class="info-val-txt">2000. 04. 11</span>
                            </div>
                            <div class="info-cell">
                                <span class="info-label-txt">연락처</span>
                                <span class="info-val-txt">010-9822-7714</span>
                            </div>
                            <div class="info-cell">
                                <span class="info-label-txt">이메일</span>
                                <span class="info-val-txt">caddman771144@gmail.com</span>
                            </div>
                            <div class="info-cell">
                                <span class="info-label-txt">병역 사항</span>
                                <span class="info-val-txt">군필 (만기 제대)</span>
                            </div>
                            <div class="info-cell" style="grid-column: span 2;">
                                <span class="info-label-txt">소재지 주소</span>
                                <span class="info-val-txt">서울특별시 중구 동호로 28길 21 202호</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="canvas-step-footer">
                    <span class="step-indicator-tag">01 / 05 [인적 사항 및 비전]</span>
                    <span>화면을 클릭하면 다음 단계(02 기술 스택)로 이동합니다 →</span>
                </div>
            </div>

            <!-- Slide 2: 보유 기술 및 가시성 개선된 유니티/어도비/오피스 아이콘 순차 등장 -->
            <div class="resume-step-canvas resume-canvas-2" id="resume-step-2" onclick="handleResumeCanvasClick(3)">
                <div style="width:100%; display:flex; flex-direction:column; align-items:center;">
                    <span class="role-badge-pill">TECHNICAL SKILLS &amp; TOOLS</span>
                    <h2 style="font-size:28px; color:#fff; margin-bottom:8px;">보유 기술 및 숙련도</h2>
                    <p style="color:var(--color-ash-gray); font-size:14px;">실무 게임 기획, 알고리즘 시뮬레이션, 데이터 시트 구조화에 활용하는 툴셋입니다.</p>

                    <!-- 중앙 정렬 아이콘들 -->
                    <div class="tools-center-row">
                        <div class="tool-icon-box stagger-item stagger-1">
                            <img src="icon_unity.svg" alt="Unity" style="filter: drop-shadow(0 0 12px rgba(255,255,255,0.7));" />
                            <span class="tool-tag-txt">Unity</span>
                            <span class="tool-level-badge">중급 (Core)</span>
                        </div>
                        <div class="tool-icon-box stagger-item stagger-2">
                            <img src="icon_premiere.svg" alt="Premiere Pro" />
                            <span class="tool-tag-txt">Premiere Pro</span>
                            <span class="tool-level-badge">고급 (Advanced)</span>
                        </div>
                        <div class="tool-icon-box stagger-item stagger-3">
                            <img src="icon_photoshop.svg" alt="Photoshop" />
                            <span class="tool-tag-txt">Photoshop</span>
                            <span class="tool-level-badge">고급 (Advanced)</span>
                        </div>
                        <div class="tool-icon-box stagger-item stagger-4">
                            <img src="icon_excel.svg" alt="Excel" />
                            <span class="tool-tag-txt">MS Excel</span>
                            <span class="tool-level-badge">고급 (Advanced)</span>
                        </div>
                        <div class="tool-icon-box stagger-item stagger-4">
                            <img src="icon_powerpoint.svg" alt="PowerPoint" />
                            <span class="tool-tag-txt">PowerPoint</span>
                            <span class="tool-level-badge">고급 (Advanced)</span>
                        </div>
                        <div class="tool-icon-box stagger-item stagger-5">
                            <img src="icon_word.svg" alt="Word" />
                            <span class="tool-tag-txt">MS Word</span>
                            <span class="tool-level-badge">고급 (Advanced)</span>
                        </div>
                    </div>

                    <!-- 하단 간략 설명 -->
                    <div class="tools-desc-grid">
                        <div class="tool-desc-card stagger-item stagger-3">
                            <h4>🎮 유니티 (Unity Engine)</h4>
                            <p>C# 바이브 코딩 및 객체 지향 구조 설계. 유한 상태 머신(FSM)과 AI 행동 트리(Behavior Tree)를 직접 스크립팅하여 게임 로직을 구현합니다.</p>
                        </div>
                        <div class="tool-desc-card stagger-item stagger-4">
                            <h4>🎨 어도비 프리미어 / 포토샵</h4>
                            <p>게임 공식 PV 티저 트레일러 직접 제작. 컷 편집, 색보정, 사운드 믹싱 지원 및 게임 내 UI/2D 그래픽 리소스 가공을 전담합니다.</p>
                        </div>
                        <div class="tool-desc-card stagger-item stagger-5">
                            <h4>📊 엑셀 / PPT / 워드</h4>
                            <p>복합 수식 기반의 재배/제조/무역 경제 밸런스 테이블 구조화. 명확한 시각적 다이어그램 중심의 시스템 기획서 및 제안서를 작성합니다.</p>
                        </div>
                    </div>
                </div>
                <div class="canvas-step-footer" style="width:100%;">
                    <span class="step-indicator-tag">02 / 05 [보유 기술 및 숙련도]</span>
                    <span>화면을 클릭하면 다음 단계(03 프로젝트 &amp; 경력)로 이동합니다 →</span>
                </div>
            </div>

            <!-- Slide 3: 프로젝트 설명 이미지 + 데블다이스, 제임스텍 로고 순차 등장 -->
            <div class="resume-step-canvas resume-canvas-3" id="resume-step-3" onclick="handleResumeCanvasClick(4)">
                <div style="width:100%; display:flex; flex-direction:column; align-items:center;">
                    <span class="role-badge-pill">PROJECTS &amp; CAREERS</span>
                    <h2 style="font-size:28px; color:#fff; margin-bottom:6px;">프로젝트 및 실무 경력</h2>
                    <p style="color:var(--color-ash-gray); font-size:14px;">기획 총괄부터 현장 운영 및 공급망 관리까지 체득한 실전 역량입니다.</p>

                    <div class="project-logos-grid">
                        <!-- 1. LAST SANCTUARY -->
                        <div class="career-milestone-box stagger-item stagger-1">
                            <div class="career-logo-container">
                                <img src="lastsanctuary.png" alt="LAST SANCTUARY" />
                            </div>
                            <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:4px;">&lt;LAST SANCTUARY&gt;</div>
                            <div style="font-size:11px; font-family:var(--font-mono); color:var(--color-iris-violet); margin-bottom:10px;">디벨로켓 / 시스템 기획</div>
                            <div style="font-size:12px; color:var(--color-ash-gray); line-height:1.6; text-align:left;">
                                전체 시스템 설계, 유니티 AI 행동 트리 구축, 밸런스 패치 및 공식 메인 PV 영상 직접 제작 총괄.
                            </div>
                        </div>

                        <!-- 2. 슬기로운 재배생활 -->
                        <div class="career-milestone-box stagger-item stagger-2">
                            <div class="career-logo-container">
                                <img src="슬기로운재배생활.png" alt="슬기로운 재배생활" />
                            </div>
                            <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:4px;">&lt;슬기로운 재배생활&gt;</div>
                            <div style="font-size:11px; font-family:var(--font-mono); color:var(--color-iris-violet); margin-bottom:10px;">디벨로켓 / 팀장 (PD)</div>
                            <div style="font-size:12px; color:var(--color-ash-gray); line-height:1.6; text-align:left;">
                                팀 총괄 관리, 코어 게임 루프 기획, 작물/가공/무역소 경제 순환 엑셀 시트 설계 및 밸런싱.
                            </div>
                        </div>

                        <!-- 3. 데블다이스 -->
                        <div class="career-milestone-box stagger-item stagger-3">
                            <div class="career-logo-container">
                                <img src="logo_devildice.png" alt="데블다이스" />
                            </div>
                            <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:4px;">데블다이스 (DEVILDICE)</div>
                            <div style="font-size:11px; font-family:var(--font-mono); color:var(--color-iris-violet); margin-bottom:10px;">매장 관리 &amp; 룰 티칭</div>
                            <div style="font-size:12px; color:var(--color-ash-gray); line-height:1.6; text-align:left;">
                                보드게임 매장 현장 운영, 유저 수준별 게임 룰 구조화 티칭 및 자원 순환 프로세스 관리.
                            </div>
                        </div>

                        <!-- 4. 제임스텍 -->
                        <div class="career-milestone-box stagger-item stagger-4">
                            <div class="career-logo-container">
                                <img src="logo_jamestech.png" alt="제임스텍" />
                            </div>
                            <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:4px;">(주)제임스 텍</div>
                            <div style="font-size:11px; font-family:var(--font-mono); color:var(--color-iris-violet); margin-bottom:10px;">구매팀 사원</div>
                            <div style="font-size:12px; color:var(--color-ash-gray); line-height:1.6; text-align:left;">
                                물류 공급망 관리, 부품 입출고 프로세스 트래킹 및 재고 수불 관리 시스템 운용.
                            </div>
                        </div>
                    </div>
                </div>
                <div class="canvas-step-footer" style="width:100%;">
                    <span class="step-indicator-tag">03 / 05 [프로젝트 및 실무 경력]</span>
                    <span>화면을 클릭하면 다음 단계(04 영화 연출)로 이동합니다 →</span>
                </div>
            </div>

            <!-- Slide 4: 영화 연출 & 참여 영화 (카메라 방향 반전: 왼쪽 영화 목록을 비춤) -->
            <div class="resume-step-canvas resume-canvas-4" id="resume-step-4" onclick="handleResumeCanvasClick(5)">
                <div class="cinema-flex-container">
                    <!-- 좌측: 참여 영화 9편 + 영화제 순차 리스트 -->
                    <div class="movie-scroll-col">
                        <div style="margin-bottom:8px;">
                            <span class="role-badge-pill" style="margin-bottom:6px;">FILMOGRAPHY &amp; PRODUCTION</span>
                            <h3 style="font-size:22px; color:#fff;">영화 연출 및 프로덕션 참여작</h3>
                            <p style="font-size:12.5px; color:var(--color-ash-gray);">현장에서 직접 연출, 예산 관리, 데이터 편집 및 사운드를 전담한 작품들입니다.</p>
                        </div>

                        <div class="movie-strip-item stagger-item stagger-1">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:3px;">🎬 졸업영화 &lt;개인 전시&gt;</div>
                                <div style="font-size:12px; color:var(--color-ash-gray);">동국대학교 | 총괄 PD (로케이션 헌팅, 전체 예산 및 현장 운영 관리)</div>
                            </div>
                            <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 8px; border-radius:4px;">2026.06 ~ 2026.11</div>
                        </div>

                        <div class="movie-strip-item stagger-item stagger-2">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:3px;">🎬 학생영화 &lt;각질&gt;</div>
                                <div style="font-size:12px; color:var(--color-ash-gray);">서울예술대학교 | 데이터매니저 &amp; 촬영 현장 컷 편집 전담</div>
                            </div>
                            <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 8px; border-radius:4px;">2025.10 ~ 2025.12</div>
                        </div>

                        <div class="movie-strip-item stagger-item stagger-3">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:3px;">🎬 졸업영화 &lt;그날의 음모&gt;</div>
                                <div style="font-size:12px; color:var(--color-ash-gray);">동국대학교 | 총괄 PD (예산 계획 수립, 현장 운영, 스틸 촬영 및 최종 보고서 작성)</div>
                            </div>
                            <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 8px; border-radius:4px;">2024.06 ~ 2024.12</div>
                        </div>

                        <div class="movie-strip-item stagger-item stagger-4">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:3px;">🎬 졸업영화 &lt;유산을 넘겨라, 아니!&gt;</div>
                                <div style="font-size:12px; color:var(--color-ash-gray);">동국대학교 | 총괄 PD (촬영 계획 수립 및 프로덕션 운영 총괄)</div>
                            </div>
                            <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 8px; border-radius:4px;">2024.05 ~ 2024.12</div>
                        </div>

                        <div class="movie-strip-item stagger-item stagger-5">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:3px;">🎬 졸업영화 &lt;교실의 이데아&gt; &amp; &lt;신발장 나눔합니다&gt;</div>
                                <div style="font-size:12px; color:var(--color-ash-gray);">동국대학교 | 미술부 소품 세팅 및 제작부 운영 관리</div>
                            </div>
                            <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 8px; border-radius:4px;">2023.08 ~ 2024.02</div>
                        </div>

                        <div class="movie-strip-item stagger-item stagger-5">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:3px;">🎬 대학원 졸업영화 &lt;WS 부재중전화&gt; &amp; &lt;침묵&gt;</div>
                                <div style="font-size:12px; color:var(--color-ash-gray);">한예종 미술부 세팅 | 개인작 학생영화 음향 감독 (녹음 및 믹싱)</div>
                            </div>
                            <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 8px; border-radius:4px;">2021.06 ~ 2021.12</div>
                        </div>

                        <div class="movie-strip-item stagger-item stagger-5">
                            <div>
                                <div style="font-size:15px; font-weight:700; color:#fff; margin-bottom:3px;">🎥 2026 / 2020 동국영화제 (DUFF)</div>
                                <div style="font-size:12px; color:var(--color-ash-gray);">운영팀장 (행사 현장 운영 관리 총괄) 및 홍보팀 공식 홍보영상 제작</div>
                            </div>
                            <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); background:rgba(146,129,247,0.1); padding:4px 8px; border-radius:4px;">운영팀장 / 홍보팀</div>
                        </div>
                    </div>

                    <!-- 우측: 35mm 영화 카메라 (왼쪽 영사 방향으로 반전) -->
                    <div class="camera-anim-col">
                        <div class="lens-light-beam-left"></div>
                        <div class="camera-facing-left">
                            <svg viewBox="0 0 280 280" width="250" height="250" xmlns="http://www.w3.org/2000/svg">
                                <!-- Reel Left -->
                                <g class="reel-spin-cw">
                                    <circle cx="90" cy="80" r="46" fill="#141722" stroke="#9281f7" stroke-width="3.5" />
                                    <circle cx="90" cy="80" r="16" fill="#292d30" stroke="#fff" stroke-width="2" />
                                    <line x1="90" y1="36" x2="90" y2="124" stroke="#9281f7" stroke-width="2.5" />
                                    <line x1="46" y1="80" x2="134" y2="80" stroke="#9281f7" stroke-width="2.5" />
                                    <line x1="59" y1="49" x2="121" y2="111" stroke="#9281f7" stroke-width="2.5" />
                                    <line x1="59" y1="111" x2="121" y2="49" stroke="#9281f7" stroke-width="2.5" />
                                </g>

                                <!-- Reel Right -->
                                <g class="reel-spin-ccw">
                                    <circle cx="170" cy="80" r="46" fill="#141722" stroke="#9281f7" stroke-width="3.5" />
                                    <circle cx="170" cy="80" r="16" fill="#292d30" stroke="#fff" stroke-width="2" />
                                    <line x1="170" y1="36" x2="170" y2="124" stroke="#9281f7" stroke-width="2.5" />
                                    <line x1="126" y1="80" x2="214" y2="80" stroke="#9281f7" stroke-width="2.5" />
                                    <line x1="139" y1="49" x2="201" y2="111" stroke="#9281f7" stroke-width="2.5" />
                                    <line x1="139" y1="111" x2="201" y2="49" stroke="#9281f7" stroke-width="2.5" />
                                </g>

                                <!-- Camera Body -->
                                <rect x="60" y="120" width="140" height="96" rx="14" fill="#1b1e2a" stroke="#484d5c" stroke-width="3" />
                                <rect x="75" y="136" width="60" height="42" rx="6" fill="#0b0d13" stroke="#9281f7" stroke-width="1.5" />
                                <circle cx="165" cy="155" r="12" fill="#9281f7" opacity="0.3" />
                                <circle cx="165" cy="155" r="6" fill="#9281f7" />

                                <!-- Front Lens -->
                                <path d="M200 142 L236 128 L236 208 L200 194 Z" fill="#292e3f" stroke="#9281f7" stroke-width="2.5" />
                                <ellipse cx="236" cy="168" rx="8" ry="40" fill="#9281f7" opacity="0.7" />

                                <!-- Tripod Mount -->
                                <rect x="115" y="216" width="30" height="18" fill="#383d4c" />
                                <line x1="80" y1="260" x2="130" y2="234" stroke="#484d5c" stroke-width="4" stroke-linecap="round" />
                                <line x1="180" y1="260" x2="130" y2="234" stroke="#484d5c" stroke-width="4" stroke-linecap="round" />
                                <line x1="130" y1="260" x2="130" y2="234" stroke="#484d5c" stroke-width="4" stroke-linecap="round" />
                            </svg>
                        </div>
                        <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-top:14px; letter-spacing:0.08em;">
                            ● 35MM CINEMATIC PROJECTION
                        </div>
                    </div>
                </div>
                <div class="canvas-step-footer" style="width:100%;">
                    <span class="step-indicator-tag">04 / 05 [영화 연출 및 프로덕션]</span>
                    <span>화면을 클릭하면 다음 단계(05 학력 및 비전)로 이동합니다 →</span>
                </div>
            </div>

            <!-- Slide 5: 동국대학교 로고 + 영화영상학과 졸업 설명 (클릭 시 다시 1번 슬라이드로 순환!) -->
            <div class="resume-step-canvas resume-canvas-5" id="resume-step-5" onclick="handleResumeCanvasClick(1)">
                <div style="width:100%; display:flex; flex-direction:column; align-items:center;">
                    <span class="role-badge-pill">ACADEMIC BACKGROUND &amp; CORE VISION</span>
                    <h2 style="font-size:28px; color:#fff; margin-bottom:6px;">학력 및 융합 역량</h2>
                    <p style="color:var(--color-ash-gray); font-size:14px;">영화영상 전공의 서사적 깊이와 게임 인터랙션을 융합하는 설계 철학입니다.</p>

                    <div class="univ-center-card stagger-item stagger-1">
                        <div class="univ-logo-box-white">
                            <img src="logo_dongguk.png" alt="동국대학교 DONGGUK UNIVERSITY" />
                        </div>
                        <h3 style="font-size:22px; color:#fff; margin-bottom:6px;">동국대학교 영화영상학과</h3>
                        <div style="font-family:var(--font-mono); font-size:14px; color:var(--color-iris-violet); margin-bottom:18px;">
                            학사 졸업 예정 (2019.01 ~ 현재) | 학점: 3.46 / 4.5
                        </div>
                        <p style="color:#d0d4dd; font-size:15px; line-height:1.85; text-align:left; max-width:700px; word-break:keep-all;">
                            동국대학교 영화영상학과에서 영화 기획, 시나리오 작법, 제작 총괄(PD)을 거치며 관객의 시선을 사로잡는 연출과 갈등 구조를 체득했습니다.<br><br>
                            수동적인 영상 매체를 넘어, <strong>유저가 스스로 선택하고 시스템과 능동적으로 호흡하는 게임</strong>에 매료되어 게임 기획자로 전향했습니다. 
                            영화를 만들며 단련된 스토리텔링과 집요한 논리 구조를 바탕으로 유저에게 잊지 못할 몰입을 선사하는 게임 시스템을 구축합니다.
                        </p>
                    </div>
                </div>
                <div class="canvas-step-footer" style="width:100%;">
                    <span class="step-indicator-tag">05 / 05 [학력 및 융합 역량]</span>
                    <span style="color:var(--color-iris-violet); font-weight:600;">화면을 클릭하면 첫 단계(01 인적사항)로 돌아갑니다 ↺</span>
                </div>
            </div>

        </section>


        <!-- =================================================================
             3. 자기소개서 전용 단독 페이지 (#page-coverletter)
             (사용자가 작성한 4개 섹션 전문을 100% 온전하게 수록)
        ================================================================== -->
        <section id="page-coverletter" class="page-section">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; flex-wrap:wrap; gap:16px;">
                <div>
                    <h1 class="section-title">자기소개서</h1>
                    <p class="section-desc" style="margin-bottom:0;">정승운 기획자의 지원 동기, 직무 역량, 문제 해결 경험 및 미래 목표 전문입니다.</p>
                </div>
                <a href="/api/download?file=20260904_13-1_자기소개서_Ver01_정승운.pdf&folder=root" target="_blank" class="btn-ghost" style="padding:10px 18px; border-color:var(--color-iris-violet); background:rgba(146,129,247,0.15);">
                    <span>📄 원본 PDF 열람 / 다운로드</span>
                </a>
            </div>

            <div class="coverletter-grid">
                <!-- 1. 지원 동기 -->
                <div class="essay-card">
                    <span class="essay-num-tag">ESSAY SECTION 01</span>
                    <h3 class="essay-title">1. 지원 동기: 상상을 실현하는 장으로서의 게임</h3>
                    <div class="essay-body" contenteditable="false">
                        상상력은 많은 것들을 가능하게 합니다. 누군가는 종이 위에 새로운 세계를 창조하기도 하고, 누군가는 붓질 몇 번만에 수많은 사람들의 시선을 사로잡습니다. 때로는 수백 명의 사람들의 눈과 귀를 황홀경에 빠트리는 것도 상상력의 힘일 것입니다. 어릴 때부터 책과 영화를 좋아했던 저는 언제나 상상 속의 세계에 빠져 있었고, 이런 공간을 창조하는 일을 하고 있는 저를 막연하게 떠올리곤 했습니다.<br><br>
                        처음으로 접한 게임은 이런 저에게 가뭄 속의 단비와 같았습니다. 수동적으로 주어진 세계를 받아들일 수밖에 없는 이전의 문화 매체들과 다르게 게임 속 세계에서는 유저가 스스로 성장하고 다른 이들과 이야기를 나누며 그 세계를 창조하거나 이야기의 운명을 바꾸는 것도 가능합니다. 게임은 상상의 세계 속에 저를 초대하는 것뿐만 아니라 '내가 상상한 것들을 마음껏 펼쳐내고 싶다'는 저의 욕망을 훌륭하게 충족해 주었습니다.<br><br>
                        여러 가지 다양한 게임을 플레이한 것은 영화를 만드는 일에도 분명 영향을 주었습니다. 제가 쓴 시나리오들은 제가 경험한 많은 세계의 영향으로 상당히 특이하고 독창적이라는 평가를 많이 받았고, 남들과는 다른 시선으로 무언가를 바라보려고 하는 습관 때문인지 많은 사람들이 자신의 시나리오 평가를 부탁하기도 했습니다. 다만 어디까지고 획일적으로 같은 장면을 구성하여 반복해서 찍어 동일한 감상을 관객들에게 전달하려 애쓰는 일은 저에게 말로 하기 힘든 답답함을 선사했습니다. 이러한 답답함을 해소하기 위해선 저의 작품을 즐기는 이들에게 의도된 자유를 부여할 수 있어야 하고 이것이 가능한 문화 매체는 게임밖에 없다는 생각이 불현듯 떠올랐습니다.<br><br>
                        AI의 발달로 인해 어렵게만 느껴지고 문외한의 영역이었던 코딩이나 게임 엔진의 접근성이 용이해져, 실제로 게임을 기획하고 개발해 보는 경험은 저에게 색다른 즐거움을 선사해 주었습니다. 단순히 저의 상상이 아니라 누군가의 상상력을 이끌어 낼 수 있도록 창조해 낸 세계, 어릴 적부터 꿈꿔왔던 일이 비로소 실현되는 순간이었습니다.<br><br>
                        게임을 만드는 일은 자신의 생각을 남들에게 보여주는 것보다, 유저가 어떠한 생각과 행동을 할 수 있도록 상상한다는 점에서 다른 문화 매체의 제작과는 다른 매력과 강점이 있다고 생각합니다. 제가 수없이 마주친 상상 실현의 체험과 그 즐거움을 다른 사람들에게도 전달할 수 있는 기획자가 되고 싶습니다.
                    </div>
                </div>

                <!-- 2. 직무 역량 / 경험 -->
                <div class="essay-card">
                    <span class="essay-num-tag">ESSAY SECTION 02</span>
                    <h3 class="essay-title">2. 직무 역량 및 경험: 논리와 빈틈없는 예외 검증</h3>
                    <div class="essay-body" contenteditable="false">
                        게임을 기획하고 그 시스템을 이해하는 데에 가장 중요한 것은 의도와 목적성을 설명할 수 있는 논리력입니다. 또한 해당 논리의 허점과 예외 사항을 꼼꼼히 점검하여 빈틈이 없도록 하는 것 또한 필수적일 것입니다.<br><br>
                        팀 단위 시뮬레이션 게임 개발 프로젝트인 &lt;LAST SANCTUARY&gt;에 시스템 기획자로 참여할 당시 AI 로직을 설계하게 되었습니다. 저는 평소에도 &lt;문명&gt;, &lt;풋볼매니저&gt;, &lt;림월드&gt; 등 다양한 AI 기반 시뮬레이션 게임을 즐겨왔기 때문에 바이브 코딩의 특성과 그동안의 플레이 경험을 고려하여 유한 상태 머신(FSM)을 활용해 로직을 생성했습니다. 명확한 계획과 논리 구조를 세우지 않고 한 번에 자연어로 명령하여 생성한 코드는 전투 시뮬레이션에서 수많은 예외 사항을 발생시켰고 결국 모든 구조를 다시 세울 수밖에 없었습니다.<br><br>
                        우선 하나로 통합되어 있던 AI 스크립트를 각 행동과 예외 상황별로 스크립트를 만들어 로직을 꼼꼼하게 점검 후 행동 트리(Behavior Tree) 형태로 연결했습니다. 이후 발생할 수 있는 상황에 대한 체크리스트를 작성하여 기능 하나하나에 대한 테스트를 진행했고, 발생한 버그들에 대한 수정과 필요한 기능을 추가하는 것만으로 기획한 형태의 전투 AI를 구성하는 데 성공했습니다. 이때의 경험은 논리적이고 체계적인 시스템 기획과 구축 역량 향상에 큰 도움을 주었습니다.
                    </div>
                </div>

                <!-- 3. 문제 해결 / 소통 -->
                <div class="essay-card">
                    <span class="essay-num-tag">ESSAY SECTION 03</span>
                    <h3 class="essay-title">3. 문제 해결: 탄탄한 논리와 시각화를 통한 조율</h3>
                    <div class="essay-body" contenteditable="false">
                        저는 언제나 탄탄한 논리력을 바탕으로 이해시키려는 자세를 가지고 있습니다. 단체로 프로젝트를 진행하다 보면 구성원들 간의 의견 충돌이 반드시 일어나기 마련입니다.<br><br>
                        팀 WEED HOLDINGS의 팀장으로 게임 &lt;슬기로운 재배생활&gt;을 제작하는 과정에서 UI 배치 과정에 팀원과의 의견 충돌 상황이 발생했습니다. 팀원들은 각 UI 슬롯의 진행 시간을 표기하는 것이 불필요하다 느꼈고, 생산이 필요한 리소스의 양이 많은 해당 게임의 특성상 리소스의 양을 최대한 줄이자고 주장했습니다.<br><br>
                        시스템 구성상 각 슬롯에서 돌아가고 있는 타이머의 시간이 각기 다른 상황이 많을 수 있다는 것을 우선 설명한 후 팀원들의 의견도 일부 절충하여 기존에 다른 UI에서 사용하던 타이머 리소스를 색만 변경하여 재활용하는 것으로 리소스의 절감을 이루어 냈습니다.<br><br>
                        이처럼 제 의견이 상대방의 의견보다 더 합당하다 스스로 느끼는 경우에도 설명을 동반하여 충분한 논의 과정을 거칩니다. 이 과정에서 상대방의 의견이 더 합당하다고 느낄 경우 제 의견을 철회하거나 상대방의 의견 또한 좋은 아이디어를 일부 채용하려고 합니다. 이를 통해 저의 의견에서 부족했던 부분을 보완하거나 제가 구축하고자 하는 시스템에 대한 팀원들의 이해도가 상승하는 긍정적 효과가 창출될 수 있기 때문에 저는 항상 업무 내에서의 갈등 상황을 문제에 대한 해결책을 마련할 수 있는 기회라고 보고 있습니다.
                    </div>
                </div>

                <!-- 4. 목표와 포부 -->
                <div class="essay-card">
                    <span class="essay-num-tag">ESSAY SECTION 04</span>
                    <h3 class="essay-title">4. 목표와 포부: 대중성과 깊이를 겸비한 기획자</h3>
                    <div class="essay-body" contenteditable="false">
                        저는 인정받는 기획자가 되고 싶습니다. 기획자가 된다는 것은 제가 만들고 싶은 것만 만든다는 의미는 아닐 것입니다. 결국 기획이라는 것은 판매할 상품을 만드는 것이고, 제가 만든 세계가 대다수의 인원들에게 흥미롭게 받아들여져야 하기 때문입니다.<br><br>
                        제가 만든 세계가 모두에게 외면받고, 받아들여지지 않을 수도 있습니다. 그럴 때마다 누군가를 탓하고 남아 있기만 한다면 스스로 성장할 기회를 버리는 것이라 생각합니다. 제가 창조한 세계의 문제점을 파악하고 의견을 받아들여 보완해 나간다면 언젠가는 그 노력의 진가를 알아주는 순간이 올 것이라 믿고 있습니다.
                    </div>
                </div>
            </div>
        </section>


        <!-- =================================================================
             4. 포트폴리오 페이지 (대표 프로젝트 + 20건 기획서/데이터 문서함)
        ================================================================== -->
        <section id="page-portfolio" class="page-section">
            <h1 class="section-title">포트폴리오 아카이브</h1>
            <p class="section-desc">대표 프로젝트 기획 및 연동된 기획서 문서함을 열람할 수 있습니다.</p>

            <div style="display:flex; gap:12px; margin-bottom:28px; border-bottom:1px solid var(--color-graphite-hairline); padding-bottom:12px;">
                <button class="sub-tab-btn active" onclick="switchPortfolioTab('portfolio-projects', this)">대표 프로젝트 기획</button>
                <button class="sub-tab-btn" onclick="switchPortfolioTab('portfolio-docs', this)">기획서 및 데이터 문서함 (20건)</button>
            </div>

            <!-- 1. 대표 프로젝트 기획 -->
            <div id="portfolio-projects" class="sub-content active">
                <div class="project-card-horizontal" onclick="openModal('project1')">
                    <div class="project-horizontal-imgbox"><img src="lastsanctuary.png" alt="LAST SANCTUARY"></div>
                    <div class="project-card-body">
                        <div>
                            <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-bottom:6px;">PC RPG / SYSTEM PLANNING</div>
                            <div class="project-title">PC 게임 &lt;LAST SANCTUARY&gt;</div>
                            <div class="project-desc">전체 게임 시스템 기획, 유니티 바이브 코딩, AI 행동 트리(Behavior Tree) 설계 및 메인 PV 제작. 유한 상태 머신 기반의 전투 예외 제어.</div>
                        </div>
                        <span class="btn-ghost" style="font-size:12px; width:fit-content;">상세 기획서 열람 →</span>
                    </div>
                </div>

                <div class="project-card-horizontal" onclick="openModal('project2')">
                    <div class="project-horizontal-imgbox"><img src="슬기로운재배생활.png" alt="슬기로운 재배생활"></div>
                    <div class="project-card-body">
                        <div>
                            <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-bottom:6px;">PC SIMULATION / TEAM LEAD</div>
                            <div class="project-title">PC 게임 &lt;슬기로운 재배생활&gt;</div>
                            <div class="project-desc">팀장 총괄, 코어 루프 기획, 작물 재배/제조/무역 데이터 시트 수립 및 밸런스 패치. 일정 마일스톤 및 QA 체크리스트 운용.</div>
                        </div>
                        <span class="btn-ghost" style="font-size:12px; width:fit-content;">상세 기획서 열람 →</span>
                    </div>
                </div>
            </div>

            <!-- 2. 기획서 및 데이터 문서함 -->
            <div id="portfolio-docs" class="sub-content">
                <div id="documentsArchiveContainer">
                    <div style="color:var(--color-ash-gray); text-align:center; padding:40px;">⏳ 문서를 불러오는 중입니다...</div>
                </div>
            </div>
        </section>


        <!-- =================================================================
             5. 플레이 히스토리 (삼각 파라미터 복구 + 게임 카드 + IGDB 검색 연동)
        ================================================================== -->
        <section id="page-playhistory" class="page-section">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; flex-wrap:wrap; gap:16px;">
                <div>
                    <h1 class="section-title">플레이 히스토리</h1>
                    <p class="section-desc" style="margin-bottom:0;">게임 기획적 인사이트를 얻은 주요 플레이 게임과 코어 시스템 분석입니다.</p>
                </div>
                <button class="btn-ghost" onclick="openGameSearchModal()" style="padding:10px 18px; border-color:var(--color-iris-violet); background:rgba(146,129,247,0.18); font-weight:600;">
                    <span>🔍 IGDB 게임 실시간 검색 및 추가</span>
                </button>
            </div>

            <!-- 삼각 파라미터 레이더 다이어그램 (사용자 요청 복구) -->
            <div class="radar-triangle-container">
                <div class="radar-svg-col">
                    <svg viewBox="0 0 340 310" width="320" height="290" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#9281f7" stop-opacity="0.6"/>
                                <stop offset="100%" stop-color="#705cf6" stop-opacity="0.25"/>
                            </linearGradient>
                            <filter id="radarGlow" x="-20%" y="-20%" width="140%" height="140%">
                                <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#9281f7" flood-opacity="0.6"/>
                            </filter>
                        </defs>

                        <!-- Guide Triangles (100%, 75%, 50%, 25%) Center: (170, 160), R=110 -->
                        <!-- 0° Top=(170, 50), 120° Bottom-Right=(265, 215), 240° Bottom-Left=(75, 215) -->
                        <polygon points="170,50 265,215 75,215" fill="none" stroke="#2a2e3d" stroke-width="1.5" />
                        <polygon points="170,77.5 241.25,201.25 98.75,201.25" fill="none" stroke="#1f2330" stroke-width="1" />
                        <polygon points="170,105 217.5,187.5 122.5,187.5" fill="none" stroke="#1f2330" stroke-width="1" />
                        <polygon points="170,132.5 193.75,173.75 146.25,173.75" fill="none" stroke="#1f2330" stroke-width="1" />

                        <!-- Axis Lines -->
                        <line x1="170" y1="160" x2="170" y2="50" stroke="#353b4d" stroke-width="1.5" stroke-dasharray="3,3"/>
                        <line x1="170" y1="160" x2="265" y2="215" stroke="#353b4d" stroke-width="1.5" stroke-dasharray="3,3"/>
                        <line x1="170" y1="160" x2="75" y2="215" stroke="#353b4d" stroke-width="1.5" stroke-dasharray="3,3"/>

                        <!-- User Radar Data Polygon (Simulation 55% / Management 30% / RPG 25%) -->
                        <!-- Scaled points: Top: 50+(160-50)*0.1 = 61, BR: 160+(215-160)*0.75=201, BL: 160+(215-160)*0.7=198 -->
                        <polygon points="170,62 248,205 92,203" fill="url(#polyGrad)" stroke="#9281f7" stroke-width="2.5" filter="url(#radarGlow)" />

                        <!-- Vertex Dots -->
                        <circle cx="170" cy="62" r="5" fill="#fff" stroke="#9281f7" stroke-width="2"/>
                        <circle cx="248" cy="205" r="5" fill="#fff" stroke="#9281f7" stroke-width="2"/>
                        <circle cx="92" cy="203" r="5" fill="#fff" stroke="#9281f7" stroke-width="2"/>

                        <!-- Labels -->
                        <text x="170" y="32" fill="#ffffff" font-size="12.5" font-weight="700" text-anchor="middle" font-family="Pretendard">시뮬레이션 / 전략 (55%)</text>
                        <text x="275" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">경영 / 샌드박스 (30%)</text>
                        <text x="65" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">RPG / 내러티브 (25%)</text>
                    </svg>
                </div>

                <div class="radar-desc-col">
                    <div class="radar-axis-card">
                        <div class="radar-axis-title">
                            <span>시뮬레이션 / 전략 (Simulation &amp; Strategy)</span>
                            <span style="color:var(--color-iris-violet); font-family:var(--font-mono);">55% | 1,400h+</span>
                        </div>
                        <div class="radar-axis-txt">&lt;문명 6&gt;, &lt;풋볼 매니저&gt; 등 복합 상태 변수 기반 시뮬레이션과 성장 곡선 밸런싱 분석.</div>
                    </div>

                    <div class="radar-axis-card">
                        <div class="radar-axis-title">
                            <span>경영 / 샌드박스 (Management &amp; Sandbox)</span>
                            <span style="color:var(--color-iris-violet); font-family:var(--font-mono);">30% | 700h+</span>
                        </div>
                        <div class="radar-axis-txt">&lt;림월드&gt;, &lt;팩토리오&gt; 등 자원 순환 경제 사이클 및 유한 상태 머신(FSM) 상호작용 기획 적용.</div>
                    </div>

                    <div class="radar-axis-card">
                        <div class="radar-axis-title">
                            <span>RPG / 내러티브 (RPG &amp; Narrative)</span>
                            <span style="color:var(--color-iris-violet); font-family:var(--font-mono);">25% | 400h+</span>
                        </div>
                        <div class="radar-axis-txt">영화영상학 기반 서사 설계와 퀘스트 트리, AI 행동 트리(Behavior Tree) 전투 연출 연구.</div>
                    </div>
                </div>
            </div>

            <!-- 플레이 게임 목록 -->
            <div class="play-grid" id="full-play-grid">
                <div class="play-card">
                    <div class="play-thumb"><img src="https://images.igdb.com/igdb/image/upload/t_cover_big/coaaqr.jpg" alt="문명 6"></div>
                    <div class="play-content">
                        <div class="play-title">Sid Meier's Civilization VI</div>
                        <div class="play-meta">턴제 전략 / 1,200h+ 분석</div>
                        <div class="play-insight">타일 산출량 수식 구조, 불가사의 트리 설계 및 시대별 승리 조건 밸런싱 연구.</div>
                    </div>
                </div>
                <div class="play-card">
                    <div class="play-thumb"><img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co73z1.jpg" alt="FM 2024"></div>
                    <div class="play-content">
                        <div class="play-title">Football Manager 2024</div>
                        <div class="play-meta">스포츠 시뮬 / 950h+ 분석</div>
                        <div class="play-insight">다변수 수치 시뮬레이션 연산 구조와 AI 이적 시장 경제 순환 사이클 벤치마킹.</div>
                    </div>
                </div>
                <div class="play-card">
                    <div class="play-thumb"><img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co5w0x.jpg" alt="RimWorld"></div>
                    <div class="play-content">
                        <div class="play-title">RimWorld (림월드)</div>
                        <div class="play-meta">SF 생존 시뮬 / 700h+ 분석</div>
                        <div class="play-insight">AI 스토리텔러 이벤트 확률 분포 모델링과 림 성격별 유한 상태 머신(FSM) 상호작용.</div>
                    </div>
                </div>
            </div>
        </section>

    </div>


    <!-- =================================================================
         IGDB 게임 실시간 검색 모달
    ================================================================== -->
    <div class="modal" id="gameSearchModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.88); z-index:2100; padding:40px 20px; overflow-y:auto;">
        <div class="modal-content" style="background:#0c0e14; border:1px solid var(--color-graphite-hairline); border-radius:18px; max-width:680px; margin:30px auto; padding:28px; position:relative; box-shadow:0 20px 50px rgba(0,0,0,0.9);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h3 style="color:#fff; font-size:18px;">🎮 IGDB 실시간 게임 데이터베이스 검색</h3>
                <button onclick="closeGameSearchModal()" style="background:transparent; border:none; color:var(--color-ash-gray); font-size:18px; cursor:pointer;">✕</button>
            </div>
            
            <div style="display:flex; gap:10px; margin-bottom:20px;">
                <input type="text" id="gameQueryInput" placeholder="게임 이름 입력 (예: 문명, 림월드, 젤다, 마리오, Zelda, Mario)" style="flex:1; background:#141722; border:1px solid var(--color-graphite-hairline); border-radius:8px; padding:12px 16px; color:#fff; font-size:14px; outline:none;" onkeyup="if(event.key==='Enter') executeGameSearch()" />
                <button onclick="executeGameSearch()" class="btn-ghost" style="background:var(--color-iris-violet); color:#fff; border-color:var(--color-iris-violet); padding:0 20px; font-weight:600;">검색</button>
            </div>

            <div id="gameSearchResults" style="max-height:420px; overflow-y:auto; border:1px solid var(--color-graphite-hairline); border-radius:10px; background:#07080c;">
                <div style="color:var(--color-ash-gray); text-align:center; padding:36px; font-size:13.5px;">한글 또는 영문 게임명을 입력하시면 IGDB 공식 데이터베이스에서 실시간으로 검색합니다.</div>
            </div>
        </div>
    </div>


    <!-- =================================================================
         프로젝트 상세 모달
    ================================================================== -->
    <div class="modal" id="projectModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:2000; padding:40px 20px; overflow-y:auto;">
        <div class="modal-content" style="background:#090a0e; border:1px solid var(--color-graphite-hairline); border-radius:16px; max-width:860px; margin:0 auto; padding:36px; position:relative; box-shadow:0 20px 50px rgba(0,0,0,0.9);">
            <button onclick="closeModal()" style="position:absolute; top:24px; right:24px; background:transparent; border:none; color:#fff; cursor:pointer; font-size:16px;">닫기 ✕</button>
            <div id="modalBody"></div>
        </div>
    </div>


    <script>
        // API 기본 주소 동적 감지 (CORS 및 포트 불일치 방지)
        const API_BASE = window.location.origin.includes('http') ? window.location.origin : 'http://localhost:3000';
        let mainAutoSlideTimer = null;
        let currentResumeStep = 1;
        const TOTAL_RESUME_STEPS = 5;

        /* -------------------------------------------------------------
           메인 페이지 10초 자동 전환 로직
           - 1페이지 -> 10초 후 2페이지로 전환된 뒤 거기서 정지!
           - 다른 페이지 갔다 오면 항상 1페이지로 초기화되고 다시 10초 타이머 시작!
        ------------------------------------------------------------- */
        function startMainAutoTimer() {
            stopMainAutoTimer();
            mainAutoSlideTimer = setTimeout(() => {
                const s1 = document.getElementById('main-step-1');
                if (s1 && s1.classList.contains('active')) {
                    handleMainStepClick(2);
                }
                stopMainAutoTimer(); // 2페이지에서 멈춤
            }, 10000);
        }

        function stopMainAutoTimer() {
            if (mainAutoSlideTimer) {
                clearTimeout(mainAutoSlideTimer);
                mainAutoSlideTimer = null;
            }
        }

        function resetMainSteps() {
            document.querySelectorAll('.main-step-container').forEach(s => s.classList.remove('active'));
            const s1 = document.getElementById('main-step-1');
            if (s1) s1.classList.add('active');
        }

        function handleMainStepClick(targetStep) {
            document.querySelectorAll('.main-step-container').forEach(s => s.classList.remove('active'));
            const target = document.getElementById('main-step-' + targetStep);
            if (target) target.classList.add('active');

            if (targetStep === 2) {
                stopMainAutoTimer(); // 2페이지 도달 시 정지
            } else {
                startMainAutoTimer(); // 1페이지로 돌아가면 다시 10초 타이머
            }
        }

        /* -------------------------------------------------------------
           페이지 라우팅 전환 (메인 복귀 시 1페이지 초기화)
        ------------------------------------------------------------- */
        function switchPage(pageId, btnElement) {
            document.querySelectorAll('.page-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('nav .nav-link').forEach(btn => btn.classList.remove('active'));
            
            const target = document.getElementById('page-' + pageId);
            if (target) target.classList.add('active');

            const navBtn = document.getElementById('nav-btn-' + pageId);
            if (navBtn) navBtn.classList.add('active');

            window.scrollTo({ top: 0, behavior: 'smooth' });

            if (pageId === 'main') {
                resetMainSteps(); // 메인으로 돌아오면 반드시 1페이지로 초기화!
                startMainAutoTimer(); // 10초 타이머 재시작
            } else {
                stopMainAutoTimer();
            }

            if (pageId === 'portfolio') {
                loadPortfolioDocuments();
            }
        }

        /* -------------------------------------------------------------
           이력 소개: 5단계 풀캔버스 인터랙티브 쇼케이스
           (화면 클릭 시 다음 단계, 5단계에서 클릭 시 다시 1단계로 순환)
        ------------------------------------------------------------- */
        function jumpResumeStep(stepNum) {
            currentResumeStep = stepNum;
            for (let i = 1; i <= TOTAL_RESUME_STEPS; i++) {
                const cv = document.getElementById('resume-step-' + i);
                if (cv) cv.classList.remove('active');
                const pill = document.getElementById('resume-pill-' + i);
                if (pill) pill.classList.remove('active');
            }
            const activeCanvas = document.getElementById('resume-step-' + stepNum);
            if (activeCanvas) activeCanvas.classList.add('active');

            const activePill = document.getElementById('resume-pill-' + stepNum);
            if (activePill) activePill.classList.add('active');
        }

        function handleResumeCanvasClick(nextStep) {
            jumpResumeStep(nextStep);
        }

        /* -------------------------------------------------------------
           포트폴리오 서브 탭 & 문서함
        ------------------------------------------------------------- */
        function switchPortfolioTab(tabId, btn) {
            document.querySelectorAll('#page-portfolio .sub-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('#page-portfolio .sub-tab-btn').forEach(b => b.classList.remove('active'));
            const target = document.getElementById(tabId);
            if (target) target.classList.add('active');
            if (btn) btn.classList.add('active');
            if (tabId === 'portfolio-docs') loadPortfolioDocuments();
        }

        // 정적 Fallback 데이터 (서버 지연 시에도 즉각 100% 렌더링)
        const staticDocCategories = [
            {
                category: '공식 제출 서류 (이력서 및 자기소개서)',
                badge: 'CAREER & ESSAY',
                items: [
                    { name: '20260901_12-3_이력서_Ver01_정승운.pdf', title: '정승운 이력서 Ver01', desc: '인적사항, 기술 스택, 영화 및 게임 개발 프로젝트 이력, 학력 상세 기재 원본', type: 'PDF', folder: 'root', sizeFormatted: '55 KB' },
                    { name: '20260904_13-1_자기소개서_Ver01_정승운.pdf', title: '정승운 자기소개서 Ver01', desc: '지원 동기, AI 행동 트리 전투 로직 구축 역량, UI 리소스 갈등 조율 및 문제 해결 경험', type: 'PDF', folder: 'root', sizeFormatted: '45 KB' }
                ]
            },
            {
                category: '프로젝트 기획서 (슬기로운 재배생활 / 파송송계란탁)',
                badge: 'GDD & DESIGN',
                items: [
                    { name: '0705_슬기로운재배생활컨셉기획서_Ver01.pdf', title: '슬기로운 재배생활 컨셉 기획서 Ver01', desc: '게임의 핵심 플레이 루프, 타겟층, 세계관 및 힐링 재배 시뮬레이션 초기 컨셉 정의', type: 'PDF', folder: 'portfolio', sizeFormatted: '2.7 MB' },
                    { name: '0708_비주얼 가이드_Ver05.pdf', title: '슬기로운 재배생활 비주얼 가이드 Ver05', desc: '게임 내 아트 스타일 가이드라인, 컬러 팔레트, 타일셋 및 오브젝트 규격 정의', type: 'PDF', folder: 'portfolio', sizeFormatted: '3.9 MB' },
                    { name: '0709_UI화면기획_ver05.pdf', title: '슬기로운 재배생활 UI 화면 기획서 Ver05', desc: '각 화면별 UI 플로우, 슬롯 타이머 표시 규격, 인벤토리/제작 화면 상세 와이어프레임', type: 'PDF', folder: 'portfolio', sizeFormatted: '5.4 MB' },
                    { name: '0718_시스템기획서_Ver03.pdf', title: '슬기로운 재배생활 시스템 기획서 Ver03', desc: '재배, 수확, 가공, 무역 연계 경제 사이클 및 유한 상태 객체 인터랙션 시스템', type: 'PDF', folder: 'portfolio', sizeFormatted: '1.3 MB' },
                    { name: '20260722_7-5_컨셉기획서_Ver05_파송송계란탁 (1).pdf', title: '파송송계란탁 컨셉 기획서 Ver05', desc: '팀 파송송계란탁 프로젝트 통합 컨셉 기획서 및 코어 메커니즘 정리', type: 'PDF', folder: 'portfolio', sizeFormatted: '3.6 MB' }
                ]
            },
            {
                category: '캐릭터 & 세계관 가이드 (PPTX)',
                badge: 'CHARACTER & WORLD',
                items: [
                    { name: '20260810_캐릭터가이드_Ver02_파송송계란탁.pptx', title: '캐릭터 가이드 Ver02', desc: '등장 캐릭터들의 전반적인 설정, 성격, 모션 및 대사 톤앤매너 통합 가이드', type: 'PPTX', folder: 'portfolio', sizeFormatted: '18.8 MB' },
                    { name: '20260828_세라피엘 기획서_Ver01_파송송계란탁.pptx', title: '캐릭터 기획서: 세라피엘 (Seraphiel)', desc: '세라피엘 캐릭터 설정, 외형 특징, 고유 스킬 및 배경 시나리오 기획서', type: 'PPTX', folder: 'portfolio', sizeFormatted: '2.8 MB' },
                    { name: '20260828_시안 기획서_Ver01_파송송계란탁.pptx', title: '캐릭터 기획서: 시안 (Cyan)', desc: '시안 캐릭터 성격, 전투 메커니즘, 기획 의도 및 상호작용 트리', type: 'PPTX', folder: 'portfolio', sizeFormatted: '2.7 MB' },
                    { name: '20260828_아르세니아 기획서_Ver01_파송송계란탁.pptx', title: '캐릭터 기획서: 아르세니아 (Arsenia)', desc: '아르세니아 캐릭터 컨셉, 스킬 셋, 그래픽 레퍼런스 및 밸런스 지표', type: 'PPTX', folder: 'portfolio', sizeFormatted: '2.7 MB' },
                    { name: '20260828_엘린 기획서_Ver01_파송송계란탁.pptx', title: '캐릭터 기획서: 엘린 (Elin)', desc: '엘린 캐릭터 프로필, 감정 표현 스프라이트 기획 및 퀘스트 연계', type: 'PPTX', folder: 'portfolio', sizeFormatted: '2.6 MB' },
                    { name: '20260901_유물발굴기획서_Ver01_파송송계란탁.pptx', title: '유물 발굴 시스템 기획서 Ver01', desc: '유물 탐색 및 발굴 미니게임 시스템, 보상 테이블 및 유물 도감 기획', type: 'PPTX', folder: 'portfolio', sizeFormatted: '360 KB' }
                ]
            },
            {
                category: '시스템 밸런스 & 데이터 테이블 (XLSX)',
                badge: 'DATA & BALANCE',
                items: [
                    { name: '재배테이블.xlsx', title: '작물 재배 데이터 테이블', desc: '작물별 생장 시간, 필요 영양분, 수확량, 단계별 스프라이트 매핑', type: 'XLSX', folder: 'portfolio', sizeFormatted: '10 KB' },
                    { name: '제조테이블.xlsx', title: '가공 및 제조 레시피 테이블', desc: '조합 공식, 제조 소요 시간, 결과물 티어 및 숙련도별 보너스', type: 'XLSX', folder: 'portfolio', sizeFormatted: '16 KB' },
                    { name: '무역소 테이블.xlsx', title: '무역소 경제 및 시세 변동 테이블', desc: '지역별 거래 품목, 기준 가격, 시세 변동 알고리즘 및 마진율', type: 'XLSX', folder: 'portfolio', sizeFormatted: '13 KB' },
                    { name: '캐릭터테이블.xlsx', title: '캐릭터 스탯 및 성장 테이블', desc: '레벨별 스탯 성장 곡선, 필요 경험치, 특성 해금 조건', type: 'XLSX', folder: 'portfolio', sizeFormatted: '13 KB' },
                    { name: '설명 테이블.xlsx', title: '게임 내 툴팁 및 설명 텍스트 테이블', desc: '아이템, 버프/디버프, 도움말 텍스트 ID 및 다국어 대비 텍스트', type: 'XLSX', folder: 'portfolio', sizeFormatted: '14 KB' },
                    { name: '0708_마일스톤_Ver01.xlsx', title: '개발 일정 마일스톤 관리 시트', desc: '주차별 개발 목표, 스프린트 관리, 파트별(기획/아트/클라) R&R 분배', type: 'XLSX', folder: 'portfolio', sizeFormatted: '74 KB' },
                    { name: '0717_QA 구동 확인_Ver01.xlsx', title: 'QA 테스트 체크리스트 및 구동 확인 시트', desc: '빌드별 기능 검증 체크리스트, 발견된 버그 현황 및 해결 상태 추적', type: 'XLSX', folder: 'portfolio', sizeFormatted: '21 KB' }
                ]
            }
        ];

        async function loadPortfolioDocuments() {
            const container = document.getElementById('documentsArchiveContainer');
            if (!container) return;

            let categories = staticDocCategories;
            try {
                const res = await fetch(`${API_BASE}/api/portfolio-documents`);
                if (res.ok) {
                    categories = await res.json();
                }
            } catch(e) {
                console.log('서버 오프라인 모드: 정적 문서 목록을 표시합니다.');
            }

            renderDocArchive(categories, container);
        }

        function renderDocArchive(categories, container) {
            container.innerHTML = '';
            categories.forEach(cat => {
                const section = document.createElement('div');
                section.className = 'doc-category-section';

                let cardsHtml = '';
                cat.items.forEach(item => {
                    const downloadUrl = item.url || `${API_BASE}/api/download?file=${encodeURIComponent(item.name)}&folder=${item.folder || 'portfolio'}`;
                    const isPdf = item.type === 'PDF';
                    
                    cardsHtml += `
                        <div class="doc-item-card">
                            <div class="doc-info">
                                <div class="doc-title-row">
                                    <span class="doc-type-badge">${item.type}</span>
                                    <div class="doc-title" title="${item.title}">${item.title}</div>
                                </div>
                                <div class="doc-desc">${item.desc}</div>
                                <div style="font-family:var(--font-mono); font-size:11px; color:var(--color-iris-violet); margin-top:6px;">
                                    크기: ${item.sizeFormatted || '확인 중'}
                                </div>
                            </div>
                            <div class="doc-actions">
                                ${isPdf ? `<a href="${downloadUrl}" target="_blank" class="btn-ghost" style="padding:6px 12px; font-size:12px; text-align:center;">열람 ↗</a>` : ''}
                                <a href="${downloadUrl}" download class="btn-ghost" style="padding:6px 12px; font-size:12px; text-align:center;">다운로드 ↓</a>
                            </div>
                        </div>
                    `;
                });

                section.innerHTML = `
                    <div class="doc-cat-header">
                        <span class="doc-badge">${cat.badge}</span>
                        <h3 class="doc-cat-title">${cat.category}</h3>
                        <span style="font-size:12px; color:var(--color-ash-gray); font-family:var(--font-mono);">(${cat.items.length}개 파일)</span>
                    </div>
                    <div class="doc-cards-grid">${cardsHtml}</div>
                `;
                container.appendChild(section);
            });
        }

        /* -------------------------------------------------------------
           IGDB 실시간 게임 검색 모달
        ------------------------------------------------------------- */
        function openGameSearchModal() {
            document.getElementById('gameSearchModal').style.display = 'block';
            document.getElementById('gameQueryInput').focus();
        }

        function closeGameSearchModal() {
            document.getElementById('gameSearchModal').style.display = 'none';
        }

        async function executeGameSearch() {
            const query = document.getElementById('gameQueryInput').value.trim();
            const container = document.getElementById('gameSearchResults');
            if (!query) {
                alert('검색어를 입력해주세요.');
                return;
            }

            container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;"><span style="font-size:24px;">⏳</span><br>IGDB 공식 데이터베이스에서 검색 중입니다...</div>';

            try {
                const res = await fetch(`${API_BASE}/api/search-games?q=${encodeURIComponent(query)}`);
                if (!res.ok) {
                    const errJson = await res.json().catch(() => ({}));
                    throw new Error(errJson.error || '서버 응답 오류');
                }
                const games = await res.json();

                if (!games || games.length === 0) {
                    container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;">검색 결과가 없습니다. 다른 게임명을 입력해보세요.</div>';
                    return;
                }

                container.innerHTML = '';
                games.forEach(game => {
                    const row = document.createElement('div');
                    row.style.cssText = 'display:flex; align-items:center; gap:14px; padding:12px 16px; border-bottom:1px solid var(--color-graphite-hairline); cursor:pointer; transition:background 0.2s;';
                    row.onmouseover = () => row.style.background = 'rgba(146,129,247,0.08)';
                    row.onmouseout = () => row.style.background = '';

                    const imgHtml = game.coverUrl 
                        ? `<img src="${game.coverUrl}" style="width:45px; height:60px; object-fit:cover; border-radius:6px; border:1px solid var(--color-graphite-hairline);" />`
                        : `<div style="width:45px; height:60px; background:#1a1c24; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:10px; color:#888;">NO IMG</div>`;

                    row.innerHTML = `
                        ${imgHtml}
                        <div style="flex:1; min-width:0;">
                            <div style="font-weight:600; color:#fff; font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                ${game.title} ${game.releaseYear ? `(${game.releaseYear})` : ''}
                            </div>
                            <div style="font-size:11px; color:var(--color-ash-gray); font-family:var(--font-mono); margin-top:2px;">
                                플랫폼: ${game.platform} | 장르: ${game.genre}
                            </div>
                        </div>
                        <button class="btn-ghost" style="padding:6px 14px; font-size:12px;" onclick="addGameToGrid(${JSON.stringify(game).replace(/"/g, '&quot;')})">히스토리 추가 +</button>
                    `;
                    container.appendChild(row);
                });

            } catch(e) {
                container.innerHTML = `<div style="color:#ff6b6b; text-align:center; padding:30px;">⚠️ 검색 오류: ${e.message}<br><small style="color:var(--color-ash-gray);">서버 상태: ${API_BASE}</small></div>`;
            }
        }

        function addGameToGrid(game) {
            const grid = document.getElementById('full-play-grid');
            if (!grid) return;

            const card = document.createElement('div');
            card.className = 'play-card';
            card.innerHTML = `
                <div class="play-thumb"><img src="${game.coverUrl || 'lastsanctuary.png'}" alt="${game.title}"></div>
                <div class="play-content">
                    <div class="play-title">${game.title}</div>
                    <div class="play-meta">${game.genre} / ${game.releaseYear || '신규 등록'}</div>
                    <div class="play-insight">IGDB에서 실시간 연동 등록된 게임입니다. 기획적 코어 메커니즘을 지속 분석 중입니다.</div>
                </div>
            `;
            grid.prepend(card);
            closeGameSearchModal();
            alert(`[${game.title}] 게임이 플레이 히스토리에 성공적으로 추가되었습니다!`);
        }

        /* -------------------------------------------------------------
           프로젝트 모달 및 편집 모드
        ------------------------------------------------------------- */
        const projectData = {
            project1: `
                <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-bottom:8px;">SYSTEM PLANNING &amp; AI ARCHITECTURE</div>
                <h2 style="color:#fff; font-size:26px; margin-bottom:16px;">PC 게임 &lt;LAST SANCTUARY&gt; 상세 기획서</h2>
                <div style="margin-bottom:20px; border-radius:12px; overflow:hidden; border:1px solid var(--color-graphite-hairline); max-height:300px; display:flex; justify-content:center; background:#000;">
                    <img src="lastsanctuary.png" style="max-width:100%; object-fit:contain;" />
                </div>
                <h4 style="color:#fff; margin-bottom:8px; font-size:16px;">1. 프로젝트 개요</h4>
                <p style="color:var(--color-ash-gray); line-height:1.7; margin-bottom:16px;">
                    포스트 아포칼립스 세계관 기반의 PC 액션 RPG. 시스템 기획자로서 전체 전투 사이클 및 유한 상태 머신(FSM) 기반의 AI 행동 트리(Behavior Tree) 구조를 설계하고 유니티 바이브 코딩으로 구현했습니다.
                </p>
                <h4 style="color:#fff; margin-bottom:8px; font-size:16px;">2. 핵심 기획 기여</h4>
                <ul style="color:var(--color-ash-gray); line-height:1.7; padding-left:20px; margin-bottom:20px;">
                    <li>단일 스크립트로 얽혀있던 전투 AI를 행동 단위 모듈로 분리하여 예외 상황 95% 감소</li>
                    <li>적 AI의 시야각, 청각 인지 범위, 상태 전이 조건 테이블 구조화</li>
                    <li>공식 티저 메인 PV 영상 제작 총괄 (프리미어 프로 컷 편집, 색보정)</li>
                </ul>
            `,
            project2: `
                <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-iris-violet); margin-bottom:8px;">SIMULATION &amp; ECONOMY BALANCING</div>
                <h2 style="color:#fff; font-size:26px; margin-bottom:16px;">PC 게임 &lt;슬기로운 재배생활&gt; 상세 기획서</h2>
                <div style="margin-bottom:20px; border-radius:12px; overflow:hidden; border:1px solid var(--color-graphite-hairline); max-height:300px; display:flex; justify-content:center; background:#000;">
                    <img src="슬기로운재배생활.png" style="max-width:100%; object-fit:contain;" />
                </div>
                <h4 style="color:#fff; margin-bottom:8px; font-size:16px;">1. 프로젝트 개요</h4>
                <p style="color:var(--color-ash-gray); line-height:1.7; margin-bottom:16px;">
                    팀 WEED HOLDINGS의 팀장(PD)으로서 기획, 아트, 클라이언트 간의 협업을 총괄하고 재배, 제조, 무역으로 이어지는 경제 순환 루프를 기획한 힐링 시뮬레이션 게임입니다.
                </p>
                <h4 style="color:#fff; margin-bottom:8px; font-size:16px;">2. 핵심 기획 기여</h4>
                <ul style="color:var(--color-ash-gray); line-height:1.7; padding-left:20px; margin-bottom:20px;">
                    <li>엑셀 기반 작물 성장 곡선, 비료 시너지 및 시세 변동 알고리즘 설계</li>
                    <li>UI 슬롯 타이머 표시 리소스 재활용 절충안 제시를 통한 팀원 갈등 해결 및 개발 비용 절감</li>
                    <li>주차별 마일스톤 시트 및 QA 기능 검증 체크리스트 수립 및 운용</li>
                </ul>
            `
        };

        function openModal(projectId) {
            document.getElementById('modalBody').innerHTML = projectData[projectId] || '';
            document.getElementById('projectModal').style.display = 'block';
        }

        function closeModal() {
            document.getElementById('projectModal').style.display = 'none';
        }

        let isEditMode = false;
        function toggleEditMode() {
            isEditMode = !isEditMode;
            const btn = document.getElementById('editToggleBtn');
            const editables = document.querySelectorAll('[contenteditable]');
            if (isEditMode) {
                btn.classList.add('active');
                btn.innerText = '편집 모드 ON (저장)';
                editables.forEach(el => el.setAttribute('contenteditable', 'true'));
            } else {
                btn.classList.remove('active');
                btn.innerText = '편집 모드 OFF';
                editables.forEach(el => el.setAttribute('contenteditable', 'false'));
            }
        }

        // 초기화 실행
        document.addEventListener('DOMContentLoaded', () => {
            startMainAutoTimer();
        });
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("index.html fully rebuilt! Length:", len(html_code))
