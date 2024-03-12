import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

window = tkinter.Tk()
window.title("Snake Apple game")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="light green", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
apple = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
power_up = None  # Power-up tile
blocks = []  # List to store the block tiles
velocityX = 0
velocityY = 0
snake_body = []
game_over = False
score = 0
apple_counter = 0

# Function to create blocks
def create_blocks():
    for _ in range(10):
        block = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)
        blocks.append(block)

create_blocks()

def change_direction(event):
    global velocityX, velocityY, game_over
    if game_over:
        return

    if event.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif event.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif event.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif event.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():
    global snake, apple, power_up, snake_body, game_over, score, apple_counter
    if game_over:
        return

    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    for block in blocks:
        if snake.x == block.x and snake.y == block.y:
            game_over = True
            return

    # Check if snake eats the apple
    if snake.x == apple.x and snake.y == apple.y:
        snake_body.append(Tile(apple.x, apple.y))
        score += 1
        apple_counter += 1

        if apple_counter == 5:  # Generate power-up every 5 apples eaten
            apple_counter = 0
            generate_power_up()

        apple.x = random.randint(0, COLS - 1) * TILE_SIZE
        apple.y = random.randint(0, ROWS - 1) * TILE_SIZE

    # Check if snake eats the power-up
    if power_up is not None and snake.x == power_up.x and snake.y == power_up.y:
        for _ in range(3):
            snake_body.append(Tile(snake_body[-1].x, snake_body[-1].y))
        power_up = None  # Remove power-up after eaten

    # Move snake
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            previous_tile = snake_body[i - 1]
            tile.x = previous_tile.x
            tile.y = previous_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def generate_power_up():
    global power_up
    power_up = Tile(random.randint(0, COLS - 1) * TILE_SIZE, random.randint(0, ROWS - 1) * TILE_SIZE)

def draw():
    global snake, apple, power_up, snake_body, game_over, score
    move()

    canvas.delete("all")

    # Draw apple
    canvas.create_rectangle(apple.x, apple.y, apple.x + TILE_SIZE, apple.y + TILE_SIZE, fill="red")

    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="orange")
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="orange")

    # Draw power-up if exists
    if power_up is not None:
        canvas.create_rectangle(power_up.x, power_up.y, power_up.x + TILE_SIZE, power_up.y + TILE_SIZE, fill="yellow")

    # Draw blocks
    for block in blocks:
        canvas.create_rectangle(block.x, block.y, block.x + TILE_SIZE, block.y + TILE_SIZE, fill="black")

    # Draw score/game over text
    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text=f"Game Over: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    window.after(100, draw)

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()
