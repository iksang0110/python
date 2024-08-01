import cv2
import mediapipe as mp
import numpy as np
import serial

# Arduino 연결 (포트는 실제 환경에 맞게 수정 필요)
arduino = serial.Serial('/dev/tty.usbserial-AD0JLDZT', 9600, timeout=1)

# MediaPipe 손 추적 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# 카메라 캡처 초기화
cap = cv2.VideoCapture(0)

# 화면 크기 설정 (더 크게 변경)
screen_width, screen_height = 1280, 720  # Full HD 크기로 변경
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# 가상 박스 정의 (화면 크기에 맞춰 조정)
box_size = int(min(screen_width, screen_height) * 0.9)  # 화면 크기의 90%로 증가
box_x = (screen_width - box_size) // 2
box_y = (screen_height - box_size) // 2

def map_range(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

# 손목 크기의 이동 평균을 계산하기 위한 변수
wrist_sizes = []
max_sizes = 10  # 이동 평균을 계산할 최대 크기 수

# 초기 기준 크기 설정
initial_size = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # 프레임을 좌우 반전
    frame = cv2.flip(frame, 1)

    # 프레임을 RGB로 변환
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 손바닥 중심점 (0번 랜드마크) 좌표 추출
            palm_x = int(hand_landmarks.landmark[0].x * frame.shape[1])
            palm_y = int(hand_landmarks.landmark[0].y * frame.shape[0])

            # 박스 내 좌표로 변환
            box_palm_x = min(max(palm_x - box_x, 0), box_size)
            box_palm_y = min(max(palm_y - box_y, 0), box_size)

            # 손목 크기 계산 (손목 랜드마크의 너비)
            wrist = hand_landmarks.landmark[0]
            wrist_size = wrist.x * frame.shape[1]  # 손목 랜드마크의 x 좌표를 픽셀 단위로 변환

            # 초기 기준 크기 설정
            if initial_size is None:
                initial_size = wrist_size
                print(f"Initial wrist size set to: {initial_size}")

            # 상대적 크기 계산
            relative_size = wrist_size / initial_size

            # 이동 평균 계산
            wrist_sizes.append(relative_size)
            if len(wrist_sizes) > max_sizes:
                wrist_sizes.pop(0)
            avg_wrist_size = sum(wrist_sizes) / len(wrist_sizes)

            # 로봇 팔 각도로 매핑
            bottom_angle = int(map_range(box_palm_x, 0, box_size, 180, 0))
            height_angle = int(map_range(box_palm_y, 0, box_size, 180, 30))  # 높낮이 반전
            forward_angle = int(map_range(avg_wrist_size, 0.5, 1.5, 40, 120))  # 손목 크기에 따른 전진/후진, 범위 조정

            # 주먹 쥔 상태 확인
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
            gripper_angle = 140 if distance > 0.1 else 90

            # Arduino로 데이터 전송
            command = f"{bottom_angle},{forward_angle},{height_angle},{gripper_angle}\n"
            arduino.write(command.encode())

            # 손 랜드마크 그리기
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 디버그 정보 표시
            cv2.putText(frame, f"Bottom: {bottom_angle}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Forward: {forward_angle}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Height: {height_angle}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Gripper: {gripper_angle}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Relative Wrist Size: {avg_wrist_size:.3f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 가상 박스 그리기
    cv2.rectangle(frame, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 255, 0), 2)

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(5) & 0xFF == 27:  # ESC 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()