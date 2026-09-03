import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="원자폭탄 강화하기 30단계", page_icon="💥", layout="centered")

st.markdown("<h1 style='text-align: center;'>💥 원자폭탄 강화하기 (30단계) 💥</h1>", unsafe_allow_html=True)

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
            max-width: 500px;
            margin: 0 auto;
            background: #2a2a2a;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);
        }
        .status {
            font-size: 15px;
            margin: 8px 0;
            background: #1e1e1e;
            padding: 10px;
            border-radius: 8px;
        }
        .bomb-container {
            min-height: 180px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 15px 0;
            background: #151515;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 10px;
        }
        .bomb-image {
            font-size: 65px;
            transition: transform 0.2s;
            margin-bottom: 5px;
        }
        .bomb-img-tag {
            max-width: 140px;
            max-height: 100px;
            object-fit: contain;
            display: none; /* 이미지 URL이 삽입되면 JS로 block 처리 가능 */
        }
        .bomb-info {
            font-size: 16px;
            font-weight: bold;
            color: #ff9800;
        }
        .bomb-yield {
            font-size: 13px;
            color: #aaa;
        }

        /* 애니메이션 효과 클래스들 */
        @keyframes bounceSuccess {
            0% { transform: scale(1); }
            50% { transform: scale(1.3) rotate(10deg); filter: drop-shadow(0 0 15px #4CAF50); }
            100% { transform: scale(1); }
        }
        .anim-success {
            animation: bounceSuccess 0.5s ease;
        }

        @keyframes explodeBomb {
            0% { transform: scale(1); filter: brightness(1); }
            30% { transform: scale(1.6); filter: drop-shadow(0 0 30px #ff4500) brightness(1.5); }
            60% { transform: scale(0.8) rotate(-15deg); }
            100% { transform: scale(1); filter: brightness(1); }
        }
        .anim-explode {
            animation: explodeBomb 0.6s ease;
        }

        @keyframes shieldShield {
            0% { transform: scale(1); }
            30% { transform: scale(1.2); filter: drop-shadow(0 0 20px #2196F3); }
            100% { transform: scale(1); }
        }
        .anim-shield {
            animation: shieldShield 0.6s ease;
        }

        button {
            background-color: #ff4500;
            color: white;
            border: none;
            padding: 10px 18px;
            margin: 5px;
            font-size: 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            width: 88%;
        }
        button:hover { background-color: #ff5722; }
        .sell-btn { background-color: #4CAF50; }
        .sell-btn:hover { background-color: #45a049; }
        .sell-btn:disabled { background-color: #555; cursor: not-allowed; }
        .shop-btn { background-color: #2196F3; }
        .shop-btn:hover { background-color: #0b7dda; }
        
        .log {
            margin-top: 15px;
            height: 100px;
            background: #111;
            padding: 8px;
            border-radius: 5px;
            overflow-y: auto;
            font-size: 13px;
            text-align: left;
            border: 1px solid #444;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="status">
        <div>소유 돈: <span id="money" style="color:#ffd700; font-weight:bold;">5,000</span>원 | 방지권: <span id="shield" style="color:#2196F3; font-weight:bold;">0</span>장</div>
        <div style="margin-top:5px;">현재: <span id="level" style="color:#ff5722; font-weight:bold;">1</span> / 30 단계 (성공 확률: <span id="prob">100</span>%)</div>
    </div>

    <div class="bomb-container">
        <div class="bomb-image" id="bombImg">💣</div>
        <!-- 이미지가 준비되었을 경우 img 태그 활성화 사용 가능 -->
        <img id="bombCustomImg" class="bomb-img-tag" src="" alt="폭탄 이미지">
        <div class="bomb-info" id="bombName">1단계 폭탄</div>
        <div class="bomb-yield" id="bombYield">위력: 0.01 kt</div>
    </div>

    <div>
        <button id="upgradeBtn" onclick="tryUpgrade()">강화하기 (<span id="cost">200</span>원)</button>
        <button id="sellBtn" class="sell-btn" onclick="sellBomb()" disabled>원자폭탄 판매 (1단계 판매 불가)</button>
        <button class="shop-btn" onclick="buyShield()">폭발 방지권 구매 (1,000원)</button>
    </div>

    <div class="log" id="logBox">
        ☢️ 30단계 원자폭탄 강화하기 게임에 오신 것을 환영합니다!<br>
        인류 최후의 무기인 '차르 봄바'를 향해 강화해보세요.<br>
    </div>
</div>

<script>
    let money = 5000;
    let level = 1;
    let shield = 0;

    // 1단계부터 30단계까지의 폭탄 데이터 정의 (이름, 위력, 아이콘, 이미지URL)
    const bombData = {
        1:  { name: "데이비 크로켓 (Davy Crockett)", yield: "0.01 kt (초소형 전술핵)", icon: "🎯", img: "" },
        2:  { name: "W48 전술 핵포탄", yield: "0.072 kt", icon: "🚀", img: "" },
        3:  { name: "SADM 배낭형 원자폭탄", yield: "0.1 kt", icon: "🎒", img: "" },
        4:  { name: "W54 초소형 탄두", yield: "0.25 kt", icon: "📦", img: "" },
        5:  { name: "W25 공대공 핵미사일", yield: "1.5 kt", icon: "✈️", img: "" },
        6:  { name: "가젯 (Trinity Test)", yield: "19 kt (인류 최초의 핵실험)", icon: "⚙️", img: "" },
        7:  { name: "리틀 보이 (Little Boy)", yield: "15 kt (히로시마 투하)", icon: "💣", img: "" },
        8:  { name: "팻 맨 (Fat Man)", yield: "21 kt (나가사키 투하)", icon: "🛢️", img: "" },
        9:  { name: "교차로 작전 (Operation Crossroads)", yield: "23 kt", icon: "⚓", img: "" },
        10: { name: "아이비 기공 (Ivy King)", yield: "500 kt (최대 순수 분열 폭탄)", icon: "⚡", img: "" },
        11: { name: "W27 열핵탄두", yield: "2 Mt", icon: "🔥", img: "" },
        12: { name: "W49 ICBM 탄두", yield: "1.44 Mt", icon: "🚀", img: "" },
        13: { name: "W56 중거리 탄두", yield: "1.2 Mt", icon: "☄️", img: "" },
        14: { name: "B28 수소폭탄", yield: "1.45 Mt", icon: "💥", img: "" },
        15: { name: "B83 수소폭탄", yield: "1.2 Mt (미군 현용 최대)", icon: "🛡️", img: "" },
        16: { name: "B53 대형 수소폭탄", yield: "9 Mt", icon: "🌋", img: "" },
        17: { name: "EC-17 대형 수소폭탄", yield: "10 Mt", icon: "☣️", img: "" },
        18: { name: "캐슬 브라보 (Castle Bravo)", yield: "15 Mt (미국 최대 핵실험)", icon: "🏖️", img: "" },
        19: { name: "캐슬 얀키 (Castle Yankee)", yield: "13.5 Mt", icon: "🌊", img: "" },
        20: { name: "B41 (Mk 41) 수소폭탄", yield: "25 Mt (미국 역사상 최고 위력)", icon: "👑", img: "" },
        21: { name: "RDS-37 소련 수소폭탄", yield: "1.6 Mt", icon: "❄️", img: "" },
        22: { name: "RDS-6s (조 칼 4)", yield: "400 kt", icon: "🛰️", img: "" },
        23: { name: "중국 최초 수소폭탄 (Test No. 6)", yield: "3.3 Mt", icon: "🐉", img: "" },
        24: { name: "프랑스 카노푸스 (Canopus)", yield: "2.6 Mt", icon: "⚜️", img: "" },
        25: { name: "영국 그래플 Z (Grapple Z)", yield: "3 Mt", icon: "🏰", img: "" },
        26: { name: "소련 219번 시험 (Test 219)", yield: "24.2 Mt", icon: "🪐", img: "" },
        27: { name: "차르 봄바 프로토타입", yield: "30 Mt", icon: "☠️", img: "" },
        28: { name: "차르 봄바 축소판 (RDS-220 50M)", yield: "50 Mt", icon: "🎆", img: "" },
        29: { name: "차르 봄바 원형 (RDS-220 100M 설계)", yield: "100 Mt (이론상 최대)", icon: "☀️", img: "" },
        30: { name: "행성 파괴자 (Doomsday Device)", yield: "∞ Mt (지구 파괴급 종말 무기)", icon: "🌌", img: "" }
    };

    function getSuccessProb(lvl) {
        if (lvl < 3) return 100;
        if (lvl >= 28) return Math.max(5, 35 - (lvl * 1.0)); // 후반부는 5~10% 확률
        return Math.max(10, 100 - (lvl * 3.2));
    }

    function getSellPrice(lvl) {
        if (lvl === 1) return 0;
        let base = 150;
        return Math.floor(base * Math.pow(lvl, 2.3));
    }

    function triggerAnimation(animClass) {
        const bombElement = document.getElementById("bombImg");
        bombElement.className = "bomb-image " + animClass;
        setTimeout(() => {
            bombElement.className = "bomb-image";
        }, 600);
    }

    function updateUI() {
        document.getElementById("money").innerText = money.toLocaleString();
        document.getElementById("level").innerText = level;
        document.getElementById("shield").innerText = shield;
        
        let currentCost = Math.floor(200 * Math.pow(1.25, level - 1));
        document.getElementById("cost").innerText = currentCost.toLocaleString();
        
        let sellBtn = document.getElementById("sellBtn");
        if (level === 1) {
            sellBtn.disabled = true;
            sellBtn.innerText = "원자폭탄 판매 (1단계 판매 불가)";
        } else {
            sellBtn.disabled = false;
            let currentSellPrice = getSellPrice(level);
            sellBtn.innerText = `원자폭탄 판매 (${currentSellPrice.toLocaleString()}원)`;
        }

        let prob = getSuccessProb(level).toFixed(0);
        document.getElementById("prob").innerText = prob;

        // 현재 단계 폭탄 정보 갱신
        let data = bombData[level] || bombData[30];
        document.getElementById("bombName").innerText = `${level}단계: ${data.name}`;
        document.getElementById("bombYield").innerText = `위력: ${data.yield}`;
        
        // 커스텀 이미지 URL이 등록되어 있다면 이미지를 띄우고, 없으면 아이콘 텍스트 표시
        const customImgTag = document.getElementById("bombCustomImg");
        const bombIconTag = document.getElementById("bombImg");

        if (data.img && data.img.trim() !== "") {
            customImgTag.src = data.img;
            customImgTag.style.display = "block";
            bombIconTag.style.display = "none";
        } else {
            bombIconTag.innerText = data.icon;
            bombIconTag.style.display = "block";
            customImgTag.style.display = "none";
        }

        // 30단계 달성 시 만렙 처리
        if (level === 30) {
            document.getElementById("upgradeBtn").disabled = true;
            document.getElementById("upgradeBtn").innerText = "🏆 최고 단계 달성! (최종 무기)";
        }
    }

    function addLog(message) {
        const logBox = document.getElementById("logBox");
        logBox.innerHTML += message + "<br>";
        logBox.scrollTop = logBox.scrollHeight;
    }

    function tryUpgrade() {
        let cost = Math.floor(200 * Math.pow(1.25, level - 1));
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
            let nextBomb = bombData[level];
            addLog(`✨ <span style="color: #4CAF50;">성공!</span> [${nextBomb.name}] (으)로 강화되었습니다.`);
        } else {
            if (shield > 0) {
                shield--;
                triggerAnimation("anim-shield");
                addLog(`🛡️ <span style="color: #2196F3;">방어 성공!</span> 폭발 방지권이 발동하여 실패를 막았습니다.`);
            } else {
                level = 1;
                triggerAnimation("anim-explode");
                addLog(`💥 <span style="color: #ff4500;">폭발실패!</span> 폭탄이 폭발하여 1단계로 초기화되었습니다.`);
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
        addLog(`💰 ${level}단계 폭탄을 판매하여 <b>${sellPrice.toLocaleString()}원</b>을 얻었습니다.`);
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

components.html(game_html, height=620, scrolling=True)
