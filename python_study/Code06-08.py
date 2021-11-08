## 전역 변수 선언 부분 ##
i, k, rnrneks = 0, 0, ""

## 메인 코드 부분 ##
for i in range(2, 10):
    rnrneks = rnrneks + ("# %d단 #"% i)

print(rnrneks)

for i in range(1, 10):
    rnrneks =""
    for k in range(2, 10):
        rnrneks = rnrneks + str("%2d X %2d = %2d" % (k, i, k*i))
    print(rnrneks)