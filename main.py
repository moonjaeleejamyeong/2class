import random
import streamlit as st

st.set_page_config(
    page_title="Project-Ultimate-Nuke", page_icon="☢️", layout="centered"
)

# 세션 상태 초기화
if "power_kt" not in st.session_state:
  st.session_state.power_kt = 10
  st.session_state.stability = 100
  st.session_state.commits = 0
  st.session_state.logs = ["게임이 시작되었습니다. 커밋으로 위력을 높이세요!"]
  st.session_state.game_over = False


def add_log(msg):
  st.session_state.logs.append(msg)
  if len(st.session_state.logs) > 10:
    st.session_state.logs.pop(0)


st.title("=== [GitHub: Project-Ultimate-Nuke] ===")

# 상태 지표 표시
col1, col2, col3 = st.columns(3)
col1.metric("현재 위력", f"{st.session_state.power_kt:,} kt")
col2.metric("시스템 안정성", f"{st.session_state.stability}%")
col3.metric("총 커밋", f"{st.session_state.commits}회")

st.markdown("---")

# 게임 종료 조건 체크
if st.session_state.stability <= 0:
  st.error(
      "🔥 [MELTDOWN] 시스템 안정성 0% 도달! 원자폭탄이 개발자 PC와 함께"
      " 증발했습니다. Game Over."
  )
  st.session_state.game_over = True
elif st.session_state.power_kt >= 10000:
  st.success(
      f"🎉 [VICTORY] 위력 {st.session_state.power_kt:,} kt 달성! 깃허브 역사상"
      " 가장 강력한 궁극의 핵무기가 완성되었습니다!"
  )
  st.session_state.game_over = True

# 명령어 버튼 배치
b_col1, b_col2, b_col3, b_col4 = st.columns(4)
disabled = st.session_state.game_over

if b_col1.button("git commit", disabled=disabled):
  st.session_state.commits += 1
  st.session_state.power_kt += random.randint(50, 150)
  st.session_state.stability -= random.randint(3, 7)
  if st.session_state.stability < 0:
    st.session_state.stability = 0
  add_log("✨ [git commit] 핵분열 알고리즘 최적화 코드를 커밋했습니다.")
  st.rerun()

if b_col2.button("git push", disabled=disabled):
  if random.random() < 0.20:
    add_log(
        "💥 [CRITICAL EXPLOSION] 푸시 중 불안정한 코드로 폭발 발생! 초기화면으로"
        " 리셋됩니다."
    )
    st.session_state.power_kt = 10
    st.session_state.stability = 100
    st.session_state.commits = 0
  else:
    if random.random() < 0.25:
      st.session_state.stability -= 25
      if st.session_state.stability < 0:
        st.session_state.stability = 0
      add_log("⚠️ [Merge Conflict!] 충돌 해결 실패로 방사능 누출! 안정성 급감.")
    else:
      st.session_state.power_kt += random.randint(300, 700)
      st.session_state.stability -= random.randint(5, 15)
      if st.session_state.stability < 0:
        st.session_state.stability = 0
      add_log(
          "🚀 [git push origin main] 핵탄두 설계도가 원격 서버에 반영되었습니다!"
      )
  st.rerun()

if b_col3.button("git pull", disabled=disabled):
  st.session_state.stability = min(100, st.session_state.stability + 20)
  add_log("🛡️ [git pull] 보안 패치 동기화 완료. 시스템 안정성 회복.")
  st.rerun()

if b_col4.button("git status", disabled=disabled):
  add_log(
      f"📊 [git status]: 코어 온도 위험 수준. 현재 안정성"
      f" {st.session_state.stability}%."
  )
  st.rerun()

st.markdown("### 📋 실행 로그")
log_text = "\n".join(st.session_state.logs)
st.text_area("Log", value=log_text, height=150, label_visibility="collapsed")

if st.button("🔄 게임 초기화 (Reset)"):
  st.session_state.power_kt = 10
  st.session_state.stability = 100
  st.session_state.commits = 0
  st.session_state.logs = ["게임이 초기화되었습니다."]
  st.session_state.game_over = False
  st.rerun()
