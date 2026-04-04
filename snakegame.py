import turtle
import random

WIDTH = 500
HEIGHT = 500
FOOD_SIZE = 10
DELAY = 100

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

def reset():
    global snake, snake_direction, food_pos

    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)

    move_snake()


def move_snake():
    global snake_direction

    # Create new head
    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Self-collision
    if new_head in snake[:-1]:
        reset()
        return

    snake.append(new_head)

    # Check food
    if not food_collision():
        snake.pop(0)

    # Screen wrapping
    if snake[-1][0] > WIDTH/2:
        snake[-1][0] -= WIDTH
    elif snake[-1][0] < -WIDTH/2:
        snake[-1][0] += WIDTH

    if snake[-1][1] > HEIGHT/2:
        snake[-1][1] -= HEIGHT
    elif snake[-1][1] < -HEIGHT/2:
        snake[-1][1] += HEIGHT

    # Clear old snake drawings
    pen.clearstamps()

    # Draw new snake
    for segment in snake:
        pen.goto(segment[0], segment[1])
        pen.stamp()

    screen.update()

    turtle.ontimer(move_snake, DELAY)


def food_collision():
    global food_pos

    if get_distance(snake[-1], food_pos) < 20:   # collision range
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True

    return False


def get_random_food_pos():
    # Use integers — randint does NOT accept floats!
    x = random.randint(-WIDTH//2 + FOOD_SIZE, WIDTH//2 - FOOD_SIZE)
    y = random.randint(-HEIGHT//2 + FOOD_SIZE, HEIGHT//2 - FOOD_SIZE)
    return (x, y)


def get_distance(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5


def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"


# --- SCREEN SETUP ---
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game")
screen.bgcolor("black")
screen.tracer(0)  # disable animation for smooth movement

# --- SNAKE PEN ---
pen = turtle.Turtle("square")
pen.penup()
pen.color("yellow")

# --- FOOD ---
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# --- KEYS ---
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

# START GAME
reset()
turtle.done()
