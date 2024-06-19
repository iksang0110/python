import cv2
import torch
import time

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 'yolov5s', 'yolov5m', 'yolov5l', 'yolov5x'

# 카메라 초기화
cap = cv2.VideoCapture(0)

def detect_people(frame):
    results = model(frame)
    detections = results.pred[0]

    people_count = 0
    for *box, conf, cls in detections:
        if int(cls) == 0:  # 0번 클래스가 'person'입니다.
            people_count += 1
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'Person: {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return people_count

start_time = time.time()
people_counts = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    people_count = detect_people(frame)
    people_counts.append(people_count)

    cv2.putText(frame, f'People Count: {people_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 평균 대기 시간 계산
total_people = sum(people_counts)
elapsed_time = time.time() - start_time
average_wait_time = elapsed_time / total_people if total_people else 0

print(f'Average Wait Time: {average_wait_time:.2f} seconds')
