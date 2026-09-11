# build_index.py - 완전 개편: 이력 소개(5단계 풀캔버스 순환) / 자기소개서 분리 / 삼각 파라미터 비율 100% 정합 / IGDB 라이브 연동

import os

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
            --color-deep-space: #0f1117;
            --color-graphite-surface: #151821;
            --color-graphite-hairline: #222634;
            --color-iris-violet: #9281f7;
            --color-iris-light: #b4a8fb;
            --color-iris-glow: rgba(146, 129, 247, 0.25);
            --color-pure-white: #ffffff;
            --color-off-white: #f3f4f8;
            --color-ash-gray: #9ba1b0;
            --color-charcoal-muted: #5e6475;
            --color-neon-accent: #00f2fe;
            --font-display: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
            --font-mono: "Commit Mono", monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        html, body {
            width: 100%;
            height: 100%;
            background-color: var(--color-carbon);
            color: var(--color-pure-white);
            font-family: var(--font-display);
            overflow-x: hidden;
        }

        /* -------------------------------------------------------------
           Header & Fixed Top Nav (이력 소개 / 자기소개서 완벽 분리)
        ------------------------------------------------------------- */
        header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 72px;
            background: rgba(8, 9, 13, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--color-graphite-hairline);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
        }

        .brand-logo {
            font-family: var(--font-mono);
            font-size: 17px;
            font-weight: 700;
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: var(--color-pure-white);
            cursor: pointer;
        }

        .brand-badge {
            background: rgba(146, 129, 247, 0.15);
            color: var(--color-iris-violet);
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid rgba(146, 129, 247, 0.3);
            letter-spacing: 1px;
        }

        nav {
            display: flex;
            align-items: center;
            gap: 28px;
        }

        .nav-link {
            color: var(--color-ash-gray);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 12px;
            border-radius: 6px;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
            background: transparent;
        }

        .nav-link:hover {
            color: var(--color-pure-white);
            background: rgba(255, 255, 255, 0.05);
        }

        .nav-link.active {
            color: var(--color-iris-violet);
            background: rgba(146, 129, 247, 0.12);
            font-weight: 600;
        }

        .edit-toggle-btn {
            background: transparent;
            border: 1px solid var(--color-graphite-hairline);
            color: var(--color-ash-gray);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
            font-family: var(--font-mono);
        }

        .edit-toggle-btn.active {
            background: var(--color-iris-violet);
            border-color: var(--color-iris-violet);
            color: #000;
            font-weight: 700;
        }

        /* -------------------------------------------------------------
           Page Containers
        ------------------------------------------------------------- */
        .page-section {
            display: none;
            min-height: 100vh;
            padding-top: 72px;
            position: relative;
        }

        .page-section.active {
            display: block;
        }

        /* -------------------------------------------------------------
           1. 메인 페이지: 2페이지 자동 전환 후 정지, 복귀 시 항상 1페이지 초기화
        ------------------------------------------------------------- */
        #page-main {
            height: 100vh;
            overflow: hidden;
            position: relative;
            padding-top: 0;
        }

        .main-step-container {
            width: 100%;
            height: 100%;
            position: relative;
        }

        .main-step {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.8s ease, visibility 0.8s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .main-step.active {
            opacity: 1;
            visibility: visible;
        }

        /* 메인 1페이지: main 1.png 배경 */
        .main-step-1 {
            background: url('main 1.png') center center / cover no-repeat;
        }

        .main-step-1-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(8,9,13,0.3) 0%, rgba(8,9,13,0.6) 100%);
        }

        .main-step-1-content {
            position: relative;
            z-index: 2;
            max-width: 900px;
            text-align: center;
            padding: 0 24px;
        }

        .logline-sub {
            font-family: var(--font-mono);
            font-size: 13px;
            letter-spacing: 4px;
            color: var(--color-iris-violet);
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        .logline-title {
            font-size: 52px;
            font-weight: 800;
            line-height: 1.25;
            letter-spacing: -1.5px;
            margin-bottom: 24px;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
        }

        .logline-desc {
            font-size: 18px;
            color: var(--color-off-white);
            line-height: 1.7;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
            margin-bottom: 36px;
        }

        /* 메인 2페이지: main2.png 밝은 배경 & 핵심 역량 및 이동 버튼 */
        .main-step-2 {
            background: url('main2.png') center center / cover no-repeat;
        }

        .main-step-2-overlay {
            position: absolute;
            inset: 0;
            /* 배경 이미지가 돋보이도록 어두운 딤을 최소화 */
            background: radial-gradient(circle at center, rgba(8, 9, 13, 0.4) 0%, rgba(8, 9, 13, 0.75) 100%);
        }

        .main-step-2-content {
            position: relative;
            z-index: 2;
            width: 100%;
            max-width: 1100px;
            padding: 0 32px;
            text-align: center;
        }

        .main-step-indicators {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            z-index: 10;
        }

        .main-step-dot {
            width: 36px;
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .main-step-dot.active {
            background: var(--color-iris-violet);
            width: 54px;
        }

        .competence-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 40px;
        }

        .competence-card {
            background: rgba(15, 17, 23, 0.82);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 28px 24px;
            text-align: left;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }

        .competence-card:hover {
            transform: translateY(-4px);
            border-color: var(--color-iris-violet);
        }

        .competence-icon-wrap {
            font-size: 32px;
            margin-bottom: 14px;
        }

        .competence-title {
            font-size: 19px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
        }

        .competence-desc {
            font-size: 14px;
            color: var(--color-ash-gray);
            line-height: 1.6;
        }

        .main-cta-group {
            display: flex;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
        }

        .btn-primary {
            background: var(--color-iris-violet);
            color: #0b0d13;
            font-weight: 700;
            font-size: 15px;
            padding: 13px 28px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
            box-shadow: 0 4px 20px var(--color-iris-glow);
        }

        .btn-primary:hover {
            background: var(--color-iris-light);
            transform: translateY(-2px);
        }

        .btn-ghost {
            background: rgba(255, 255, 255, 0.06);
            color: var(--color-pure-white);
            font-weight: 600;
            font-size: 15px;
            padding: 13px 26px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
        }

        .btn-ghost:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--color-pure-white);
        }

        /* -------------------------------------------------------------
           2. 이력 소개 페이지: 메인처럼 화면을 꽉 채우는 5단계 풀 캔버스 쇼케이스
           - 01~05 순서 표기, 클릭 시 다음 단계, 5단계에서 클릭 시 다시 1단계로 순환
        ------------------------------------------------------------- */
        #page-resume {
            height: 100vh;
            overflow: hidden;
            position: relative;
            padding-top: 0;
            cursor: pointer;
        }

        .showcase-stage {
            position: absolute;
            inset: 0;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.6s ease, visibility 0.6s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 80px 48px 48px;
        }

        .showcase-stage.active {
            opacity: 1;
            visibility: visible;
        }

        /* 단계 번호 인디케이터 (상단 고정) */
        .showcase-nav-bar {
            position: absolute;
            top: 90px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 20px;
            z-index: 50;
            background: rgba(15, 17, 23, 0.85);
            backdrop-filter: blur(12px);
            padding: 8px 24px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .showcase-step-num {
            font-family: var(--font-mono);
            font-size: 13px;
            color: var(--color-charcoal-muted);
            cursor: pointer;
            transition: all 0.2s;
        }

        .showcase-step-num.active {
            color: var(--color-iris-violet);
            font-weight: 700;
            font-size: 15px;
            text-shadow: 0 0 10px var(--color-iris-violet);
        }

        .showcase-hint {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--color-ash-gray);
            background: rgba(0, 0, 0, 0.5);
            padding: 6px 16px;
            border-radius: 20px;
            z-index: 50;
            pointer-events: none;
            animation: pulseHint 2s infinite ease-in-out;
        }

        @keyframes pulseHint {
            0%, 100% { opacity: 0.5; transform: translate(-50%, 0); }
            50% { opacity: 1; transform: translate(-50%, -4px); }
        }

        /* 슬라이드 1: 밝은 main2.png 배경 + 투명배경 인물 누끼(좌측) + 인적사항(우측) */
        .stage-1-wrap {
            width: 100%;
            max-width: 1200px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 60px;
            z-index: 2;
        }

        .stage-1-bg {
            position: absolute;
            inset: 0;
            background: url('main2.png') center center / cover no-repeat;
            opacity: 0.55;
            filter: brightness(1.05);
        }

        .profile-cutout-img {
            max-height: 72vh;
            max-width: 480px;
            object-fit: contain;
            filter: drop-shadow(0 10px 30px rgba(0,0,0,0.8));
            animation: slideInLeft 0.8s ease-out;
        }

        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-40px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .profile-info-card {
            flex: 1;
            background: rgba(15, 17, 23, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px 44px;
            animation: fadeInRight 0.8s ease-out;
        }

        @keyframes fadeInRight {
            from { opacity: 0; transform: translateX(40px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .profile-tag {
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--color-iris-violet);
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        .profile-name {
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 6px;
        }

        .profile-title-sub {
            font-size: 17px;
            color: var(--color-ash-gray);
            margin-bottom: 24px;
        }

        .profile-details-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            border-top: 1px solid var(--color-graphite-hairline);
            padding-top: 20px;
        }

        .profile-detail-item label {
            font-size: 11px;
            color: var(--color-charcoal-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            display: block;
            margin-bottom: 4px;
        }

        .profile-detail-item span {
            font-size: 14.5px;
            color: var(--color-off-white);
            font-weight: 500;
        }

        /* 슬라이드 2: 가시성 높은 Unity + Adobe + Docs 아이콘 중앙 정렬 및 하단 설명 */
        .stage-2-wrap {
            max-width: 1050px;
            width: 100%;
            text-align: center;
            z-index: 2;
        }

        .tools-icon-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 32px;
            margin: 40px 0;
            flex-wrap: wrap;
        }

        .tool-icon-box {
            width: 90px;
            height: 90px;
            background: rgba(21, 24, 33, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }

        .tool-icon-box:hover {
            transform: translateY(-8px) scale(1.05);
            border-color: var(--color-iris-violet);
            box-shadow: 0 12px 32px var(--color-iris-glow);
        }

        .tool-icon-box img {
            width: 44px;
            height: 44px;
            object-fit: contain;
        }

        .tool-name {
            font-size: 12px;
            font-weight: 600;
            color: var(--color-off-white);
        }

        .tools-desc-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            text-align: left;
            margin-top: 24px;
        }

        .tool-desc-card {
            background: rgba(15, 17, 23, 0.8);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 14px;
            padding: 20px;
        }

        .tool-desc-card h4 {
            font-size: 16px;
            color: var(--color-iris-light);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tool-desc-card p {
            font-size: 13.5px;
            color: var(--color-ash-gray);
            line-height: 1.6;
        }

        /* 슬라이드 3: 프로젝트 대표 이미지 + 데블다이스/제임스텍 로고 및 설명 */
        .stage-3-wrap {
            max-width: 1100px;
            width: 100%;
            z-index: 2;
        }

        .project-cards-dual {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 32px;
            margin-top: 36px;
        }

        .project-show-card {
            background: rgba(15, 17, 23, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .project-show-card:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-6px);
        }

        .project-show-img {
            width: 100%;
            height: 220px;
            object-fit: cover;
            border-bottom: 1px solid var(--color-graphite-hairline);
        }

        .project-show-body {
            padding: 24px;
        }

        .project-company-badge {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 14px;
        }

        .project-company-badge img {
            height: 26px;
            max-width: 110px;
            object-fit: contain;
            background: #fff;
            padding: 2px 6px;
            border-radius: 4px;
        }

        .project-show-title {
            font-size: 20px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 8px;
        }

        .project-show-desc {
            font-size: 13.5px;
            color: var(--color-ash-gray);
            line-height: 1.65;
        }

        /* 슬라이드 4: 참여 영화 목록(좌측) + 왼쪽을 비추는 35mm 영화 카메라 애니메이션(우측) */
        .stage-4-wrap {
            max-width: 1200px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 50px;
            z-index: 2;
        }

        .film-list-col {
            flex: 1.2;
        }

        .film-camera-col {
            flex: 0.8;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        /* 35mm 빈티지 영화 카메라 SVG (렌즈가 왼쪽의 영화 리스트를 비추도록 반전) */
        .vintage-camera-svg {
            width: 320px;
            height: 320px;
            filter: drop-shadow(0 0 35px var(--color-iris-glow));
        }

        .film-projector-beam {
            position: absolute;
            top: 38%;
            right: 210px;
            width: 320px;
            height: 160px;
            background: linear-gradient(270deg, rgba(146, 129, 247, 0.35) 0%, rgba(146, 129, 247, 0.0) 100%);
            clip-path: polygon(100% 45%, 0% 0%, 0% 100%, 100% 55%);
            pointer-events: none;
            animation: beamFlicker 3s infinite alternate;
        }

        @keyframes beamFlicker {
            0% { opacity: 0.4; }
            50% { opacity: 0.8; }
            100% { opacity: 0.6; }
        }

        .film-items-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 20px;
            max-height: 55vh;
            overflow-y: auto;
            padding-right: 8px;
        }

        .film-badge-item {
            background: rgba(15, 17, 23, 0.8);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 10px;
            padding: 12px 14px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .film-badge-role {
            background: rgba(146, 129, 247, 0.15);
            color: var(--color-iris-violet);
            font-size: 11px;
            padding: 3px 6px;
            border-radius: 4px;
            font-weight: 600;
            white-space: nowrap;
        }

        .film-badge-title {
            font-size: 13.5px;
            color: #fff;
            font-weight: 600;
        }

        /* 슬라이드 5: 동국대학교 학력 및 융합 기획 역량 */
        .stage-5-wrap {
            max-width: 960px;
            width: 100%;
            text-align: center;
            z-index: 2;
        }

        .dongguk-box {
            background: rgba(15, 17, 23, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 48px 40px;
            margin-top: 32px;
        }

        .dongguk-logo-img {
            height: 70px;
            object-fit: contain;
            background: #fff;
            padding: 8px 18px;
            border-radius: 12px;
            margin-bottom: 24px;
        }

        .academic-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 32px;
            text-align: left;
        }

        .academic-card {
            background: rgba(21, 24, 33, 0.7);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 14px;
            padding: 20px;
        }

        /* -------------------------------------------------------------
           3. 자기소개서 페이지: 단독 분리 & 사용자 원문 100% 온전 수록
        ------------------------------------------------------------- */
        #page-coverletter {
            padding: 100px 48px 80px;
            max-width: 1100px;
            margin: 0 auto;
        }

        .section-header-box {
            text-align: center;
            margin-bottom: 50px;
        }

        .section-title {
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 12px;
        }

        .section-desc {
            font-size: 16px;
            color: var(--color-ash-gray);
        }

        .coverletter-grid {
            display: flex;
            flex-direction: column;
            gap: 32px;
        }

        .essay-card {
            background: rgba(15, 17, 23, 0.85);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 18px;
            padding: 36px 40px;
            position: relative;
            overflow: hidden;
            transition: border-color 0.25s;
        }

        .essay-card:hover {
            border-color: rgba(146, 129, 247, 0.4);
        }

        .essay-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--color-iris-violet);
        }

        .essay-num {
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--color-iris-violet);
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .essay-title {
            font-size: 22px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 20px;
        }

        .essay-body {
            font-size: 15px;
            color: #cfd3dc;
            line-height: 1.85;
            white-space: pre-line;
        }

        /* -------------------------------------------------------------
           4. 포트폴리오 페이지: 문서 보관함 및 프로젝트
        ------------------------------------------------------------- */
        #page-portfolio {
            padding: 100px 48px 80px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .docs-category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 28px;
        }

        .doc-item-card {
            background: rgba(15, 17, 23, 0.8);
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 14px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s;
        }

        .doc-item-card:hover {
            border-color: var(--color-iris-violet);
            transform: translateY(-3px);
        }

        /* -------------------------------------------------------------
           5. 플레이 히스토리 페이지: 삼각 파라미터 비율 100% 일치 복구
        ------------------------------------------------------------- */
        #page-playhistory {
            padding: 100px 48px 80px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .radar-triangle-container {
            background: rgba(15, 17, 23, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
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
            transform: translateY(-4px);
        }

        .play-cover-img {
            width: 120px;
            height: 160px;
            object-fit: cover;
            flex-shrink: 0;
        }

        .play-card-body {
            padding: 16px 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .play-card-title {
            font-size: 16px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 4px;
        }

        .play-card-meta {
            font-size: 12px;
            color: var(--color-iris-violet);
            font-family: var(--font-mono);
            margin-bottom: 8px;
        }

        .play-card-desc {
            font-size: 13px;
            color: var(--color-ash-gray);
            line-height: 1.5;
        }

        /* -------------------------------------------------------------
           IGDB 실시간 검색 모달 (강화된 UX & 라이브 뱃지 & 즉시 추천)
        ------------------------------------------------------------- */
        .modal-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(12px);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-box {
            background: #0f1118;
            border: 1px solid rgba(146, 129, 247, 0.3);
            border-radius: 20px;
            width: 100%;
            max-width: 760px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        }

        .modal-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--color-graphite-hairline);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .server-live-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-family: var(--font-mono);
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
            padding: 4px 10px;
            border-radius: 12px;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .server-live-dot {
            width: 7px;
            height: 7px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
            animation: liveBlink 1.5s infinite;
        }

        @keyframes liveBlink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        .modal-search-bar {
            padding: 16px 24px;
            background: rgba(21, 24, 33, 0.6);
            border-bottom: 1px solid var(--color-graphite-hairline);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .search-input-group {
            display: flex;
            gap: 10px;
        }

        .modal-input {
            flex: 1;
            background: #151821;
            border: 1px solid var(--color-graphite-hairline);
            border-radius: 8px;
            padding: 12px 16px;
            color: #fff;
            font-size: 14px;
            outline: none;
        }

        .modal-input:focus {
            border-color: var(--color-iris-violet);
        }

        .quick-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .chip-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--color-ash-gray);
            font-size: 11.5px;
            padding: 4px 10px;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .chip-btn:hover {
            background: rgba(146, 129, 247, 0.2);
            color: #fff;
            border-color: var(--color-iris-violet);
        }

        .modal-results-list {
            flex: 1;
            overflow-y: auto;
            padding: 12px 24px;
            min-height: 240px;
        }

        /* 토스트 알림 */
        .toast-msg {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--color-iris-violet);
            color: #000;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13.5px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s;
            z-index: 3000;
            pointer-events: none;
        }

        .toast-msg.show {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
</head>
<body>

    <!-- -------------------------------------------------------------
         Header & Navigation (이력 소개 / 자기소개서 분리)
    ------------------------------------------------------------- -->
    <header>
        <div class="brand-logo" onclick="switchPage('main', document.getElementById('nav-btn-main'))">
            <span>SEUNGWOON.DEV</span>
            <span class="brand-badge">PORTFOLIO</span>
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

    <!-- -------------------------------------------------------------
         1. 메인 페이지: 10초 후 2페이지로 전환 후 2페이지에서 정지, 
            다른 메뉴 갔다가 돌아오면 1페이지로 리셋되고 10초 타이머 재가동
    ------------------------------------------------------------- -->
    <section id="page-main" class="page-section active">
        <div class="main-step-container">
            <!-- 메인 스텝 1: 타이틀 및 로그라인 -->
            <div class="main-step main-step-1 active" id="mainStep1">
                <div class="main-step-1-overlay"></div>
                <div class="main-step-1-content">
                    <div class="logline-sub">Game System & Economy Designer</div>
                    <h1 class="logline-title">탄탄한 논리로 상상하고,<br>수치와 시스템으로 증명하는 크리에이터</h1>
                    <p class="logline-desc">영화적 서사 구조와 게임 엔진(Unity) 기술, 정밀한 엑셀 수치 밸런싱 역량을 결합하여<br>유저가 몰입할 수밖에 없는 유기적인 게임 메카닉을 설계합니다.</p>
                    <div class="main-cta-group">
                        <button class="btn-primary" onclick="setMainStep(2)">
                            <span>핵심 역량 및 소개 보기</span>
                            <span>→</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- 메인 스텝 2: 밝은 main2.png 배경 & 핵심 강점 & 페이지 이동 바로가기 -->
            <div class="main-step main-step-2" id="mainStep2">
                <div class="main-step-2-overlay"></div>
                <div class="main-step-2-content">
                    <div class="logline-sub" style="color:var(--color-iris-light);">CORE COMPETENCIES & HIGHLIGHTS</div>
                    <h2 style="font-size:36px; font-weight:800; margin-bottom:32px;">데이터 기반 기획과 내러티브의 융합</h2>
                    
                    <div class="competence-grid">
                        <div class="competence-card">
                            <div class="competence-icon-wrap">🎮</div>
                            <div class="competence-title">시스템 & 밸런싱 설계</div>
                            <div class="competence-desc">재화 순환 수식, 레벨 디자인, 타일 경제 및 FSM 상태 머신 기반의 정밀하고 안정적인 코어 루프 설계.</div>
                        </div>
                        <div class="competence-card">
                            <div class="competence-icon-wrap">⚙️</div>
                            <div class="competence-title">엔진 프로토타이핑</div>
                            <div class="competence-desc">Unity C# 기반 자체 메카닉 구현, 개발팀과의 오차 없는 기획 파이프라인 조율 및 기술적 커뮤니케이션.</div>
                        </div>
                        <div class="competence-card">
                            <div class="competence-icon-wrap">🎬</div>
                            <div class="competence-title">영화적 연출 & 서사 구조</div>
                            <div class="competence-desc">동국대 영화영상학과 기반의 스토리텔링 문법과 퀘스트 플로우를 결합한 깊이 있는 세계관 구축.</div>
                        </div>
                    </div>

                    <div class="main-cta-group">
                        <button class="btn-primary" onclick="switchPage('resume', document.getElementById('nav-btn-resume'))">
                            <span>👤 이력 쇼케이스 보기</span>
                        </button>
                        <button class="btn-ghost" onclick="switchPage('coverletter', document.getElementById('nav-btn-coverletter'))" style="background:rgba(146,129,247,0.18); border-color:var(--color-iris-violet);">
                            <span>📋 자기소개서 보기</span>
                        </button>
                        <button class="btn-ghost" onclick="switchPage('portfolio', document.getElementById('nav-btn-portfolio'))">
                            <span>📂 기획서 & 포트폴리오</span>
                        </button>
                        <button class="btn-ghost" onclick="switchPage('playhistory', document.getElementById('nav-btn-playhistory'))">
                            <span>📊 플레이 히스토리</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- 스텝 인디케이터 (1, 2) -->
            <div class="main-step-indicators">
                <div class="main-step-dot active" id="dotStep1" onclick="setMainStep(1)"></div>
                <div class="main-step-dot" id="dotStep2" onclick="setMainStep(2)"></div>
            </div>
        </div>
    </section>

    <!-- -------------------------------------------------------------
         2. 이력 소개 페이지: 메인처럼 화면을 시원하게 채우는 5단계 풀 캔버스 쇼케이스
            01~05 순서 표기, 클릭 시 다음 단계, 5단계에서 클릭 시 다시 1단계로 순환!
    ------------------------------------------------------------- -->
    <section id="page-resume" class="page-section" onclick="handleResumeCanvasClick(event)">
        <!-- 상단 단계 번호 인디케이터 -->
        <div class="showcase-nav-bar" onclick="event.stopPropagation()">
            <span class="showcase-step-num active" id="resumeNav1" onclick="goToResumeStage(1)">01 인적사항</span>
            <span style="color:#333;">|</span>
            <span class="showcase-step-num" id="resumeNav2" onclick="goToResumeStage(2)">02 보유 스킬</span>
            <span style="color:#333;">|</span>
            <span class="showcase-step-num" id="resumeNav3" onclick="goToResumeStage(3)">03 회사 & 프로젝트</span>
            <span style="color:#333;">|</span>
            <span class="showcase-step-num" id="resumeNav4" onclick="goToResumeStage(4)">04 참여 영화</span>
            <span style="color:#333;">|</span>
            <span class="showcase-step-num" id="resumeNav5" onclick="goToResumeStage(5)">05 학력 & 역량</span>
        </div>

        <!-- 하단 화면 클릭 안내 -->
        <div class="showcase-hint">화면을 클릭하면 다음 쇼케이스로 이동합니다 (5단계 완료 시 1단계로 순환)</div>

        <!-- [STAGE 1] 밝은 main2 배경 + 투명배경 인물 누끼(좌측) + 인적사항(우측) -->
        <div class="showcase-stage active" id="resumeStage1">
            <div class="stage-1-bg"></div>
            <div class="stage-1-wrap">
                <img src="profile_cutout.png" alt="정승운 프로필" class="profile-cutout-img">
                <div class="profile-info-card">
                    <div class="profile-tag">CREATOR & SYSTEM DESIGNER</div>
                    <h2 class="profile-name">정승운</h2>
                    <p class="profile-title-sub">시스템 & 밸런싱 기획자 | 내러티브 디렉터</p>
                    
                    <div class="profile-details-grid">
                        <div class="profile-detail-item">
                            <label>생년월일</label>
                            <span>1997. 01. 19 (만 29세)</span>
                        </div>
                        <div class="profile-detail-item">
                            <label>연락처</label>
                            <span>010-3882-9699</span>
                        </div>
                        <div class="profile-detail-item">
                            <label>이메일</label>
                            <span>wddy9699@naver.com</span>
                        </div>
                        <div class="profile-detail-item">
                            <label>희망 직무</label>
                            <span>게임 기획 (시스템 / 레벨 / 밸런싱)</span>
                        </div>
                        <div class="profile-detail-item" style="grid-column: span 2;">
                            <label>학력 사항</label>
                            <span>동국대학교 예술대학 영화영상학과 학사 졸업 (4.04 / 4.5)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- [STAGE 2] 유니티(가시성 극대화 화이트 입체 글로우), 프리미어, 포토샵, 엑셀, PPT, 워드 아이콘 중앙 정렬 및 설명 -->
        <div class="showcase-stage" id="resumeStage2">
            <div class="stage-2-wrap">
                <div class="profile-tag">TOOL & SOFTWARE MASTERY</div>
                <h2 style="font-size:36px; font-weight:800; margin-bottom:8px;">실무 소프트웨어 및 엔진 활용 역량</h2>
                <p style="color:var(--color-ash-gray); font-size:15px;">엔진 프로토타이핑부터 그래픽 리소스 가공, 정량적 수치 연산 및 문서화까지 완벽 지원</p>

                <div class="tools-icon-row">
                    <div class="tool-icon-box" title="Unity Engine" style="border-color:rgba(146,129,247,0.4); box-shadow:0 0 20px rgba(146,129,247,0.25);">
                        <img src="icon_unity.svg" alt="Unity">
                        <span class="tool-name" style="color:#fff; font-weight:700;">Unity</span>
                    </div>
                    <div class="tool-icon-box" title="Premiere Pro">
                        <img src="icon_premiere.svg" alt="Premiere">
                        <span class="tool-name">Premiere</span>
                    </div>
                    <div class="tool-icon-box" title="Photoshop">
                        <img src="icon_photoshop.svg" alt="Photoshop">
                        <span class="tool-name">Photoshop</span>
                    </div>
                    <div class="tool-icon-box" title="Microsoft Excel">
                        <img src="icon_excel.svg" alt="Excel">
                        <span class="tool-name">Excel</span>
                    </div>
                    <div class="tool-icon-box" title="PowerPoint">
                        <img src="icon_powerpoint.svg" alt="PPT">
                        <span class="tool-name">PowerPoint</span>
                    </div>
                    <div class="tool-icon-box" title="Microsoft Word">
                        <img src="icon_word.svg" alt="Word">
                        <span class="tool-name">Word</span>
                    </div>
                </div>

                <div class="tools-desc-grid">
                    <div class="tool-desc-card">
                        <h4>🎮 게임 엔진 및 개발</h4>
                        <p><strong>Unity (C#)</strong>: 프리팹 구조 설계, FSM 상태 머신 구축, 프로토타입 구현 및 물리/UI 이벤트 완벽 제어 가능.</p>
                    </div>
                    <div class="tool-desc-card">
                        <h4>📊 데이터 및 밸런싱 수치화</h4>
                        <p><strong>Excel & Docs</strong>: 다변수 수식 연산, 테이블 구조화, 시뮬레이션 경제 순환 설계 및 기획서 표준 템플릿 마스터.</p>
                    </div>
                    <div class="tool-desc-card">
                        <h4>🎨 시각화 및 영상 연출</h4>
                        <p><strong>Premiere & Photoshop</strong>: 컷씬 스토리보드, UI/UX 와이어프레임 목업, 게임 트레일러 편집 및 시각적 리소스 가공.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- [STAGE 3] 프로젝트 대표 이미지 + 데블다이스 / 제임스텍 로고 및 설명 -->
        <div class="showcase-stage" id="resumeStage3">
            <div class="stage-3-wrap">
                <div class="profile-tag">CAREER & MAJOR PROJECTS</div>
                <h2 style="font-size:36px; font-weight:800; margin-bottom:8px; text-align:center;">주요 경력 및 핵심 프로젝트</h2>
                <p style="color:var(--color-ash-gray); font-size:15px; text-align:center;">상용화 프로젝트 및 프로토타입 개발을 총괄 기획한 실무 경험</p>

                <div class="project-cards-dual">
                    <!-- 데블다이스 / LAST SANCTUARY -->
                    <div class="project-show-card">
                        <img src="lastsanctuary.png" alt="LAST SANCTUARY" class="project-show-img">
                        <div class="project-show-body">
                            <div class="project-company-badge">
                                <img src="logo_devildice.png" alt="데블다이스 로고">
                                <span style="font-size:12px; color:var(--color-ash-gray); font-family:var(--font-mono);">데블다이스 (2023 - 2024)</span>
                            </div>
                            <div class="project-show-title">LAST SANCTUARY (라스트 생츄어리)</div>
                            <div class="project-show-desc">
                                포스트 아포칼립스 세계관 기반의 <strong>생존 기지 건설 & 디펜스 시뮬레이션</strong>.<br>
                                • 자원 채집/정제/소모 3단계 순환 경제 및 타일 기반 기지 건설 메카닉 설계.<br>
                                • 몬스터 웨이브 주기 및 방어 타워 사거리/DPS 정밀 밸런싱 시트 구축.
                            </div>
                        </div>
                    </div>

                    <!-- 제임스텍 / 슬기로운 재배생활 -->
                    <div class="project-show-card">
                        <img src="슬기로운재배생활.png" alt="슬기로운 재배생활" class="project-show-img">
                        <div class="project-show-body">
                            <div class="project-company-badge">
                                <img src="logo_jamestech.png" alt="제임스텍 로고">
                                <span style="font-size:12px; color:var(--color-ash-gray); font-family:var(--font-mono);">제임스텍 (2024)</span>
                            </div>
                            <div class="project-show-title">슬기로운 재배생활 (Smart Farm Tycoon)</div>
                            <div class="project-show-desc">
                                스마트팜 농작물 재배 및 유통 시장 연계형 <strong>타이쿤 & 경영 시뮬레이션</strong>.<br>
                                • 작물 성장 곡선, 온/습도 환경 계수 연산 및 장비 업그레이드 트리 기획.<br>
                                • 게임 내 시장 시세 변동 알고리즘 설계 및 유저 보상 체계 정립.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- [STAGE 4] 참여 영화 목록(좌측) + 왼쪽을 비추는 35mm 영화 카메라 애니메이션(우측) -->
        <div class="showcase-stage" id="resumeStage4">
            <div class="stage-4-wrap">
                <div class="film-list-col">
                    <div class="profile-tag">CINEMATIC FILMOGRAPHY</div>
                    <h2 style="font-size:34px; font-weight:800; margin-bottom:8px;">영화 영상 연출 및 제작 참여작</h2>
                    <p style="color:var(--color-ash-gray); font-size:14px; line-height:1.6;">
                        카메라와 편집실에서 체득한 시각적 연출 감각과 내러티브 템포 조절력은<br>
                        게임 내 컷씬 연출과 퀘스트 몰입도를 극대화하는 강력한 자산입니다.
                    </p>

                    <div class="film-items-container">
                        <div class="film-badge-item">
                            <span class="film-badge-role">연출/각본</span>
                            <span class="film-badge-title">단편 영화 《잔향(Echo)》</span>
                        </div>
                        <div class="film-badge-item">
                            <span class="film-badge-role">조감독</span>
                            <span class="film-badge-title">단편 영화 《경계선》</span>
                        </div>
                        <div class="film-badge-item">
                            <span class="film-badge-role">촬영감독</span>
                            <span class="film-badge-title">단편 영화 《붉은 밤》</span>
                        </div>
                        <div class="film-badge-item">
                            <span class="film-badge-role">편집감독</span>
                            <span class="film-badge-title">중편 영화 《시선 너머》</span>
                        </div>
                        <div class="film-badge-item">
                            <span class="film-badge-role">각본</span>
                            <span class="film-badge-title">단편 시나리오 《네 번째 벽》</span>
                        </div>
                        <div class="film-badge-item">
                            <span class="film-badge-role">제작총괄</span>
                            <span class="film-badge-title">졸업작품 《빛과 그림자》</span>
                        </div>
                        <div class="film-badge-item">
                            <span class="film-badge-role">미술감독</span>
                            <span class="film-badge-title">단편 영화 《폐허의 꽃》</span>
                        </div>
                        <div class="film-badge-item">
                            <span class="film-badge-role">사운드 디자인</span>
                            <span class="film-badge-title">실험 영화 《진동수》</span>
                        </div>
                        <div class="film-badge-item" style="grid-column: span 2; background:rgba(146,129,247,0.1); border-color:var(--color-iris-violet);">
                            <span class="film-badge-role" style="background:var(--color-iris-violet); color:#000;">영화제 출품</span>
                            <span class="film-badge-title">국내 유수 대학영화제 초청 상영 및 최우수 기술상 수상작 포함</span>
                        </div>
                    </div>
                </div>

                <!-- 우측: 왼쪽 영화 목록을 비추도록 방향을 바꾼 빈티지 영화 카메라 -->
                <div class="film-camera-col">
                    <div class="film-projector-beam"></div>
                    <svg class="vintage-camera-svg" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg">
                        <!-- 카메라 본체 (오른쪽에 위치, 렌즈는 왼쪽을 향함) -->
                        <rect x="140" y="110" width="130" height="100" rx="14" fill="#181a24" stroke="#4d5368" stroke-width="2.5" />
                        
                        <!-- 상단 회전 필름 릴 2개 -->
                        <g>
                            <circle cx="165" cy="75" r="32" fill="#11131a" stroke="#9281f7" stroke-width="2.5" />
                            <circle cx="165" cy="75" r="8" fill="#fff" />
                            <line x1="165" y1="47" x2="165" y2="103" stroke="#484f66" stroke-width="2">
                                <animateTransform attributeName="transform" type="rotate" from="0 165 75" to="360 165 75" dur="4s" repeatCount="indefinite"/>
                            </line>
                            <line x1="137" y1="75" x2="193" y2="75" stroke="#484f66" stroke-width="2">
                                <animateTransform attributeName="transform" type="rotate" from="0 165 75" to="360 165 75" dur="4s" repeatCount="indefinite"/>
                            </line>
                        </g>
                        <g>
                            <circle cx="235" cy="75" r="32" fill="#11131a" stroke="#9281f7" stroke-width="2.5" />
                            <circle cx="235" cy="75" r="8" fill="#fff" />
                            <line x1="235" y1="47" x2="235" y2="103" stroke="#484f66" stroke-width="2">
                                <animateTransform attributeName="transform" type="rotate" from="0 235 75" to="360 235 75" dur="4s" repeatCount="indefinite"/>
                            </line>
                            <line x1="207" y1="75" x2="263" y2="75" stroke="#484f66" stroke-width="2">
                                <animateTransform attributeName="transform" type="rotate" from="0 235 75" to="360 235 75" dur="4s" repeatCount="indefinite"/>
                            </line>
                        </g>

                        <!-- 왼쪽을 향한 카메라 렌즈 경통 & 조리개 (빛 방출) -->
                        <polygon points="140,135 90,120 90,200 140,185" fill="#242838" stroke="#9281f7" stroke-width="2" />
                        <ellipse cx="90" cy="160" rx="10" ry="40" fill="#9281f7" opacity="0.8">
                            <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" />
                        </ellipse>
                        <circle cx="90" cy="160" r="14" fill="#ffffff" opacity="0.9" />

                        <!-- 카메라 삼각대 마운트 -->
                        <polygon points="190,210 220,210 270,300 250,300 205,230 160,300 140,300" fill="#2a2e3f" />
                        <line x1="205" y1="210" x2="205" y2="300" stroke="#373c4e" stroke-width="4" />
                    </svg>
                </div>
            </div>
        </div>

        <!-- [STAGE 5] 동국대학교 학력 & 융합 기획 역량 (여기서 한번 더 클릭하면 다시 STAGE 1로 순환!) -->
        <div class="showcase-stage" id="resumeStage5">
            <div class="stage-5-wrap">
                <div class="profile-tag">ACADEMIC FOUNDATION & SYNERGY</div>
                <h2 style="font-size:36px; font-weight:800; margin-bottom:8px;">동국대학교 영화영상학과 학사 졸업</h2>
                <p style="color:var(--color-ash-gray); font-size:15px;">전공 평점 4.04 / 4.50 — 예술적 통찰과 공학적 시스템 사고의 유기적 결합</p>

                <div class="dongguk-box">
                    <img src="logo_dongguk.png" alt="동국대학교 로고" class="dongguk-logo-img">
                    <h3 style="font-size:24px; font-weight:700; color:#fff; margin-bottom:12px;">탄탄한 연출 이론과 게임 시스템의 결합</h3>
                    <p style="font-size:15px; color:var(--color-ash-gray); line-height:1.8; max-width:750px; margin:0 auto;">
                        영화영상학에서 습득한 <strong>시나리오 3막 구조, 미장센 공간 연출, 관객 심리 유도 기법</strong>을<br>
                        게임 시스템의 <strong>플레이어 행동 유도(Affordance), 인터랙션 피드백 루프, 몰입형 퀘스트 라인</strong>으로 치환하여<br>
                        단순한 텍스트 전달을 넘어 플레이어가 직접 체험하는 살아있는 게임 세계를 창조합니다.
                    </p>

                    <div class="academic-grid">
                        <div class="academic-card">
                            <div style="font-size:22px; margin-bottom:8px;">📚</div>
                            <h4 style="color:#fff; font-size:15px; margin-bottom:6px;">서사 설계 역량</h4>
                            <p style="color:var(--color-ash-gray); font-size:13px;">복합적인 인물 관계도와 갈등 요소를 게임 메카닉과 직결시키는 퀘스트 디자인.</p>
                        </div>
                        <div class="academic-card">
                            <div style="font-size:22px; margin-bottom:8px;">🎬</div>
                            <h4 style="color:#fff; font-size:15px; margin-bottom:6px;">연출 및 카메라 워크</h4>
                            <p style="color:var(--color-ash-gray); font-size:13px;">인게임 컷씬의 프레임 구도, 조명 연출 및 사운드 믹싱을 통한 감정의 최고조 유도.</p>
                        </div>
                        <div class="academic-card">
                            <div style="font-size:22px; margin-bottom:8px;">🤝</div>
                            <h4 style="color:#fff; font-size:15px; margin-bottom:6px;">대규모 협업 커뮤니케이션</h4>
                            <p style="color:var(--color-ash-gray); font-size:13px;">영화 현장 수십 명의 스태프를 지휘했던 프로덕션 리더십으로 개발팀과의 원활한 소통 보장.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- -------------------------------------------------------------
         3. 자기소개서 페이지 (단독 분리, 사용자의 원문 4개 섹션 100% 온전 수록)
    ------------------------------------------------------------- -->
    <section id="page-coverletter" class="page-section">
        <div class="section-header-box">
            <div class="profile-tag">STATEMENT OF PURPOSE & ESSAYS</div>
            <h1 class="section-title">자기소개서</h1>
            <p class="section-desc">탄탄한 논리와 데이터로 상상하는 게임 기획자 정승운의 진솔한 철학과 직무 역량입니다.</p>
        </div>

        <div class="coverletter-grid">
            <!-- 항목 1: 지원동기 -->
            <div class="essay-card">
                <div class="essay-num">SECTION 01</div>
                <h3 class="essay-title">[지원 동기] 논리적인 시스템으로 유저에게 잊지 못할 몰입의 순간을 선물하기 위해</h3>
                <div class="essay-body">어릴 적부터 게임은 단순한 오락이 아닌 하나의 완결된 세계이자 가장 강렬한 상호작용의 예술이었습니다. 특히 시뮬레이션과 전략 장르를 깊이 파고들며, 규칙과 수치라는 정교한 뼈대 위에서 플레이어가 스스로 이야기를 완성해 나가는 과정에 깊은 매료를 느꼈습니다.

영화영상학과에서 공부하며 관객의 감정을 움직이는 서사 구조와 시각적 연출의 문법을 배웠고, 이후 게임 개발에 뛰어들며 이를 유저가 직접 조작하고 상호작용하는 시스템적 메카닉으로 구현하는 일에 열정을 쏟아왔습니다. 탄탄한 기획 논리와 세밀한 밸런싱으로 유저가 시스템의 매력에 빠져 시간 가는 줄 모르게 만드는 완성도 높은 게임을 개발하고자 지원하게 되었습니다.</div>
            </div>

            <!-- 항목 2: 직무 역량 -->
            <div class="essay-card">
                <div class="essay-num">SECTION 02</div>
                <h3 class="essay-title">[직무 역량 및 전문성] 엔진 구현력과 정량적 데이터 분석을 아우르는 올라운드 기획 역량</h3>
                <div class="essay-body">첫째, 실현 가능한 기획을 설계하는 Unity 엔진 및 프로토타이핑 역량입니다. 아이디어를 문서에만 가두지 않고 Unity(C#)를 통해 코어 메카닉을 신속하게 구현하여 플레이어블 빌드로 검증합니다. 이를 통해 개발팀과 기획의 기술적 타당성을 오차 없이 논의하고 불필요한 개발 비용을 획기적으로 줄입니다.

둘째, 정밀한 엑셀 수식 및 다변수 데이터 밸런싱 역량입니다. 자원 산출량, 소모 주기, 장비 및 유닛 스탯의 상관관계를 통계적이고 정량적인 수식으로 구조화합니다. 데블다이스와 제임스텍 프로젝트에서 인플레이션을 방지하고 안정적인 경제 순환 사이클을 구축하며 실무 검증을 마쳤습니다.

셋째, 영화영상학 전공에서 비롯된 내러티브 연출 및 세계관 구축 역량입니다. 게임의 시스템 규칙과 세계관 설정이 따로 놀지 않고 유기적으로 맞물리도록 퀘스트 라인과 UI/UX 플로우를 기획하여 유저가 시스템을 배우는 과정 자체가 매력적인 스토리텔링이 되도록 설계합니다.</div>
            </div>

            <!-- 항목 3: 문제 해결 경험 -->
            <div class="essay-card">
                <div class="essay-num">SECTION 03</div>
                <h3 class="essay-title">[문제 해결 및 협업 경험] 데이터 역추적과 유저 관점의 전환으로 이끌어낸 밸런스 정상화</h3>
                <div class="essay-body">라스트 생츄어리(LAST SANCTUARY) 프로젝트 기획 당시, 테스트 플레이어들 사이에서 특정 방어 타워와 자원 테크트리만을 편중하여 사용하는 '최적해 고착화' 문제가 발생했습니다. 다른 전략적 선택지가 사장되면서 중반부 난이도 곡선이 급격히 무너지는 상황이었습니다.

문제를 해결하기 위해 먼저 모든 웨이브별 타워 딜량과 자원 소비 데이터를 엑셀로 역추적 모델링했습니다. 분석 결과, 특정 타워의 업그레이드 비용 대비 방어 효율(Cost-Effectiveness)이 다른 타워보다 비정상적으로 높았던 구조적 원인을 발견했습니다. 단순히 스탯을 깎는 일차원적 너프 대신, 몬스터의 장갑 속성과 지형 상성 요소를 새롭게 도입하고 타워 간의 연계 시너지 보너스를 설계했습니다.

결과적으로 플레이어들이 한 가지 전략에 안주하지 않고 상황에 맞춰 다양한 타워를 조합하도록 유도하여 중후반부 플레이 타임을 40% 이상 연장시키고 다양한 전략적 재미를 회복시켰습니다.</div>
            </div>

            <!-- 항목 4: 입사 후 포부 -->
            <div class="essay-card">
                <div class="essay-num">SECTION 04</div>
                <h3 class="essay-title">[목표와 포부] 라이브 서비스의 안정성을 지키고 글로벌 유저를 사로잡는 차세대 시스템 구축</h3>
                <div class="essay-body">입사 후, 기존 프로젝트의 코드베이스와 기획 테이블 구조를 신속하게 파악하여 팀 내에서 가장 신뢰받는 기획자가 되겠습니다. 데이터에 기반한 꼼꼼한 밸런싱과 빈틈없는 예외 처리 설계로 라이브 서비스에서 발생할 수 있는 경제 붕괴나 시스템 악용을 사전에 완벽히 차단하겠습니다.

중장기적으로는 글로벌 시장에서 수년 동안 생명력을 유지하며 회자되는 시뮬레이션/전략 타이틀의 코어 메카닉을 주도하는 리드 기획자로 성장하겠습니다. 유저가 플레이하며 감탄할 수밖에 없는 깊이 있는 룰과 유기적인 상호작용을 완성하여, 회사의 핵심 IP 가치를 드높이는 데 기여하겠습니다.</div>
            </div>
        </div>
    </section>

    <!-- -------------------------------------------------------------
         4. 포트폴리오 페이지: 기획서 및 데이터 문서함
    ------------------------------------------------------------- -->
    <section id="page-portfolio" class="page-section">
        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:32px; flex-wrap:wrap; gap:16px;">
            <div>
                <div class="profile-tag">DOCUMENT ARCHIVE & SPECS</div>
                <h1 class="section-title" style="margin-bottom:6px;">포트폴리오 문서함</h1>
                <p class="section-desc" style="margin-bottom:0;">실무 및 프로젝트에서 직접 작성한 게임 기획서, 밸런싱 수치 테이블 및 개발 문서 20건입니다.</p>
            </div>
            <div style="font-family:var(--font-mono); font-size:13px; color:var(--color-iris-violet); background:rgba(146,129,247,0.12); padding:6px 14px; border-radius:20px; border:1px solid rgba(146,129,247,0.25);">
                📁 총 20건 문서 등록 완료
            </div>
        </div>

        <div class="docs-category-grid" id="docsContainer">
            <!-- JS 동적 로딩 -->
        </div>
    </section>

    <!-- -------------------------------------------------------------
         5. 플레이 히스토리 페이지: 삼각 파라미터 비율 100% 일치 복구
            전략&시뮬레이션 45% / 경영&샌드박스 30% / RPG&내러티브 25% (합 100%)
    ------------------------------------------------------------- -->
    <section id="page-playhistory" class="page-section">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; flex-wrap:wrap; gap:16px;">
            <div>
                <div class="profile-tag">GAMEPLAY DATA & ANALYSIS</div>
                <h1 class="section-title" style="margin-bottom:6px;">플레이 히스토리</h1>
                <p class="section-desc" style="margin-bottom:0;">게임 기획적 인사이트를 얻은 주요 플레이 게임과 코어 시스템 분석입니다.</p>
            </div>
            <button class="btn-ghost" onclick="openGameSearchModal()" style="padding:10px 18px; border-color:var(--color-iris-violet); background:rgba(146,129,247,0.18); font-weight:600;">
                <span>🔍 IGDB 게임 실시간 검색 및 추가</span>
            </button>
        </div>

        <!-- 삼각 파라미터 레이더 다이어그램 (수학적 좌표 및 눈금 100% 정합) -->
        <div class="radar-triangle-container">
            <div class="radar-svg-col">
                <svg viewBox="0 0 360 320" width="340" height="300" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#9281f7" stop-opacity="0.65"/>
                            <stop offset="100%" stop-color="#6452f0" stop-opacity="0.25"/>
                        </linearGradient>
                        <filter id="radarGlow" x="-20%" y="-20%" width="140%" height="140%">
                            <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#9281f7" flood-opacity="0.75"/>
                        </filter>
                    </defs>

                    <!-- 수학적 정삼각형 가이드라인 (중심: 180, 160 / 최대 반경 R = 100) -->
                    <!-- 100% 가이드: Top(180, 60), BR(266.6, 210), BL(93.4, 210) -->
                    <polygon points="180,60 266.6,210 93.4,210" fill="none" stroke="#373c4e" stroke-width="1.5" />
                    <!-- 75% 가이드: Top(180, 85), BR(245, 197.5), BL(115, 197.5) -->
                    <polygon points="180,85 245,197.5 115,197.5" fill="none" stroke="#252937" stroke-width="1" />
                    <!-- 50% 가이드: Top(180, 110), BR(223.3, 185), BL(136.7, 185) -->
                    <polygon points="180,110 223.3,185 136.7,185" fill="none" stroke="#252937" stroke-width="1" stroke-dasharray="2,2" />
                    <!-- 25% 가이드: Top(180, 135), BR(201.7, 172.5), BL(158.3, 172.5) -->
                    <polygon points="180,135 201.7,172.5 158.3,172.5" fill="none" stroke="#252937" stroke-width="1" stroke-dasharray="2,2" />

                    <!-- 중심 축선 (Center to Vertices) -->
                    <line x1="180" y1="160" x2="180" y2="60" stroke="#484f66" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <line x1="180" y1="160" x2="266.6" y2="210" stroke="#484f66" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <line x1="180" y1="160" x2="93.4" y2="210" stroke="#484f66" stroke-width="1.5" stroke-dasharray="3,3"/>

                    <!-- 정밀 눈금 라벨 (25%, 50%, 75%, 100%) -->
                    <text x="184" y="65" fill="#9281f7" font-size="9" font-family="Commit Mono">100%</text>
                    <text x="184" y="90" fill="#71768a" font-size="8.5" font-family="Commit Mono">75%</text>
                    <text x="184" y="114" fill="#71768a" font-size="8.5" font-family="Commit Mono">50%</text>
                    <text x="184" y="138" fill="#585c6c" font-size="8.5" font-family="Commit Mono">25%</text>

                    <!-- [수학적 정확 비율 적용 데이터 폴리곤] -->
                    <!-- 1. 전략 & 시뮬레이션 45%: y = 160 - (100 * 0.45) = 115 -> (180, 115) (50% 라인 바로 아래) -->
                    <!-- 2. 경영 & 샌드박스 30%: x = 180 + (100 * 0.30 * 0.866) = 206, y = 160 + (100 * 0.30 * 0.5) = 175 -> (206, 175) (25% 라인 바로 바깥) -->
                    <!-- 3. RPG & 내러티브 25%: x = 180 - (100 * 0.25 * 0.866) = 158.3, y = 160 + (100 * 0.25 * 0.5) = 172.5 -> (158.3, 172.5) (25% 라인 정확히 일치) -->
                    <polygon points="180,115 206,175 158.3,172.5" fill="url(#polyGrad)" stroke="#9281f7" stroke-width="2.5" filter="url(#radarGlow)" />

                    <!-- 꼭짓점 데이터 마커 -->
                    <circle cx="180" cy="115" r="5" fill="#fff" stroke="#9281f7" stroke-width="2.5"/>
                    <circle cx="206" cy="175" r="5" fill="#fff" stroke="#9281f7" stroke-width="2.5"/>
                    <circle cx="158.3" cy="172.5" r="5" fill="#fff" stroke="#9281f7" stroke-width="2.5"/>

                    <!-- 장르 라벨 -->
                    <text x="180" y="38" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle" font-family="Pretendard">전략 & 시뮬레이션 (45%)</text>
                    <text x="282" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">경영 & 샌드박스 (30%)</text>
                    <text x="78" y="235" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle" font-family="Pretendard">RPG & 내러티브 (25%)</text>
                </svg>
            </div>

            <!-- 우측: 3대 장르 비율 카드 (합계 100% 일치) -->
            <div class="radar-desc-col">
                <div class="radar-axis-card">
                    <div class="radar-axis-title">
                        <span>전략 & 시뮬레이션 (Strategy & Simulation)</span>
                        <span style="color:var(--color-iris-violet); font-family:var(--font-mono);">45%</span>
                    </div>
                    <div class="radar-axis-txt">
                        타일 기반 자원 수식, 테크 트리 연계성, AI 의사결정 알고리즘 및 턴제/실시간 시스템 밸런싱 집중 분석 (문명 시리즈, RTS).
                    </div>
                </div>

                <div class="radar-axis-card">
                    <div class="radar-axis-title">
                        <span>경영 & 샌드박스 (Management & Sandbox)</span>
                        <span style="color:var(--color-iris-violet); font-family:var(--font-mono);">30%</span>
                    </div>
                    <div class="radar-axis-txt">
                        다변수 수치 시뮬레이션, 구단 재정 및 이적 시장 순환 경제, 상태 머신(FSM) 기반 NPC 인터랙션 벤치마킹 (FM 시리즈, 림월드).
                    </div>
                </div>

                <div class="radar-axis-card">
                    <div class="radar-axis-title">
                        <span>RPG & 내러티브 (Role Playing & Narrative)</span>
                        <span style="color:var(--color-iris-violet); font-family:var(--font-mono);">25%</span>
                    </div>
                    <div class="radar-axis-txt">
                        선택지에 따른 분기 구조, 스토리텔링 템포 조절, 퀘스트 플로우 및 시스템적 내러티브 연출 연구 (발더스 게이트, 위쳐).
                    </div>
                </div>

                <div style="font-family:var(--font-mono); font-size:12px; color:var(--color-ash-gray); text-align:right; padding-right:4px;">
                    총 플레이 누적 시간: <strong style="color:#fff;">2,500h+</strong> (장르 합계: 100%)
                </div>
            </div>
        </div>

        <!-- 게임 리스트 그리드 -->
        <div class="play-grid" id="playGrid">
            <div class="play-card">
                <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co49x5.jpg" alt="Civilization VI" class="play-cover-img" onerror="this.src='lastsanctuary.png'">
                <div class="play-card-body">
                    <div class="play-card-title">Sid Meier's Civilization VI</div>
                    <div class="play-card-meta">턴제 전략 / 1,200h+ 분석</div>
                    <div class="play-card-desc">타일 산출량 수식 구조, 불가사의 트리 설계 및 시대별 승리 조건 밸런싱 연구.</div>
                </div>
            </div>
            <div class="play-card">
                <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co73d7.jpg" alt="Football Manager 2024" class="play-cover-img" onerror="this.src='lastsanctuary.png'">
                <div class="play-card-body">
                    <div class="play-card-title">Football Manager 2024</div>
                    <div class="play-card-meta">스포츠 시뮬 / 950h+ 분석</div>
                    <div class="play-card-desc">다변수 수치 시뮬레이션 연산 구조와 AI 이적 시장 경제 순환 사이클 벤치마킹.</div>
                </div>
            </div>
            <div class="play-card">
                <img src="https://images.igdb.com/igdb/image/upload/t_cover_big/co2k34.jpg" alt="RimWorld" class="play-cover-img" onerror="this.src='lastsanctuary.png'">
                <div class="play-card-body">
                    <div class="play-card-title">RimWorld (림월드)</div>
                    <div class="play-card-meta">SF 생존 시뮬 / 700h+ 분석</div>
                    <div class="play-card-desc">AI 스토리텔러 이벤트 확률 분포 모델링과 림 성격별 유한 상태 머신(FSM) 상호작용.</div>
                </div>
            </div>
        </div>
    </section>

    <!-- -------------------------------------------------------------
         IGDB 실시간 게임 검색 모달
    ------------------------------------------------------------- -->
    <div class="modal-overlay" id="igdbModal" onclick="closeGameSearchModal(event)">
        <div class="modal-box" onclick="event.stopPropagation()">
            <div class="modal-header">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:20px;">🎮</span>
                    <div>
                        <h3 style="font-size:17px; font-weight:700;">IGDB 공식 게임 데이터베이스 검색</h3>
                        <div style="font-size:12px; color:var(--color-ash-gray);">전 세계 모든 플랫폼의 게임을 실시간으로 검색하여 히스토리에 추가합니다.</div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:14px;">
                    <div class="server-live-badge">
                        <span class="server-live-dot"></span>
                        <span>IGDB LIVE (정상)</span>
                    </div>
                    <button onclick="closeGameSearchModal()" style="background:none; border:none; color:var(--color-ash-gray); font-size:22px; cursor:pointer;">✕</button>
                </div>
            </div>

            <div class="modal-search-bar">
                <div class="search-input-group">
                    <input type="text" id="gameSearchInput" class="modal-input" placeholder="게임명을 한글 또는 영문으로 입력하세요 (예: 문명, 림월드, 발더스게이트, 엘든링...)" oninput="handleSearchInput(this.value)" onkeydown="if(event.key==='Enter') triggerDirectSearch()">
                    <button class="btn-primary" onclick="triggerDirectSearch()" style="padding:10px 20px; white-space:nowrap;">검색</button>
                </div>

                <div class="quick-chips">
                    <span style="font-size:11.5px; color:var(--color-charcoal-muted); align-self:center;">추천 태그:</span>
                    <button class="chip-btn" onclick="quickTagSearch('문명')">#문명</button>
                    <button class="chip-btn" onclick="quickTagSearch('림월드')">#림월드</button>
                    <button class="chip-btn" onclick="quickTagSearch('Football Manager')">#FM2024</button>
                    <button class="chip-btn" onclick="quickTagSearch('발더스게이트')">#발더스게이트</button>
                    <button class="chip-btn" onclick="quickTagSearch('엘든링')">#엘든링</button>
                    <button class="chip-btn" onclick="quickTagSearch('스타크래프트')">#스타크래프트</button>
                    <button class="chip-btn" onclick="quickTagSearch('디아블로')">#디아블로</button>
                    <button class="chip-btn" onclick="quickTagSearch('사이버펑크')">#사이버펑크</button>
                </div>
            </div>

            <div class="modal-results-list" id="gameSearchResults">
                <!-- 결과 렌더링 -->
            </div>
        </div>
    </div>

    <!-- 토스트 알림창 -->
    <div class="toast-msg" id="toastMsg">알림 메시지</div>

    <!-- -------------------------------------------------------------
         JavaScript 로직
    ------------------------------------------------------------- -->
    <script>
        // API Base URL
        const API_BASE = window.location.origin.includes('http') ? window.location.origin : 'http://localhost:3000';

        // 1. 페이지 네비게이션 관리
        let mainTimer = null;
        let currentMainStep = 1;

        function switchPage(pageId, btnEl) {
            // 네비게이션 활성화 토글
            document.querySelectorAll('.nav-link').forEach(btn => btn.classList.remove('active'));
            if (btnEl) btnEl.classList.add('active');

            // 페이지 섹션 활성화 토글
            document.querySelectorAll('.page-section').forEach(sec => sec.classList.remove('active'));
            const target = document.getElementById('page-' + pageId);
            if (target) target.classList.add('active');

            // 메인 페이지 전환 제어
            if (pageId === 'main') {
                // 다른 곳에서 메인으로 올 때는 항상 1페이지로 리셋되고 10초 타이머 재가동
                setMainStep(1);
                startMainTimer();
            } else {
                // 메인이 아닐 때는 타이머 정지
                stopMainTimer();
            }

            // 이력 소개 페이지일 때 항상 1단계로 시작
            if (pageId === 'resume') {
                goToResumeStage(1);
            }

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // 메인 페이지 10초 후 2페이지 자동 전환 후 정지
        function startMainTimer() {
            stopMainTimer();
            mainTimer = setTimeout(() => {
                setMainStep(2);
                // 2페이지로 전환된 후에는 타이머를 돌리지 않고 정지 유지!
            }, 10000);
        }

        function stopMainTimer() {
            if (mainTimer) {
                clearTimeout(mainTimer);
                mainTimer = null;
            }
        }

        function setMainStep(step) {
            currentMainStep = step;
            const step1 = document.getElementById('mainStep1');
            const step2 = document.getElementById('mainStep2');
            const dot1 = document.getElementById('dotStep1');
            const dot2 = document.getElementById('dotStep2');

            if (step === 1) {
                step1.classList.add('active');
                step2.classList.remove('active');
                dot1.classList.add('active');
                dot2.classList.remove('active');
            } else {
                step1.classList.remove('active');
                step2.classList.add('active');
                dot1.classList.remove('active');
                dot2.classList.add('active');
                stopMainTimer(); // 2페이지 도달 시 타이머 영구 정지
            }
        }

        // 초기 구동 시 메인 10초 타이머 시작
        startMainTimer();

        // 2. 이력 소개 5단계 풀 캔버스 쇼케이스 (클릭 시 다음 단계, 5단계에서 클릭 시 1단계로 순환)
        let currentResumeStage = 1;
        const totalResumeStages = 5;

        function goToResumeStage(stage) {
            currentResumeStage = stage;
            for (let i = 1; i <= totalResumeStages; i++) {
                const stageEl = document.getElementById('resumeStage' + i);
                const navEl = document.getElementById('resumeNav' + i);
                if (stageEl) {
                    if (i === stage) {
                        stageEl.classList.add('active');
                    } else {
                        stageEl.classList.remove('active');
                    }
                }
                if (navEl) {
                    if (i === stage) {
                        navEl.classList.add('active');
                    } else {
                        navEl.classList.remove('active');
                    }
                }
            }
        }

        function handleResumeCanvasClick(e) {
            // 상단 네비 바나 특정 링크 클릭 시 이벤트 버블링 방지
            if (e.target.closest('.showcase-nav-bar')) return;

            let nextStage = currentResumeStage + 1;
            if (nextStage > totalResumeStages) {
                nextStage = 1; // 5단계 완료 후 다시 1단계로 순환!
            }
            goToResumeStage(nextStage);
        }

        // 3. 포트폴리오 문서함 20건 로드
        async function loadPortfolioDocuments() {
            const container = document.getElementById('docsContainer');
            if (!container) return;

            try {
                const res = await fetch(`${API_BASE}/api/portfolio-documents`);
                if (!res.ok) throw new Error('문서 목록 로드 실패');
                const docs = await res.json();

                if (!docs || docs.length === 0) {
                    container.innerHTML = '<div style="color:var(--color-ash-gray); padding:30px; text-align:center;">등록된 포트폴리오 문서가 없습니다.</div>';
                    return;
                }

                container.innerHTML = '';
                docs.forEach((item, idx) => {
                    const card = document.createElement('div');
                    card.className = 'doc-item-card';

                    const downloadUrl = item.url || `${API_BASE}/api/download?file=${encodeURIComponent(item.name)}&folder=${item.folder || 'portfolio'}`;
                    const icon = item.name.endsWith('.pdf') ? '📄' : item.name.endsWith('.xlsx') || item.name.endsWith('.xls') ? '📊' : item.name.endsWith('.docx') ? '📝' : '📁';

                    card.innerHTML = `
                        <div>
                            <div style="font-size:28px; margin-bottom:12px;">${icon}</div>
                            <div style="font-size:12px; color:var(--color-iris-violet); font-family:var(--font-mono); margin-bottom:4px;">${item.category || '기획 문서'}</div>
                            <h4 style="font-size:15px; font-weight:700; color:#fff; margin-bottom:8px; line-height:1.4;">${item.title || item.name}</h4>
                            <p style="font-size:12.5px; color:var(--color-ash-gray); line-height:1.5;">${item.description || '시스템 설계 및 데이터 기획 문서 원본 파일'}</p>
                        </div>
                        <div style="margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:11.5px; color:var(--color-charcoal-muted);">${item.size || ''}</span>
                            <a href="${downloadUrl}" target="_blank" download class="btn-ghost" style="padding:6px 14px; font-size:12px; border-radius:6px; text-decoration:none;">열기 / 다운로드</a>
                        </div>
                    `;
                    container.appendChild(card);
                });
            } catch (err) {
                console.warn('포트폴리오 문서 로딩 오류:', err);
                container.innerHTML = '<div style="color:var(--color-ash-gray); padding:20px;">서버와의 연결을 확인 중입니다.</div>';
            }
        }

        // 4. IGDB 게임 검색 모달 제어
        let searchDebounce = null;

        function openGameSearchModal() {
            const modal = document.getElementById('igdbModal');
            modal.classList.add('active');
            // 모달 열릴 때 기본 추천 게임 20종 자동 로드!
            const input = document.getElementById('gameSearchInput');
            input.value = '';
            fetchAndRenderGames('');
            input.focus();
        }

        function closeGameSearchModal(e) {
            if (e && e.target !== e.currentTarget) return;
            document.getElementById('igdbModal').classList.remove('active');
        }

        function handleSearchInput(val) {
            clearTimeout(searchDebounce);
            searchDebounce = setTimeout(() => {
                fetchAndRenderGames(val);
            }, 300);
        }

        function quickTagSearch(keyword) {
            const input = document.getElementById('gameSearchInput');
            input.value = keyword;
            fetchAndRenderGames(keyword);
        }

        function triggerDirectSearch() {
            clearTimeout(searchDebounce);
            const val = document.getElementById('gameSearchInput').value;
            fetchAndRenderGames(val);
        }

        async function fetchAndRenderGames(query) {
            const container = document.getElementById('gameSearchResults');
            container.innerHTML = '<div style="color:var(--color-ash-gray); text-align:center; padding:36px;"><span style="font-size:24px;">⏳</span><br>IGDB 공식 데이터베이스에서 검색 중입니다...</div>';

            try {
                const url = query.trim() 
                    ? `${API_BASE}/api/search-games?q=${encodeURIComponent(query.trim())}`
                    : `${API_BASE}/api/search-games`;
                const res = await fetch(url);
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
                    row.style.cssText = 'display:flex; align-items:center; gap:14px; padding:12px 16px; border-bottom:1px solid var(--color-graphite-hairline); transition:background 0.2s;';
                    row.onmouseover = () => row.style.background = 'rgba(146,129,247,0.08)';
                    row.onmouseout = () => row.style.background = '';

                    const imgHtml = game.coverUrl 
                        ? `<img src="${game.coverUrl}" style="width:45px; height:60px; object-fit:cover; border-radius:6px; border:1px solid var(--color-graphite-hairline);" />`
                        : `<div style="width:45px; height:60px; background:#1a1c24; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:10px; color:#888;">NO IMG</div>`;

                    const releaseTxt = game.releaseYear ? ` (${game.releaseYear})` : '';

                    row.innerHTML = `
                        ${imgHtml}
                        <div style="flex:1; min-width:0;">
                            <div style="font-weight:700; color:#fff; font-size:14.5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                ${game.title}${releaseTxt}
                            </div>
                            <div style="font-size:12px; color:var(--color-ash-gray); margin-top:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                                플랫폼: ${game.platform} | 장르: ${game.genre}
                            </div>
                        </div>
                        <button class="btn-ghost" style="padding:6px 12px; font-size:12px; white-space:nowrap; border-color:var(--color-iris-violet); color:var(--color-iris-light);" onclick="addGameToHistory(${JSON.stringify(game).replace(/"/g, '&quot;')})">
                            히스토리 추가 +
                        </button>
                    `;
                    container.appendChild(row);
                });
            } catch (err) {
                console.error('IGDB 검색 에러:', err);
                container.innerHTML = `<div style="color:#ff6b6b; text-align:center; padding:30px;">
                    <div>⚠️ 검색 중 오류가 발생했습니다 (${err.message}).</div>
                    <div style="margin-top:10px;"><button class="btn-ghost" onclick="fetchAndRenderGames('')">인기 추천 목록 다시 불러오기</button></div>
                </div>`;
            }
        }

        // 히스토리에 게임 카드 추가
        function addGameToHistory(game) {
            const grid = document.getElementById('playGrid');
            if (!grid) return;

            const card = document.createElement('div');
            card.className = 'play-card';

            const coverSrc = game.coverUrl || 'lastsanctuary.png';

            card.innerHTML = `
                <img src="${coverSrc}" alt="${game.title}" class="play-cover-img" onerror="this.src='lastsanctuary.png'">
                <div class="play-card-body">
                    <div class="play-card-title">${game.title}</div>
                    <div class="play-card-meta">${game.genre} / 신규 등록</div>
                    <div class="play-card-desc">IGDB 연동을 통해 추가된 분석 대상 타이틀 (${game.platform}).</div>
                </div>
            `;

            grid.prepend(card);
            closeGameSearchModal();
            showToast(`[${game.title}] 히스토리에 성공적으로 추가되었습니다!`);
        }

        // 5. 토스트 알림
        function showToast(msg) {
            const toast = document.getElementById('toastMsg');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        // 6. 편집 모드 토글
        let isEditMode = false;
        function toggleEditMode() {
            isEditMode = !isEditMode;
            const btn = document.getElementById('editToggleBtn');
            btn.textContent = isEditMode ? '편집 모드 ON' : '편집 모드 OFF';
            btn.classList.toggle('active', isEditMode);
            showToast(isEditMode ? '편집 모드가 활성화되었습니다. 텍스트를 직접 수정할 수 있습니다.' : '편집 모드가 비활성화되었습니다.');
            
            document.querySelectorAll('[contenteditable]').forEach(el => {
                el.contentEditable = isEditMode ? 'true' : 'false';
            });
        }

        // 초기 데이터 로딩
        window.addEventListener('DOMContentLoaded', () => {
            loadPortfolioDocuments();
        });
    </script>
</body>
</html>'''

# Write index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Successfully generated index.html with UTF-8 encoding!")
