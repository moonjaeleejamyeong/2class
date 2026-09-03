import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="원자폭탄 강화하기", page_icon="💥", layout="centered")

st.markdown("<h1 style='text-align: center;'>💥 원자폭탄 강화하기 💥</h1>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            background-color: #1a1a1a;
            color: #ffffff;
            text-align: center;
            margin: 0;
            padding: 10px;
        }
        .container {
            max-width: 480px;
            margin: 0 auto;
            background: #2a2a2a;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
            position: relative;
            overflow: hidden;
        }
        .status {
            font-size: 16px;
            margin: 10px 0;
        }
        .bomb-container {
            min-height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 15px 0;
            position: relative;
        }
        .bomb-image {
            font-size: 70px;
            transition: transform 0.2s;
            max-width: 100px;
            max-height: 100px;
            object-fit: contain;
        }

        /* 화려하게 업그레이드된 애니메이션 효과 클래스들 */
        @keyframes bounceSuccess {
            0% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 5px #4CAF50); }
            30% { transform: scale(1.5) rotate(-15deg); filter: drop-shadow(0 0 35px #00FF66) brightness(1.5); }
            60% { transform: scale(1.2) rotate(15deg); filter: drop-shadow(0 0 25px #00FF66); }
            100% { transform: scale(1) rotate(0deg); filter: drop-shadow(0 0 0px transparent); }
        }
        .anim-success {
            animation: bounceSuccess 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes explodeBomb {
            0% { transform: scale(1); filter: brightness(1); }
            20% { transform: scale(2) rotate(10deg); filter: drop-shadow(0 0 50px #ff0000) brightness(2); }
            40% { transform: scale(0.3) rotate(-20deg); filter: drop-shadow(0 0 80px #ff4500) brightness(3); }
            70% { transform: scale(1.3); filter: drop-shadow(0 0 30px #ff0000); }
            100% { transform: scale(1) rotate(0deg); filter: brightness(1); }
        }
        .anim-explode {
            animation: explodeBomb 0.7s ease-in-out;
        }

        @keyframes shieldShield {
            0% { transform: scale(1); }
            30% { transform: scale(1.4); filter: drop-shadow(0 0 40px #00D2FF) brightness(1.8); }
            60% { transform: scale(0.9); filter: drop-shadow(0 0 20px #0088FF); }
            100% { transform: scale(1); filter: drop-shadow(0 0 0px transparent); }
        }
        .anim-shield {
            animation: shieldShield 0.6s ease-out;
        }

        /* 진동 효과 */
        @keyframes containerShake {
            0% { transform: translate(0, 0); }
            20% { transform: translate(-10px, 10px); }
            40% { transform: translate(10px, -10px); }
            60% { transform: translate(-10px, -5px); }
            80% { transform: translate(10px, 5px); }
            100% { transform: translate(0, 0); }
        }
        .shake {
            animation: containerShake 0.4s ease-in-out;
        }

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
        }
        button:hover { background-color: #ff5722; }
        .sell-btn { background-color: #4CAF50; }
        .sell-btn:hover { background-color: #45a049; }
        .sell-btn:disabled { background-color: #555; cursor: not-allowed; }
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
        }

        /* 30단계 축하 팝업 모달 */
        .modal {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 100;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
        }
        .modal h2 {
            color: #FFD700;
            font-size: 28px;
            margin-bottom: 10px;
            text-shadow: 0 0 10px #FFD700;
            animation: victoryGlow 1s infinite alternate;
        }
        @keyframes victoryGlow {
            from { text-shadow: 0 0 10px #FFD700; transform: scale(1); }
            to { text-shadow: 0 0 25px #FF4500; transform: scale(1.05); }
        }
    </style>
</head>
<body>

<div class="container" id="mainContainer">
    <!-- 30단계 완료 모달 -->
    <div class="modal" id="victoryModal">
        <h2>🎉 최종 단계 달성! 🎉</h2>
        <p style="font-size: 18px; color: #fff;">인류 최강의 원자폭탄을 완성했습니다!</p>
        <button onclick="closeModal()" style="width: auto; padding: 10px 25px; background: #FFD700; color: #000;">확인</button>
    </div>

    <div class="status">
        <p>소유 돈: <span id="money">5000</span>원 | 폭발 방지권: <span id="shield">0</span>장</p>
        <p>현재 레벨: <span id="level">1</span>단계 (성공 확률: <span id="prob">100</span>%)</p>
    </div>

    <div class="bomb-container">
        <img class="bomb-image" id="bombImg" src="https://cdn-icons-png.flaticon.com/512/112/112683.png" alt="Bomb">
    </div>

    <div>
        <button id="upgradeBtn" onclick="tryUpgrade()">강화하기 (<span id="cost">200</span>원)</button>
        <button id="sellBtn" class="sell-btn" onclick="sellBomb()" disabled>원자폭탄 판매 (1단계는 판매 불가)</button>
        <button class="shop-btn" onclick="buyShield()">폭발 방지권 구매 (1,000원)</button>
    </div>

    <div class="log" id="logBox">
        게임이 시작되었습니다. 강화 성공, 방어, 폭발 시 애니메이션 모션이 실행됩니다!<br>
    </div>
</div>

<script>
    let money = 5000;
    let level = 1;
    let shield = 0;

    // 1단계부터 30단계까지 제일 약한 것부터 쎈 것 순서로 배치된 30개의 이미지 URL
    const bombIcons = {
        1: "https://cdn-icons-png.flaticon.com/512/112/112683.png",   // Davy Crockett (초소형)
        2: "https://cdn-icons-png.flaticon.com/512/595/595568.png",
        3: "https://cdn-icons-png.flaticon.com/512/811/811452.png",
        4: "https://cdn-icons-png.flaticon.com/512/2592/2592201.png",
        5: "https://cdn-icons-png.flaticon.com/512/921/921490.png",
        6: "https://cdn-icons-png.flaticon.com/512/1033/1033095.png",
        7: "https://cdn-icons-png.flaticon.com/512/1685/1685816.png", // Little Boy
        8: "https://cdn-icons-png.flaticon.com/512/2910/2910313.png", // Fat Man
        9: "https://cdn-icons-png.flaticon.com/512/921/921434.png",
        10: "https://cdn-icons-png.flaticon.com/512/2061/2061832.png",
        11: "https://cdn-icons-png.flaticon.com/512/1785/1785210.png",
        12: "https://cdn-icons-png.flaticon.com/512/1356/1356479.png",
        13: "https://cdn-icons-png.flaticon.com/512/2936/2936886.png",
        14: "https://cdn-icons-png.flaticon.com/512/595/595576.png",
        15: "https://cdn-icons-png.flaticon.com/512/921/921473.png",
        16: "https://cdn-icons-png.flaticon.com/512/2855/2855598.png",
        17: "https://cdn-icons-png.flaticon.com/512/2936/2936932.png",
        18: "https://cdn-icons-png.flaticon.com/512/1785/1785218.png", // Castle Bravo
        19: "https://cdn-icons-png.flaticon.com/512/2061/2061875.png",
        20: "https://cdn-icons-png.flaticon.com/512/811/811438.png",
        21: "https://cdn-icons-png.flaticon.com/512/2592/2592233.png",
        22: "https://cdn-icons-png.flaticon.com/512/1033/1033073.png",
        23: "https://cdn-icons-png.flaticon.com/512/2910/2910340.png",
        24: "https://cdn-icons-png.flaticon.com/512/1356/1356502.png",
        25: "https://cdn-icons-png.flaticon.com/512/1685/1685830.png",
        26: "https://cdn-icons-png.flaticon.com/512/921/921505.png",
        27: "https://cdn-icons-png.flaticon.com/512/2855/2855605.png",
        28: "https://cdn-icons-png.flaticon.com/512/2936/2936950.png",
        29: "https://cdn-icons-png.flaticon.com/512/1785/1785235.png", // Tsar Bomba (Proto)
        30: "https://cdn-icons-png.flaticon.com/512/2061/2061900.png"  // Tsar Bomba (최종)
    };

    function getSuccessProb(lvl) {
        if (lvl < 3) return 100;
        return Math.max(5, 100 - (lvl * 3.2));
    }

    function getSellPrice(lvl) {
        if (lvl === 1) return 0;
        if (lvl === 2) return 100;
        if (lvl === 3) return 350;
        if (lvl === 4) return 800;
        let cumulativeCost = 100 * lvl * (lvl - 1);
        return cumulativeCost + (lvl * 400);
    }

    // 화려한 연출을 위한 트리거 함수
    function triggerAnimation(animClass) {
        const bombElement = document.getElementById("bombImg");
        const container = document.getElementById("mainContainer");
        
        bombElement.className = "bomb-image " + animClass;
        container.classList.add("shake");

        setTimeout(() => {
            bombElement.className = "bomb-image";
            container.classList.remove("shake");
        }, 700);
    }

    // Web Audio API를 이용한 웅장한 승리 오케스트라 브금 재생
    function playVictoryBGM() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            const ctx = new AudioContext();
            
            const notes = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99, 1046.50]; // 도-미-솔-도-미-솔-도 웅장한 아르페지오
            notes.forEach((freq, index) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, ctx.currentTime + (index * 0.12));
                
                gain.gain.setValueAtTime(0.3, ctx.currentTime + (index * 0.12));
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + (index * 0.12) + 1.5);
                
                osc.connect(gain);
                gain.connect(ctx.destination);
                
                osc.start(ctx.currentTime + (index * 0.12));
                osc.stop(ctx.currentTime + (index * 0.12) + 1.5);
            });
        } catch(e) {
            console.log("Audio not supported or blocked by browser policies.");
        }
    }

    function showVictoryModal() {
        document.getElementById("victoryModal").style.display = "flex";
        playVictoryBGM();
    }

    function closeModal() {
        document.getElementById("victoryModal").style.display = "none";
    }

    function updateUI() {
        document.getElementById("money").innerText = money.toLocaleString();
        document.getElementById("level").innerText = level;
        document.getElementById("shield").innerText = shield;
        
        let currentCost = level * 200;
        document.getElementById("cost").innerText = currentCost.toLocaleString();
        
        let sellBtn = document.getElementById("sellBtn");
        if (level === 1) {
            sellBtn.disabled = true;
            sellBtn.innerText = "원자폭탄 판매 (1단계는 판매 불가)";
        } else {
            sellBtn.disabled = false;
            let currentSellPrice = getSellPrice(level);
            sellBtn.innerText = `원자폭탄 판매 (${currentSellPrice.toLocaleString()}원)`;
        }

        let prob = getSuccessProb(level).toFixed(1);
        document.getElementById("prob").innerText = prob;

        // 레벨에 맞는 이미지 매핑
        let currentImg = bombIcons[1];
        if (bombIcons[level]) {
            currentImg = bombIcons[level];
        } else if (level > 30) {
            currentImg = bombIcons[30];
        }
        document.getElementById("bombImg").src = currentImg;
    }

    function addLog(message) {
        const logBox = document.getElementById("logBox");
        logBox.innerHTML += message + "<br>";
        logBox.scrollTop = logBox.scrollHeight;
    }

    function tryUpgrade() {
        let cost = level * 200;
        if (money < cost) {
            addLog("❌ 돈이 부족합니다!");
            return;
        }

        money -= cost;
        let successProb = getSuccessProb(level);
        let chance = Math.random() * 100;

        if (chance < successProb) {
            level++;
            triggerAnimation("anim-success");
            addLog(`✨ <span style="color: #4CAF50;">성공!</span> 원자폭탄이 ${level}단계로 강화되었습니다.`);
            
            // 30단계 달성 시 웅장한 브금과 축하 모달 실행
            if (level === 30) {
                setTimeout(() => {
                    showVictoryModal();
                }, 500);
            }
        } else {
            if (shield > 0) {
                shield--;
                triggerAnimation("anim-shield");
                addLog(`🛡️ <span style="color: #2196F3;">방어 성공!</span> 폭발 방지권이 발동했습니다.`);
            } else {
                level = 1;
                triggerAnimation("anim-explode");
                addLog(`💥 <span style="color: #ff4500;">실패 및 폭발!</span> 1단계로 초기화되었습니다.`);
            }
        }
        updateUI();
    }

    function sellBomb() {
        if (level === 1) {
            addLog("❌ 1단계 원자폭탄은 판매할 수 없습니다!");
            return;
        }
        let sellPrice = getSellPrice(level);
        money += sellPrice;
        addLog(`💰 ${level}단계 원자폭탄을 ${sellPrice.toLocaleString()}원에 판매했습니다.`);
        level = 1;
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

    updateUI();
</script>

</body>
</html>
"""

components.html(game_html, height=560, scrolling=True)
