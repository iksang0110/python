# playing = True

# while playing:
#     # Prompt the user to input two numbers
#     a = int(input("Choose a number:\n"))
#     b = int(input("Choose another one:\n"))
    
#     # Ask the user to choose an operation
#     operation = input("Choose an operation:\n    Options are: +, -, *, or /.\n    Write 'exit' to finish.\n")

#     # Check the operation and perform the corresponding calculation
#     if operation == "+":
#         result = a + b
#         print("Result:", result)
#     elif operation == "-":
#         result = a - b
#         print("Result:", result)
#     elif operation == "*":
#         result = a * b
#         print("Result:", result)
#     elif operation == "/":
#         # Check to prevent division by zero
#         if b != 0:
#             result = a / b
#             print("Result:", result)
#         else:
#             print("Error: Division by zero is not allowed.")
#     elif operation.lower() == "exit":
#         # Set playing to False to exit the loop
#         playing = False
#         print("Exiting the calculator.")
#     else:
#         # Handle invalid operation input
#         print("Invalid operation. Please choose +, -, *, or /.")

#     # Add a newline for better readability between operations
#     print() 

# playing = True

# while playing:
#     a = int(input("숫자를 선택하세요:\n"))
#     b = int(input("다른 숫자를 선택하세요:\n"))
#     operation = input("연산자를 선택하세요 (+, -, *, /) 또는 종료하려면 'exit' 입력:\n")

#     if operation == 'exit':
#         print("계산기를 종료합니다.")
#         playing = False
#     elif operation in ['+', '-', '*', '/']:
#         if operation == '+':
#             result = a + b
#         elif operation == '-':
#             result = a - b
#         elif operation == '*':
#             result = a * b
#         elif operation == '/' and b != 0:
#             result = a / b
#         else:
#             print("0으로 나눌 수 없습니다.")
#             continue
#         print("결과:", result)
#     else:
#         print("유효하지 않은 연산입니다.")

playing = True

while playing:
    a = int(input("Choose a number:\n"))
    b = int(input("Choose another number:\n"))
    operation = input("Choose an operation (+, -, *, /) or type 'exit' to quit:\n")

    if operation == 'exit':
        print("Exiting calculator.")
        playing = False
    elif operation in ['+', '-', '*', '/']:
        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        elif operation == '*':
            result = a * b
        elif operation == '/' and b != 0:
            result = a / b
        else:
            print("Cannot divide by zero.")
            continue
        print("Result:", result)
    else:
        print("Invalid operation.")
#     else:
# playing = True
# while playing == True:
#     a = int(input("Choose a number:\n"))
#     b = int(input("Choose another one:\n"))
#     operation = input(
#         "Choose an operation:\n    Options are: + , - , * or /.\n    Write 'exit' to finish.\n")

#     if operation == "+":
#         print(a+b)
#     elif operation == "-":
#         print(a-b)
#     elif operation == "*":
#         print(a*b)
#     elif operation == "/":
#         print(a/b)
#     elif operation == "exit":
#         playing = False