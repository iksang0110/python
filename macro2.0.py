import pyautogui
import keyboard
import time
import sys

click_positions = []  # 클릭할 위치를 저장할 리스트
program_running = True

print("프로그램 사용 방법:")
print("1. 's' 키를 눌러 클릭할 위치 저장")
print("2. 'b' 키를 눌러 모든 위치 클릭 시작")
print("3. 'esc' 키로 프로그램 종료")
print("긴급 정지: 마우스를 화면의 왼쪽 상단 모서리로 이동")

# 긴급 정지 설정
pyautogui.FAILSAFE = True

def record_position():
    x, y = pyautogui.position()
    click_positions.append((x, y))
    print(f"위치 저장됨: {x}, {y}")

def start_macro():
    if not click_positions:
        print("저장된 위치가 없습니다. 먼저 위치를 저장하세요.")
        return
    
    print("실행 전 확인: 시작하려면 enter 키를 누르세요 (취소하려면 'c'를 누르세요).")
    user_input = input()
    if user_input.lower() == 'c':
        print("작업이 취소되었습니다.")
        return
    
    for pos in click_positions:
        if not program_running:
            print("프로그램이 사용자에 의해 중단되었습니다.")
            break
        pyautogui.click(pos[0], pos[1])
        print(f"클릭 위치: {pos[0]}, {pos[1]}")
        time.sleep(0.25)  # 클릭 사이에 0.25초 대기

def exit_program():
    global program_running
    program_running = False
    print("프로그램을 종료합니다.")
    sys.exit()

keyboard.add_hotkey('s', record_position)
keyboard.add_hotkey('b', start_macro)
keyboard.add_hotkey('esc', exit_program)

while program_running:
    time.sleep(1)