import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# 주어진 전달 함수 정의
numerator = [1, 12]  # 분자 s + 12
denominator = [1, 15, 54, 40]  # 분모 s^3 + 15s^2 + 54s + 40
G_s = ctl.TransferFunction(numerator, denominator)

# 1) 근궤적 그리기
plt.figure()
_, klist = ctl.root_locus(G_s, Plot=True)
plt.show()

# 근궤적을 통한 K 값 찾기 (시스템이 안정한 범위 내에서)
# K 값의 범위를 설정
k_range = np.linspace(0, 10, 1000)

# 근궤적 데이터로부터 안정한 K 값의 범위를 찾음
# 이 부분은 근궤적 그래프를 통해 시각적으로 확인할 수 있습니다.

# 2) 단위 계단 응답 그리기
# 시각적으로 확인한 K 값 중 안정한 시스템에 대한 K 값을 사용
# 여기서는 예시로 K = 1을 사용합니다. 실제로는 근궤적 그래프를 통해 결정해야 합니다.
K = 12 # 이 값은 근궤적 그래프를 통해 조정해야 함
T = np.linspace(0, 10, 1000)  # 10초 동안의 시간 벡터

# 단위 계단 응답 계산
system_with_feedback = ctl.feedback(G_s * K, 1)
T, yout = ctl.step_response(system_with_feedback, T)

# 응답 그래프 그리기
plt.figure()
plt.plot(T, yout)
plt.title('Unit Step Response')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

# 응답의 오버슛을 계산하여 10% 이내인지 확인
overshoot = (np.max(yout) - 1) * 100
print('Overshoot:', overshoot)