import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="원자폭탄 강화하기", page_icon="💥", layout="centered")

st.markdown("<h1 style='text-align: center;'>💥 원자폭탄 강화하기 💥</h1>", unsafe_allow_html=True)

# HTML, CSS, JavaScript 게임 코드를 스트림릿에 삽입
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
        }
        .status {
            font-size: 16px;
            margin: 10px 0;
        }
        .bomb-image {
            font-size: 70px;
            margin: 15px 0;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
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
    </style>
</head>
<body>

<div class="container">
    <div class="status">
        <p>소유 돈: <span id="money">5000</span>원 | 폭발 방지권: <span id="shield">0</span>장</p>
        <p>현재 레벨: <span id="level">1</span>단계 (성공 확률: <span id="prob">95</span>%)</p>
    </div>

    <div class="bomb-image" id="bombImg">💣</div>

    <div>
        <button id="upgradeBtn" onclick="tryUpgrade()">강화하기 (<span id="cost">200</span>원)</button>
        <button class="sell-btn" onclick="sellBomb()">원자폭탄 판매 (<span id="sellPrice">150</span>원)</button>
        <button class="shop-btn" onclick="buyShield()">폭발 방지권 구매 (1,000원)</button>
    </div>

    <div class="log" id="logBox">
        게임이 시작되었습니다. 행운을 빕니다!<br>
    </div>
</div>

<script>
    let money = 5000;
    let level = 1;
    let shield = 0;

    const bombIcons = {
        1: "💣", 3: "🧨", 5: "🔥", 8: "☢️", 10: "⚛️", 13: "🌋", 15: "🌍"
    };

    function updateUI() {
        document.getElementById("money").innerText = money.toLocaleString();
        document.getElementById("level").innerText = level;
        document.getElementById("shield").innerText = shield;
        
        let currentCost = level * 200;
        document.getElementById("cost").innerText = currentCost.toLocaleString();
        
        let currentSellPrice = Math.floor(200 * Math.pow(1.5, level - 1));
        document.getElementById("sellPrice").innerText = currentSellPrice.toLocaleString();

        let prob = Math.max(20, 100 - (level * 4));
        document.getElementById("prob").innerText = prob;

        let currentIcon = "💣";
        for (let lvl in bombIcons) {
            if (level >= parseInt(lvl)) { currentIcon = bombIcons[lvl]; }
        }
        document.getElementById("bombImg").innerText = currentIcon;
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
        let successProb = Math.max(20, 100 - (level * 4));
        let chance = Math.random() * 100;

        if (chance < successProb) {
            level++;
            addLog(`✨ <span style="color: #4CAF50;">성공!</span> 원자폭탄이 ${level}단계로 강화되었습니다.`);
        } else {
            if (shield > 0) {
                shield--;
                addLog(`🛡️ <span style="color: #2196F3;">방어 성공!</span> 폭발 방지권이 발동했습니다.`);
            } else {
                level = 1;
                addLog(`💥 <span style="color: #ff4500;">실패 및 폭발!</span> 1단계로 초기화되었습니다.`);
            }
        }
        updateUI();
    }

    function sellBomb() {
        let sellPrice = Math.floor(200 * Math.pow(1.5, level - 1));
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

# 스트림릿 내에 HTML 컴포넌트 렌더링 (높이 설정)
components.html(game_html, height=520, scrolling=True)
