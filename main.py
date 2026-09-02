<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>GitHub Repository: Project-Ultimate-Nuke</title>
    <style>
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #161b22;
            border: 1px solid #30363d;
            padding: 30px;
            border-radius: 8px;
            width: 500px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        h1 { font-size: 1.2rem; color: #58a6ff; margin-bottom: 20px; }
        .stats { margin-bottom: 20px; line-height: 1.6; }
        .buttons { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
        button {
            background-color: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 10px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background-color: #30363d; border-color: #8b949e; }
        button.danger { background-color: #da3633; color: white; border: none; }
        button.danger:hover { background-color: #b62324; }
        #log {
            background-color: #010409;
            border: 1px solid #30363d;
            padding: 10px;
            height: 120px;
            overflow-y: auto;
            font-size: 0.85rem;
            border-radius: 4px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>=== [GitHub: Project-Ultimate-Nuke] ===</h1>
    <div class="stats" id="stats">
        현재 위력: 10 kt<br>
        시스템 안정성: 100%<br>
        총 커밋: 0회
    </div>
    <div class="buttons">
        <button onclick="commitCode()">git commit</button>
        <button onclick="pushCode()">git push</button>
        <button onclick="pullCode()">git pull</button>
        <button onclick="statusCheck()">git status</button>
    </div>
    <div id="log">게임이 시작되었습니다. 커밋으로 위력을 높이세요!<br></div>
</div>

<script>
    let power_kt = 10;
    let stability = 100;
    let commits = 0;

    function updateDisplay() {
        document.getElementById('stats').innerHTML = `
            현재 위력: ${power_kt.toLocaleString()} kt<br>
            시스템 안정성: ${stability}%<br>
            총 커밋: ${commits}회
        `;
    }

    function logMessage(msg) {
        const logDiv = document.getElementById('log');
        logDiv.innerHTML += msg + "<br>";
        logDiv.scrollTop = logDiv.scrollHeight;
    }

    function checkGameOver() {
        if (stability <= 0) {
            logMessage("🔥 [MELTDOWN] 시스템 안정성 0% 도달! 원자폭탄이 개발자 PC와 함께 증발했습니다. Game Over.");
            disableButtons();
        } else if (power_kt >= 10000) {
            logMessage(`🎉 [VICTORY] 위력 ${power_kt.toLocaleString()} kt 달성! 깃허브 역사상 가장 강력한 궁극의 핵무기가 완성되었습니다!`);
            disableButtons();
        }
    }

    function disableButtons() {
        const btns = document.querySelectorAll('button');
        btns.forEach(b => b.disabled = true);
    }

    function commitCode() {
        commits += 1;
        power_kt += Math.floor(Math.random() * 101) + 50;
        stability -= Math.floor(Math.random() * 5) + 3;
        if (stability < 0) stability = 0;
        logMessage("✨ [git commit] 핵분열 알고리즘 최적화 코드를 커밋했습니다.");
        updateDisplay();
        checkGameOver();
    }

    function pushCode() {
        if (Math.random() < 0.20) {
            logMessage("💥 [CRITICAL EXPLOSION] 푸시 중 불안정한 코드로 폭발 발생! 초기화면으로 리셋됩니다.");
            power_kt = 10;
            stability = 100;
            commits = 0;
            updateDisplay();
            return;
        }

        if (Math.random() < 0.25) {
            stability -= 25;
            if (stability < 0) stability = 0;
            logMessage("⚠️ [Merge Conflict!] 충돌 해결 실패로 방사능 누출! 안정성 급감.");
        } else {
            power_kt += Math.floor(Math.random() * 400) + 300;
            stability -= Math.floor(Math.random() * 11) + 5;
            if (stability < 0) stability = 0;
            logMessage("🚀 [git push origin main] 핵탄두 설계도가 원격 서버에 반영되었습니다!");
        }
        updateDisplay();
        checkGameOver();
    }

    function pullCode() {
        stability = Math.min(100, stability + 20);
        logMessage("🛡️ [git pull] 보안 패치 동기화 완료. 시스템 안정성 회복.");
        updateDisplay();
    }

    function statusCheck() {
        logMessage(`📊 [git status]: 코어 온도 위험 수준. 현재 안정성 ${stability}%.`);
    }
</script>

</body>
</html>
