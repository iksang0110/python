import cv2
import face_recognition

# 웹캠 비디오 스트림을 캡처합니다.
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 의미합니다.

if not cap.isOpened():
    raise Exception("웹캠을 열 수 없습니다.")

while True:
    # 프레임을 읽습니다.
    ret, frame = cap.read()
    
    if not ret:
        break

    # 얼굴을 검출합니다.
    face_locations = face_recognition.face_locations(frame)

    # 검출된 얼굴 수를 셉니다.
    person_count = len(face_locations)

    # 검출된 각 얼굴을 사각형으로 표시합니다.
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # 결과를 출력합니다.
    if person_count >= 10:
        queue_status = "long waiting."
    else:
        queue_status = "short waitiong."

    # 이미지에 사람 수와 대기 시간 상태를 표시합니다.
    cv2.putText(frame, f"the number of people: {person_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, queue_status, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # 결과 프레임을 표시합니다.
    cv2.imshow('Queue Detection', frame)

    # 'q' 키를 누르면 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 창을 닫고 캡처를 해제합니다.
cap.release()
cv2.destroyAllWindows()
