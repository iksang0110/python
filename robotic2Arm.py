import cv2
import mediapipe as mp
import serial
import numpy as np
import time

# Arduino 연결 설정
arduino_left = None
arduino_right = None

def connect_arduino():
    global arduino_left, arduino_right
    try:
        arduino_left = serial.Serial('/dev/cu.usbserial-B0036S3I', 9600, timeout=1)
        arduino_right = serial.Serial('/dev/cu.usbserial-AD0JLDZT', 9600, timeout=1)
        print("Arduino connections established")
    except serial.SerialException as e:
        print(f"Failed to connect to Arduino: {e}")
        return False
    return True

connect_arduino()

# MediaPipe Hands 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# 웹캠 초기화
cap = cv2.VideoCapture(0)

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def calculate_hand_area(hand_landmarks):
    landmarks = np.array([(lm.x, lm.y) for lm in hand_landmarks.landmark])
    hull = cv2.convexHull(np.array(landmarks * [640, 480], dtype=np.int32))
    return cv2.contourArea(hull)

def control_robot_arm(hand_landmarks, is_left):
    hand_area = calculate_hand_area(hand_landmarks)
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # 좌우 움직임을 화면 절반을 기준으로 조정
    if is_left:
        bottom_angle = int(map_range(middle_tip.x, 0, 0.5, 180, 0))
    else:
        bottom_angle = int(map_range(middle_tip.x, 0.5, 1, 180, 0))
 
    forward_angle = int(map_range(hand_area, 1000, 13000, 30, 150))
    height_angle = int(map_range(middle_tip.y, 1, 0, 0, 180))
    
    finger_distance = np.linalg.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_tip.x, index_tip.y]))
    gripper_angle = 90 if finger_distance < 0.05 else 140

    return hand_area, bottom_angle, forward_angle, height_angle, gripper_angle

def send_command(arduino, command):
    try:
        arduino.write(command.encode())
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        return False
    return True

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)  # 좌우 반전
    height, width, _ = image.shape
    
    # 중앙 구분선 그리기
    cv2.line(image, (width//2, 0), (width//2, height), (0, 255, 0), 2)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # 손의 x 좌표를 기준으로 좌우 구분
            is_left = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.5
            
            hand_area, bottom_angle, forward_angle, height_angle, gripper_angle = control_robot_arm(hand_landmarks, is_left)
            
            command = f"{bottom_angle},{forward_angle},{height_angle},{gripper_angle}\n"
            
            if is_left:
                if arduino_right and not send_command(arduino_right, command):
                    if not connect_arduino():
                        continue
                x_offset = 0
                hand_label = "Right"
            else:
                if arduino_left and not send_command(arduino_left, command):
                    if not connect_arduino():
                        continue
                x_offset = width // 2
                hand_label = "Left"

            # 화면에 로봇 팔 정보 표시
            cv2.putText(image, f"{hand_label} Hand Area: {hand_area:.0f}", (10 + x_offset, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(image, f"Bottom: {bottom_angle}", (10 + x_offset, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(image, f"Forward: {forward_angle}", (10 + x_offset, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(image, f"Height: {height_angle}", (10 + x_offset, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(image, f"Gripper: {gripper_angle}", (10 + x_offset, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:  # ESC 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
if arduino_left:
    arduino_left.close()
if arduino_right:
    arduino_right.close()