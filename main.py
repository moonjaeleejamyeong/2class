import streamlit as st
import streamlit.components.v1 as components

# 스트리밋 페이지 설정
st.set_page_config(page_title="폭탄 강화하기 - 폭발물의 진화", page_icon="💥", layout="centered")

# 스트리밋 제목
st.markdown("<h1 style='text-align: center;'>💥 폭탄 강화하기: 폭발물의 진화 💥</h1>", unsafe_allow_html=True)

# 게임 HTML/JS/CSS 코드
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bomb Upgrade Game</title>
    <style>
        body {
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            background-color: #1a1a1a;
            color: #ffffff;
            text-align: center;
            margin: 0;
            padding: 10px;
            overflow-x: hidden; /* 진동 애니메이션 시 스크롤 방지 */
        }
        .container {
            max-width: 480px;
            margin: 0 auto;
            background: #2a2a2a;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
            position: relative; /* 모달/파티클 기준점 */
        }
        .status {
            font-size: 16px;
            margin: 10px 0;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px;
            border-radius: 8px;
        }
        .status p { margin: 5px 0; }
        .money-text { color: #ffd700; font-weight: bold; }
        .shield-text { color: #2196F3; font-weight: bold; }
        .level-text { color: #ff4500; font-weight: bold; font-size: 1.2em; }
        .prob-text { color: #aaa; font-size: 0.9em; }

        .bomb-container {
            min-height: 150px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 15px 0;
            background: #151515;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 10px;
            position: relative;
        }
        .bomb-image {
            max-width: 120px;
            max-height: 120px;
            object-fit: contain;
            margin-bottom: 8px;
            transition: transform 0.1s ease-out; /* 기본 트랜지션 */
        }
        .bomb-name {
            font-size: 14px;
            font-weight: bold;
            color: #ccc;
        }

        /* --- 화려한 애니메이션 모션 --- */
        
        /* [전체화면 진동] 폭발 및 강화 시 */
        @keyframes screenShake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-1px, -2px) rotate(-1deg); }
            20% { transform: translate(-3px, 0px) rotate(1deg); }
            30% { transform: translate(3px, 2px) rotate(0deg); }
            40% { transform: translate(1px, -1px) rotate(1deg); }
            50% { transform: translate(-1px, 2px) rotate(-1deg); }
            60% { transform: translate(-3px, 1px) rotate(0deg); }
            70% { transform: translate(3px, 1px) rotate(-1deg); }
            80% { transform: translate(-1px, -1px) rotate(1deg); }
            90% { transform: translate(1px, 2px) rotate(0deg); }
            100% { transform: translate(1px, -2px) rotate(-1deg); }
        }
        .shake-screen {
            animation: screenShake 0.4s;
            animation-iteration-count: 1;
        }

        /* [성공 모션] 회전하며 확대/축소 및 발광 */
        @keyframes successPop {
            0% { transform: scale(0.5) rotate(-180deg); filter: drop-shadow(0 0 0px #4CAF50); opacity: 0; }
            60% { transform: scale(1.3) rotate(10deg); filter: drop-shadow(0 0 20px #00FF00); opacity: 1; }
            100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 5px #4CAF50); }
        }
        .anim-success {
            animation: successPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        /* [폭발 모션] 붉게 변하며 강렬한 진동 후 초기화 */
        @keyframes explodeRed {
            0% { transform: scale(1); filter: brightness(1); }
            20% { transform: scale(1.5) rotate(5deg); filter: brightness(2) drop-shadow(0 0 30px #ff0000); }
            40% { transform: scale(1.8) rotate(-5deg); }
            60% { transform: scale(0.2); filter: brightness(5) drop-shadow(0 0 50px #ff4500); opacity: 0; }
            100% { transform: scale(1); filter: brightness(1); opacity: 1; }
        }
        .anim-explode {
            animation: explodeRed 0.8s ease-out;
        }

        /* [방어 모션] 푸른 막이 생기며 충격 흡수 */
        @keyframes shieldAbsorb {
            0% { transform: scale(1); filter: drop-shadow(0 0 0px #2196F3); }
            30% { transform: scale(1.2); filter: drop-shadow(0 0 20px #00D2FF); }
            100% { transform: scale(1); filter: drop-shadow(0 0 5px #2196F3); }
        }
        .anim-shield {
            animation: shieldAbsorb 0.6s ease-out;
        }
        /* 푸른 방어막 시각 효과 */
        .shield-wave {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 10px; height: 10px;
            border-radius: 50%;
            border: 4px solid #00D2FF;
            opacity: 0;
            pointer-events: none;
        }
        @keyframes shieldWaveAnim {
            0% { width: 10px; height: 10px; opacity: 1; }
            100% { width: 200px; height: 200px; opacity: 0; }
        }
        .shield-wave.active {
            animation: shieldWaveAnim 0.5s ease-out;
        }

        /* --- 버튼 및 로그 --- */
        button {
            background-color: #ff4500;
            color: white;
            border: none;
            padding: 10px 18px;
            margin: 6px;
            font-size: 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            width: 85%;
            transition: background 0.2s, transform 0.1s;
        }
        button:hover { background-color: #ff5722; }
        button:active { transform: scale(0.97); }
        button:disabled { background-color: #555 !important; cursor: not-allowed; transform: scale(1) !important; }

        .sell-btn { background-color: #4CAF50; }
        .sell-btn:hover { background-color: #45a049; }
        .shop-btn { background-color: #2196F3; }
        .shop-btn:hover { background-color: #0b7dda; }

        .log {
            margin-top: 15px;
            height: 90px;
            background: #111;
            padding: 8px;
            border-radius: 5px;
            overflow-y: auto;
            font-size: 13px;
            text-align: left;
            border: 1px solid #444;
            color: #aaa;
        }

        /* --- 30단계 달성 축하 팝업 --- */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.85);
            z-index: 100;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
            opacity: 0;
            transition: opacity 0.5s;
        }
        .modal.show { display: flex; opacity: 1; }
        .modal-content {
            background: linear-gradient(135deg, #2a2a2a 0%, #151515 100%);
            padding: 30px;
            border-radius: 15px;
            border: 3px solid #ffd700;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
            text-align: center;
        }
        .modal h2 {
            color: #ffd700;
            font-size: 28px;
            margin-bottom: 15px;
            text-shadow: 0 0 10px #ffd700;
            animation: victoryGlow 1.5s infinite alternate;
        }
        .modal p { font-size: 18px; margin: 10px 0; }
        @keyframes victoryGlow {
            from { text-shadow: 0 0 10px #ffd700; }
            to { text-shadow: 0 0 25px #ff4500, 0 0 5px #fff; }
        }

    </style>
</head>
<body id="gameBody">

<div class="container">
    <div class="status">
        <p>소유 돈: <span id="money" class="money-text">5,000</span>원 | 폭발 방지권: <span id="shield" class="shield-text">0</span>장</p>
        <p>현재 레벨: <span id="level" class="level-text">1</span> / 30 단계 <span id="prob" class="prob-text">(성공 확률: 100%)</span></p>
    </div>

    <div class="bomb-container" id="bombContainer">
        <!-- 방어막 파동 효과 -->
        <div class="shield-wave" id="shieldWave"></div>
        <!-- 폭탄 이미지 -->
        <img class="bomb-image" id="bombImg" src="" alt="Bomb">
        <!-- 폭탄 이름/위력 설명 -->
        <div class="bomb-name" id="bombName">1단계: 흑색 화약 주머니</div>
    </div>

    <div>
        <button id="upgradeBtn" onclick="tryUpgrade()">강화하기 (<span id="cost">200</span>원)</button>
        <button id="sellBtn" class="sell-btn" onclick="sellBomb()" disabled>원자폭탄 판매 (1단계는 판매 불가)</button>
        <button class="shop-btn" onclick="buyShield()">폭발 방지권 구매 (1,000원)</button>
    </div>

    <div class="log" id="logBox">
        게임이 시작되었습니다. 강화 성공, 방어, 폭발 시 화려한 모션이 실행됩니다!<br>
        마지막 30단계 '행성 파괴자'를 향해 강화해보세요!<br>
    </div>
</div>

<!-- 30단계 달성 축하 모달 -->
<div class="modal" id="victoryModal">
    <div class="modal-content">
        <h2>🏆 최종 단계 달성! 🏆</h2>
        <p>축하합니다!</p>
        <p>당신은 위력 측정 불가, 인류 최강의 폭탄<br><b>'행성 파괴자'</b>를 완성했습니다!</p>
        <button onclick="closeVictoryModal()" style="width: auto; padding: 10px 30px; margin-top: 20px; background-color: #ffd700; color: black;">확인</button>
    </div>
</div>

<script>
    let money = 5000;
    let level = 1;
    let shield = 0;
    let isMaxLevelAchieved = false;

    // --- 1단계부터 30단계까지 화약 -> 폭탄 -> 다이너마이트 -> 원자폭탄 순서의 이미지 데이터 ---
    const bombData = {
        // [1~6단계] 화약 및 초기 폭탄
        1: { name: "1단계: 흑색 화약 주머니", yield: "극소", img: "https://i.imgur.com/rP6hO5E.png" },
        2: { name: "2단계: 화약 도화선 나무통", yield: "매우 작음", img: "https://i.imgur.com/vH3sY8s.png" },
        3: { name: "3단계: 머스킷 구형 탄환", yield: "작음", img: "https://i.imgur.com/8Qj9mZJ.png" },
        4: { name: "4단계: 심지 불붙이는 소형 흑색폭탄", yield: "작음", img: "https://i.imgur.com/b5R4f5U.png" },
        5: { name: "5단계: 중세 공성용 대형 폭탄", yield: "보통", img: "https://i.imgur.com/C4Hk6vH.png" },
        6: { name: "6단계: 파이프 폭탄 사제 폭발물", yield: "보통", img: "https://i.imgur.com/N6sY74U.png" },

        // [7~12단계] 다이너마이트 및 고성능 폭약
        7: { name: "7단계: 다이너마이트 1개 묶음", yield: "강함", img: "https://i.imgur.com/9nFk6Xo.png" },
        8: { name: "8단계: 다이너마이트 다발 (T.N.T.)", yield: "강함", img: "https://i.imgur.com/A6D3B5w.png" },
        9: { name: "9단계: C-4 플라스틱 폭약", yield: "매우 강함", img: "https://i.imgur.com/lD9UjHq.png" },
        10: { name: "10단계: 대인 지뢰", yield: "매우 강함", img: "https://i.imgur.com/1G6O8E0.png" },
        11: { name: "11단계: 대전차 지뢰", yield: "매우 강함", img: "https://i.imgur.com/pZp8UvL.png" },
        12: { name: "12단계: 항공 투하용 고성능 폭탄", yield: "강력함", img: "https://i.imgur.com/uR2iR5q.png" },

        // [13~24단계] 전술핵 및 실존 원자폭탄/수소폭탄
        13: { name: "13단계: 전술핵 데이비 크로켓 (W54)", yield: "0.01 kt", img: "https://i.imgur.com/w9U1sF2.png" },
        14: { name: "14단계: SADM 배낭형 원자폭탄", yield: "0.1 kt", img: "https://i.imgur.com/z8pQ8q4.png" },
        15: { name: "15단계: W48 전술 핵포탄 (155mm)", yield: "0.072 kt", img: "https://i.imgur.com/Y4gUjYw.png" },
        16: { name: "16단계: 가젯 (최초 핵실험)", yield: "19 kt", img: "https://i.imgur.com/tHqXvX7.png" },
        17: { name: "17단계: 리틀 보이 (히로시마 투하)", yield: "15 kt", img: "https://i.imgur.com/5VbO9q3.png" },
        18: { name: "18단계: 팻 맨 (나가사키 투하)", yield: "21 kt", img: "https://i.imgur.com/8N4Jp8g.png" },
        19: { name: "19단계: 아이비 킹 (순수 분열 최대)", yield: "500 kt", img: "https://i.imgur.com/u1t2J5y.png" },
        20: { name: "20단계: 캐슬 브라보 (미국 최대실험 수소폭탄)", yield: "15 Mt", img: "https://i.imgur.com/9C0Dq9y.png" },
        21: { name: "21단계: B83 열핵폭탄 (미군 현용)", yield: "1.2 Mt", img: "https://i.imgur.com/N6d0Bw5.png" },
        22: { name: "22단계: RDS-37 (소련 수소폭탄 설계)", yield: "1.6 Mt", img: "https://i.imgur.com/4Wn4mYw.png" },
        23: { name: "23단계: RDS-220 차르 봄바 (50Mt 모델)", yield: "50 Mt", img: "https://i.imgur.com/Y0q9C4X.png" },
        24: { name: "24단계: 차르 봄바 원형 설계 (100Mt 이론치)", yield: "100 Mt", img: "https://i.imgur.com/X2jY5q3.png" },

        // [25~30단계] 상상속 강력한 핵무기 / 행성 파괴급
        25: { name: "25단계: 코발트 탄 (Doomsday Device 설계)", yield: "1 Gigaton", img: "https://i.imgur.com/6U8O1D5.png" },
        26: { name: "26단계: 고반조 열핵폭탄", yield: "5 Gigaton", img: "https://i.imgur.com/7K9XwV7.png" },
        27: { name: "27단계: 스타브레이커 핵미사일", yield: "10 Gigaton", img: "https://i.imgur.com/r6O0W7v.png" },
        28: { name: "28단계: 노바 버스터 대륙 파괴탄", yield: "대륙급 파괴", img: "https://i.imgur.com/u1w5R9t.png" },
        29: { name: "29단계: 지각 붕괴장치", yield: "지각 파괴급", img: "https://i.imgur.com/6R5G4w8.png" },
        30: { name: "30단계: 행성 파괴자 (Planet Buster)", yield: "측정 불가 (지구 종말)", img: "https://i.imgur.com/wVq6Xf3.png" }
    };

    function getSuccessProb(lvl) {
        if (lvl < 3) return 100;
        // 30단계까지 천천히 낮아지는 확률 로직
        let p = 100 - (lvl * 3.3) + 6;
        return Math.max(5, Math.floor(p)); // 최소 5%
    }

    function getSellPrice(lvl) {
        if (lvl === 1) return 0;
        if (lvl === 2) return 100;
        if (lvl === 3) return 350;
        if (lvl === 4) return 800;
        // 위력 증가에 따른 지수 기반 판매가
        let base = 200;
        return Math.floor(base * Math.pow(lvl, 2.5));
    }

    // --- 화려한 모션 연출 함수 ---
    function triggerAnimation(type) {
        const body = document.getElementById("gameBody");
        const bombImg = document.getElementById("bombImg");
        const bombContainer = document.getElementById("bombContainer");
        const shieldWave = document.getElementById("shieldWave");

        // 이전 애니메이션 클래스 제거
        bombImg.className = "bomb-image";
        body.classList.remove("shake-screen");

        // 애니메이션 트리거 (리플로우 발생)
        void bombImg.offsetWidth; 

        if (type === 'success') {
            bombImg.classList.add("anim-success");
        } else if (type === 'explode') {
            bombImg.classList.add("anim-explode");
            body.classList.add("shake-screen"); // 화면 진동
        } else if (type === 'shield') {
            bombImg.classList.add("anim-shield");
            shieldWave.classList.add("active"); // 푸른 방어막
            setTimeout(() => shieldWave.classList.remove("active"), 500);
        }
    }

    // --- 30단계 승리 브금 (Web Audio API로 직접 생성) ---
    function playVictorySound() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const audioCtx = new AudioContext();
            
            const notes = [
                { f: 261.63, d: 0.1, t: 0 },   // 도
                { f: 329.63, d: 0.1, t: 0.1 }, // 미
                { f: 392.00, d: 0.1, t: 0.2 }, // 솔
                { f: 523.25, d: 0.3, t: 0.3 }, // 도 (높은 도)
                { f: 392.00, d: 0.1, t: 0.7 }, // 솔
                { f: 523.25, d: 0.8, t: 0.8 }  // 도 (길게)
            ];

            notes.forEach(note => {
                const osc = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                
                osc.type = 'triangle'; // 웅장한 느낌을 주는 트라이앵글 파형
                osc.frequency.setValueAtTime(note.f, audioCtx.currentTime + note.t);
                
                gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime + note.t);
                gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + note.t + note.d);
                
                osc.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                
                osc.start(audioCtx.currentTime + note.t);
                osc.stop(audioCtx.currentTime + note.t + note.d);
            });
        } catch (e) {
            console.log("Audio not supported or blocked by browser policies.");
        }
    }

    function showVictoryModal() {
        document.getElementById("victoryModal").classList.add("show");
        playVictorySound();
    }

    function closeVictoryModal() {
        document.getElementById("victoryModal").classList.remove("show");
    }

    function updateUI() {
        document.getElementById("money").innerText = money.toLocaleString();
        document.getElementById("level").innerText = level;
        document.getElementById("shield").innerText = shield;
        
        let currentCost = Math.floor(200 * Math.pow(1.15, level - 1));
        document.getElementById("cost").innerText = currentCost.toLocaleString();
        
        let sellBtn = document.getElementById("sellBtn");
        if (level === 1) {
            sellBtn.disabled = true;
            sellBtn.innerText = "판매 불가 (1단계)";
        } else {
            sellBtn.disabled = false;
            let currentSellPrice = getSellPrice(level);
            sellBtn.innerText = `폭탄 판매 (${currentSellPrice.toLocaleString()}원)`;
        }

        let prob = getSuccessProb(level);
        document.getElementById("prob").innerText = `(성공 확률: ${prob}%)`;

        // 폭탄 정보 업데이트 (이름 및 위력 설명)
        const data = bombData[level] || bombData[30]; // 30단계 초과 시 30단계 고정
        document.getElementById("bombName").innerHTML = `<b>${data.name}</b><br>(위력: ${data.yield})`;
        document.getElementById("bombImg").src = data.img;

        // 30단계 달성 시 만렙 처리
        if (level === 30 && !isMaxLevelAchieved) {
            isMaxLevelAchieved = true;
            document.getElementById("upgradeBtn").disabled = true;
            document.getElementById("upgradeBtn").innerText = "최고 단계 달성!";
            addLog(`🏆 축하합니다! 최종 무기 <span style="color: #ffd700;">[${data.name}]</span>를 완성했습니다!`);
            setTimeout(showVictoryModal, 800); // 연출 후 팝업
        }
    }

    function addLog(message) {
        const logBox = document.getElementById("logBox");
        logBox.innerHTML += message + "<br>";
        logBox.scrollTop = logBox.scrollHeight;
    }

    function tryUpgrade() {
        let cost = Math.floor(200 * Math.pow(1.15, level - 1));
        if (money < cost) {
            addLog("❌ 돈이 부족합니다!");
            return;
        }

        money -= cost;
        let successProb = getSuccessProb(level);
        let chance = Math.random() * 100;

        if (chance < successProb) {
            level++;
            triggerAnimation('success');
            const data = bombData[level];
            addLog(`✨ <span style="color: #4CAF50;">성공!</span> 폭탄이 ${level}단계 <span style="color:#eee;">[${data.name}]</span>로 강화되었습니다.`);
        } else {
            if (shield > 0) {
                shield--;
                triggerAnimation('shield');
                addLog(`🛡️ <span style="color: #2196F3;">방어 성공!</span> 폭발 방지권이 실패를 막았습니다.`);
            } else {
                level = 1;
                isMaxLevelAchieved = false; // 폭발 시 만렙 상태 초기화
                document.getElementById("upgradeBtn").disabled = false;
                triggerAnimation('explode');
                addLog(`💥 <span style="color: #ff4500;">폭발실패!</span> 폭탄이 폭발하여 1단계로 초기화되었습니다.`);
            }
        }
        updateUI();
    }

    function sellBomb() {
        if (level === 1) {
            addLog("❌ 1단계는 판매할 수 없습니다!");
            return;
        }
        let sellPrice = getSellPrice(level);
        money += sellPrice;
        addLog(`💰 ${level}단계 폭탄을 <b style="color:#ffd700;">${sellPrice.toLocaleString()}원</b>에 판매하고 1단계로 초기화했습니다.`);
        level = 1;
        isMaxLevelAchieved = false; // 판매 시 만렙 상태 초기화
        document.getElementById("upgradeBtn").disabled = false;
        updateUI();
    }

    function buyShield() {
        let shieldCost = 1000;
        if (money < shieldCost) {
            addLog("❌ 돈이 부족하여 방지권을 살 수 없습니다 (필요: 1,000원).");
            return;
        }
        money -= shieldCost;
        shield++;
        addLog("🛡️ 폭발 방지권을 1장 구매했습니다!");
        updateUI();
    }

    // 초기 실행
    updateUI();
</script>

</body>
</html>
"""

# Streamlit 에 HTML 코드 주입
components.html(game_html, height=600, scrolling=True)
