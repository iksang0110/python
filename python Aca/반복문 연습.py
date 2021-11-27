menu = ['','우유', '콜라', '홍차']
price = [0,1000, 2000, 3000]


i = 1

while i< len(menu):
    print(i, menu[i], price[i])
    
    i = i+1


n = int(input("음료를 선택하세요 : "))
total = price[n] 
print(menu[n], price[n],'원 ', '합계 ', total, '원')



while n != 0:
    print()
    n = int(input("계속 주문은 음료 번호를, 지불은 0을 누르세요 : "))
    if n > 0 and n < len(menu):
        total = total + price[n]
        print(menu[n], price[n],'원 ', '합계 ', total, '원')
    else :
        if n == 0 :
            print("주문이 완료되었습니다.")
        else :
            print("없는 메뉴입니다.")