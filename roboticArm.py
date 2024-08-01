import cv2
import mediapipe as mp
import serial
import numpy as np

# Arduino 연결 설정
arduino = serial.Serial('/dev/cu.usbserial-AD0JLDZT', 9600)  # 포트와 baudrate는 실제 환경에 맞게 조정

# MediaPipe Hands 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# 웹캠 초기화
cap = cv2.VideoCapture(0)

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def calculate_hand_area(hand_landmarks):
    landmarks = np.array([(lm.x, lm.y) for lm in hand_landmarks.landmark])
    hull = cv2.convexHull(np.array(landmarks * [640, 480], dtype=np.int32))
    return cv2.contourArea(hull)

def control_robot_arm(hand_landmarks):
    # 손바닥 면적 계산
    hand_area = calculate_hand_area(hand_landmarks)
    
    # 손가락 끝점 좌표
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # 바닥 회전 관절 제어 (좌우) - 수정된 부분
    bottom_angle = int(map_range(middle_tip.x, 0, 1, 0, 180))
    
    # 앞뒤 관절 제어 (손 면적)
    if hand_area <= 7000:
        forward_angle = int(map_range(hand_area, 1000, 7000, 30, 90))
    else:
        forward_angle = int(map_range(hand_area, 7000, 13000, 90, 150))
    
    # 높이 관절 제어 (상하)
    height_angle = int(map_range(middle_tip.y, 1, 0, 0, 180))
    
    # 집게 제어 (엄지와 검지가 닿았는지 확인)
    finger_distance = np.linalg.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_tip.x, index_tip.y]))
    gripper_angle = 90 if finger_distance < 0.05 else 140  # 임계값 0.05는 조정 가능

    # 아두이노로 각도 정보 전송
    command = f"{bottom_angle},{forward_angle},{height_angle},{gripper_angle}\n"
    arduino.write(command.encode())

    return hand_area, forward_angle, bottom_angle, gripper_angle

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # 이미지를 RGB로 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 손 인식 처리
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 손 랜드마크 그리기
            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # 로봇 팔 제어 및 정보 계산
            hand_area, forward_angle, bottom_angle, gripper_angle = control_robot_arm(hand_landmarks)
            
            # 화면에 정보 표시
            cv2.putText(image, f"Hand area: {hand_area:.0f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Forward angle: {forward_angle}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Bottom angle: {bottom_angle}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Gripper angle: {gripper_angle}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:  # ESC 키로 종료
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()