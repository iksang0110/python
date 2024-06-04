import pyautogui
import time
import keyboard

def get_position(prompt):
    input(prompt)  # 사용자가 엔터를 누를 때까지 기다립니다.
    return pyautogui.position()

def main():
    print("첫 번째 클릭 위치를 설정합니다. 마우스를 원하는 위치에 놓고 Enter를 누르세요.")
    first_click_position = get_position("Enter 키를 누르면 첫 번째 클릭 위치가 저장됩니다...")

    print("두 번째 클릭 위치를 설정합니다. 마우스를 원하는 위치에 놓고 Enter를 누르세요.")
    second_click_position = get_position("Enter 키를 누르면 두 번째 클릭 위치가 저장됩니다...")

    repeat_count = int(input("반복 횟수를 입력하세요: "))

    try:
        for _ in range(repeat_count):
            # 첫 번째 위치에서 클릭
            pyautogui.click(first_click_position)
            print("첫 번째 위치에서 클릭 완료.")
            # 20분 동안 대기 (20분 = 1200초)
            time.sleep(1500)

            # 키보드 인터럽트 체크
            if keyboard.is_pressed('esc'):
                print("사용자에 의해 스크립트가 중단되었습니다.")
                break

            # 두 번째 위치에서 클릭
            pyautogui.click(second_click_position)
            print("두 번째 위치에서 클릭 완료.")
            # 3초 대기
            time.sleep(3)

            # 다시 첫 번째 위치에서 즉시 클릭
            pyautogui.click(first_click_position)
            print("다시 첫 번째 위치에서 즉시 클릭 완료.")

            # 키보드 인터럽트 체크
            if keyboard.is_pressed('esc'):
                print("사용자에 의해 스크립트가 중단되었습니다.")
                break

    except Exception as e:
        print(f"스크립트 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()

