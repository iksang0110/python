import pyautogui
import keyboard
import time

click_positions = [] # 클릭할 위치를 저장할 리스트

print("마우스로 클릭할 위치를 설정한 후 's' 키를 눌러 위치를 저장하세요. 모든 위치를 설정한 후 'b'키를 눌러 실행하세요.")

def record_position(x, y):
    global click_positions
    click_positions.append((x,y))
    print(f"위치 저장됨: {x}, {y}")

def start_macro():
        for pos in click_positions:
            pyautogui.click(pos[0], pos[1])
            print(f"클릭 위치: {pos[0]}{pos[1]}")
            time.sleep(1) #클릭 사이에 1초대기

keyboard.add_hotkey('s', lambda: record_position(pyautogui.position()[0], pyautogui.position()[1]))
keyboard.add_hotkey('b', start_macro)

keyboard.wait('esc')
