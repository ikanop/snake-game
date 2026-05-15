from tkinter import Tk, Canvas, Label, ALL
import random


GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 150
SPACE_SIZE = 100
BODY_PARTS = 3
SNAKE_BODY_COLOR = "yellow"
SNAKE_HEAD_COLOR = "blue"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
input_queue = []


class Snake:
    def __init__(self):

        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append((i * SPACE_SIZE, 0))

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=SNAKE_BODY_COLOR,
                tags="snake",
            )
            self.squares.append(square)


class Food:
    def __init__(self):

        all_positions = [
            (x * SPACE_SIZE, y * SPACE_SIZE)
            for x in range(GAME_WIDTH // SPACE_SIZE)
            for y in range(GAME_HEIGHT // SPACE_SIZE)
        ]

        free_positions = [pos for pos in all_positions if pos not in snake.coordinates]

        x, y = random.choice(free_positions)

        self.coordinates = (x, y)
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food"
        )


def next_turn(snake, food):

    change_direction()

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_BODY_COLOR
    )
    snake.squares.insert(0, square)

    for body_square in snake.squares[1:]:
        canvas.itemconfig(body_square, fill=SNAKE_BODY_COLOR)

    canvas.itemconfig(snake.squares[0], fill=SNAKE_HEAD_COLOR)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        if victory():
            return

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction():

    global direction, input_queue

    if len(input_queue) > 0:
        new_direction = input_queue.pop(0)
    else:
        return

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def add_to_queue(new_input):

    global input_queue, direction

    if len(input_queue) > 0:
        last_direction = input_queue[-1]
    else:
        last_direction = direction

    if (
        (last_direction == "up" and new_input == "down")
        or (last_direction == "down" and new_input == "up")
        or (last_direction == "right" and new_input == "left")
        or (last_direction == "left" and new_input == "right")
    ):
        return

    if len(input_queue) == 0 and new_input == direction:
        return

    if len(input_queue) > 0 and input_queue[-1] == new_input:
        return

    if len(input_queue) >= 3:
        return

    input_queue.append(new_input)


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():

    canvas.delete(ALL)

    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("", 70),
        text="GAME OVER",
        fill="red",
        tags="gameover",
    )


def victory():

    total_cells = (GAME_WIDTH // SPACE_SIZE) * (GAME_HEIGHT // SPACE_SIZE)

    if len(snake.coordinates) >= total_cells:
        canvas.delete(ALL)

        canvas.create_text(
            canvas.winfo_width() / 2,
            canvas.winfo_height() / 2,
            font=("", 70),
            text="VICTORY!!!",
            fill="green",
            tags="victory",
        )
        return True
    return False


def restart_game():

    global snake, food, score, input_queue, direction

    canvas.delete(ALL)

    score = 0
    direction = "down"
    input_queue = []

    snake = Snake()
    food = Food()

    next_turn(snake, food)


window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

for key in ["<Left>", "<a>"]:
    window.bind(key, lambda event, d="left": add_to_queue(d))
for key in ["<Right>", "<d>"]:
    window.bind(key, lambda event, d="right": add_to_queue(d))
for key in ["<Up>", "<w>"]:
    window.bind(key, lambda event, d="up": add_to_queue(d))
for key in ["<Down>", "<s>"]:
    window.bind(key, lambda event, d="down": add_to_queue(d))

window.bind("r", lambda event: restart_game())

snake = Snake()

food = Food()


next_turn(snake, food)


window.mainloop()

