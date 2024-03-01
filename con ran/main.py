import time
from turtle import Screen
from snake import Snake
from food import Food
from score import Score

# Set up the screen
window = Screen()
window.setup(width=1500, height=800)
window.bgcolor("black")
window.title("Snake Hunter")
window.tracer(0)

# Make the window fullscreen with the preset size
window.setup(width=1.0, height=1.0)

# Create the snake, food objects
snake = Snake()
food = Food()

# Set up keyboard bindings for snake movement
window.listen()
window.onkey(snake.up, "Up")
window.onkey(snake.down, "Down")
window.onkey(snake.left, "Left")
window.onkey(snake.right, "Right")

# Initialize the game state
is_game_active = True
if is_game_active:
    score = Score()  # If the game is not active, don't display the score

# Main game loop
while is_game_active:
    window.update()
    time.sleep(0.1)
    snake.move()

    # Eat Food
    if snake.head.distance(food) < 20:
        score.increase_score()
        snake.extend()
        food.refresh()

    # Pass through walls
    for part in snake.parts:
        if part.xcor() > 700:
            part.goto(-700, part.ycor())
        elif part.xcor() < -700:
            part.goto(700, part.ycor())
        elif part.ycor() > 260:
            part.goto(part.xcor(), -350)
        elif part.ycor() < -350:
            part.goto(part.xcor(), 260)

    # Check for collision with the snake's tail
    for part in snake.parts[1:]:
        if snake.head.distance(part) < 10:
            is_game_active = False
            score.game_over()

# Close the window when clicked
window.exitonclick()
