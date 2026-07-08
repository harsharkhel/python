import random

computer = random.choice([-1, 0, 1])
you = input("enter your chocie:")
youDict = {"s": 1, "w": -1, "g":0}
reverseDict = {1: "s", -1: "w", 0: "g"}
youNum = youDict[you]

print(f"you chose {reverseDict[youNum]}\n computer chose {reverseDict[computer]} ")

if(computer == youNum):
    print("you draw!")
elif(computer == -1 and youNum == 1):
    print("You win!")   
elif(computer == -1 and youNum == 0):
    print("You lose!")
elif(computer == 0 and youNum == 1):
    print("You win!")
elif(computer == 0 and youNum == 0):
    print("You draw!")
elif(computer == 1 and youNum == -1):
    print("You win!")
elif(computer == 1 and youNum == 0):
    print("You lose!")
else:
    print("You lose!")