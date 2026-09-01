import random
import time

def play_github_nuke_game():
    power_kt = 10     # 초기 위력 (킬로톤)
    stability = 100   # 시스템 안정성 (%)
    commits = 0

    print("=== [GitHub Repository: Project-Ultimate-Nuke] ===")
    print("목표: 깃허브 커밋과 푸시로 원자폭탄의 위력을 강화하세요.")
    print("주의: push할 때마다 일정 확률로 '랜덤 폭발'이 일어날 수 있습니다!\n")
    
    while True:
        print(f"현재 위력: {power_kt:,} kt | 안정성: {stability}% | 총 커밋: {commits}회")
        command = input("git 명령어 입력 (commit / push / pull / status / exit): ").strip().lower()

        if command == "exit":
            print("게임을 종료합니다.")
            break
            
        elif "commit" in command:
            commits += 1
            power_kt += random.randint(50, 150)
            stability -= random.randint(3, 7)
            print("✨ [git commit] 핵분열 알고리즘 최적화 코드를 커밋했습니다. 위력이 상승합니다.")
            
        elif "push" in command:
            # 20% 확률로 랜덤 폭발 발생 (원한다면 확률 조절 가능)
            if random.random() < 0.20:
                print("\n💥 [CRITICAL EXPLOSION] 원격 저장소로 푸시하던 중 불안정한 코드로 인해 원자폭탄이 갑자기 폭발했습니다!")
                print("초기화면으로 돌아갑니다...\n")
                time.sleep(2)
                # 게임 상태 리셋
                power_kt = 10
                stability = 100
                commits = 0
                continue

            if random.random() < 0.25:
                stability -= 25
                print("⚠️ [Merge Conflict!] 충돌 해결 실패로 방사능 누출 발생! 안정성이 급감합니다.")
            else:
                power_kt += random.randint(300, 700)
                stability -= random.randint(5, 15)
                print("🚀 [git push origin main] 원격 서버에 핵탄두 설계도가 반영되었습니다! 위력 대폭 상승!")
                
        elif "pull" in command:
            stability = min(100, stability + 20)
            print("🛡️ [git pull] 보안 패치를 동기화하여 시스템 안정성이 회복되었습니다.")
            
        elif "status" in command:
            print(f"📊 [git status]: 현재 코어 온도 위험 수준. 안정성 {stability}% 관리 시급.")
            
        else:
            print("❌ 지원하지 않는 명령어입니다. (commit, push, pull, status 중 선택)")

        # 안정성 0 이하로 떨어질 때의 종료 조건
        if stability <= 0:
            print("\n🔥 [MELTDOWN] 시스템 안정성 0% 도달! 원자폭탄이 개발자 PC와 함께 증발했습니다. Game Over.")
            break
        elif power_kt >= 10000:
            print(f"\n🎉 [VICTORY] 위력 {power_kt:,} kt 달성! 깃허브 역사상 가장 강력한 궁극의 핵무기가 완성되었습니다!")
            break

if __name__ == "__main__":
    play_github_nuke_game()
