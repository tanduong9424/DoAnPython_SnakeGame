from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color("red")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        random_x = random.randint(-140, 140) * 2  # Chỉ random từ -140 đến 140, sau đó nhân với 2 để có số chẵn
        random_y = random.randint(-140, 140) * 2
        self.goto(random_x, random_y)



