import cv2
import numpy as np

# 이미지를 불러옵니다.
image_path = '/Users/02.011x/Downloads/KakaoTalk_Photo_2024-06-06-18-17-57.png'
image = cv2.imread(image_path)

# 이미지가 제대로 불러와졌는지 확인합니다.
if image is None:
    raise FileNotFoundError(f"이미지를 불러올 수 없습니다: {image_path}")

# HOG 기반 사람 검출기를 초기화합니다.
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 사람을 검출합니다.
(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

# 사람 수를 셉니다.
person_count = len(rects)

# 검출된 각 사람을 사각형으로 표시합니다.
for (x, y, w, h) in rects:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 결과를 출력합니다.
if person_count >= 30:
    queue_status = "long waiting."
else:
    queue_status = "short waiting."

# 이미지에 사람 수와 대기 시간 상태를 표시합니다.
cv2.putText(image, f"the number of people: {person_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv2.putText(image, queue_status, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# 결과 이미지를 표시합니다.
cv2.imshow('Queue Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 프로그램을 종료합니다.
exit()
