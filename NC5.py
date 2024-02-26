
from random import randint

print("Welcome to Casino")
pc_choice = randint(1,50)

playing = True

while playing:
    user_choice = int(input("Choose number.(1-50)"))
    if user_choice == pc_choice:
        print("You won!")
        playing = False
    elif user_choice > pc_choice:
        print("Lower!")
    elif user_choice < pc_choice:
        print("Higher!")

