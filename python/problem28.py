import random
n = random.randint(1, 100)
a = -1
guesses = 0
while (a != n):
    guesses += 1
    a = int(input("guess a number:"))
    if(a < n):
        print("too low")
    else:
        print("too high")
print(f"you guessed the correct number in {guesses} attempts")