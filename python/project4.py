import turtle
import math

# Create screen
screen = turtle.Screen()
screen.bgcolor("black")

# Create turtle
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.penup()
t.color("#ffb6c1")

# Draw the heart using text
for scale in range(11, 17):
    for i in range(120):
        angle = i * (math.pi / 60)

        x = 16 * (math.sin(angle) ** 3) * scale
        y = (
            13 * math.cos(angle)
            - 5 * math.cos(2 * angle)
            - 2 * math.cos(3 * angle)
            - math.cos(4 * angle)
        ) * scale

        t.goto(x, y)
        t.write(
            "I love you",
            align="center",
            font=("Arial", 10, "bold")
        )

turtle.done()