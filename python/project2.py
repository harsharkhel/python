import random

computer = random.choice([-1, 0, 1])
you = input("enter your chocie:")
youDict = {"s": 1, "w": -1, "g":0}
reverseDict = {1: "s", -1: "w", 0: "g"}
youNum = youDict[you]

print(f"you chose {reverseDict[youNum]}\n computer chose {reverseDict[computer]} ")

if(computer == youNum):
    print("its a draw!")
else:
    if((computer - youNum) ==  -1 or (computer - youNum) == 2):
        print("you lose!")
    else:
        print("you win!")