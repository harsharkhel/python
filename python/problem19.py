def greatest_of_three():
    a = int(input("enter the number:"))
    b = int(input("enter the number:"))
    c = int(input("enter the number:"))
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c
print(greatest_of_three())