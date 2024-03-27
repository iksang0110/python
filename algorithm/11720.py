
# a = input()
# sum = 0
# for num in a:
#     sum += int(num) #할당 연산자 += 왼쪽 변수에 오른쪽 값에 더한 후 왼쪽변수에 저장 sum= sum + int(num) 과 같음 )
# print(sum)

# import random

# num_count = int(input("뽑을 랜덤 숫자의 개수를 입력하세요: "))
# random_numbers = []

# for _ in range(num_count):
#     number = random.randint(1, 100)
#     random_numbers.append(number)

# print("생성된 랜덤 숫자:", random_numbers)
# print("랜덤 숫자의 합:", sum(random_numbers))
# --------------------------------------------
# import random

# N = int(input())
# L = [random.randrange(N) for _ in range(N)]
# print("리스트:", L)
# print("결과값:", sum(L))
# --------------------------------------------------
import random

N = int(input())
L = [] 
for _ in range(N):
    L.append(random.randrange(N))  

print("리스트:", L)
print("결과값:", sum(L))
# -------------------------------------------------
# import random

# N = int(input())
# L = []
# sum = 0

# for num in range(N) :
#     L.append(random.randrange(N))
# for num in L :
#     sum = sum + num

# print("리스트 : ", L)
# print("결과값 : ", sum)