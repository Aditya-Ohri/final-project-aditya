import arcade

# Set the number of columns and rows for the board
ROW_COUNT = 6
COLUMN_COUNT = 7

# Set the dimensions of each grid location on the board
WIDTH = 50
HEIGHT = 50
RADIUS = 23

# Set the dimensions of the header text
TEXT_HEIGHT = 50

# Compute the Screen's dimensions and set the name
SCREEN_WIDTH = WIDTH * COLUMN_COUNT
SCREEN_HEIGHT = HEIGHT * ROW_COUNT + TEXT_HEIGHT
SCREEN_TITLE = "Connect 4 Game"

# Generate 2-d grid filled with 0's to represent empty slots
grid = [[0 for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]

# Set variables to initialize game
turn = 1
game_over = False


def winning_move(piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (grid[r][c] == piece and grid[r][c + 1] == piece
            and grid[r][c + 2] == piece and grid[r][c + 3] == piece):
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if (grid[r][c] == piece and grid[r + 1][c] == piece
            and grid[r + 2][c] == piece and grid[r + 3][c] == piece):
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if (grid[r][c] == piece and grid[r + 1][c + 1] == piece
            and grid[r + 2][c + 2] == piece and grid[r + 3][c + 3] == piece):
                return True

    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (grid[r][c] == piece and grid[r - 1][c + 1] == piece
            and grid[r - 2][c + 2] == piece and grid[r - 3][c + 3] == piece):
                return True


def on_update(delta_time):
    pass

def on_draw():
    global game_over
    global turn
    arcade.start_render()
    # Draw the game board
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            # Determine the colour of the circular slot
            if grid[row][column] == 0:
                colour = arcade.color.BLACK
            elif grid[row][column] == 1:
                colour = arcade.color.RED
            else:
                colour = arcade.color.YELLOW

            # Compute the centre coordinates for each grid location
            x = WIDTH * column + WIDTH // 2
            y = HEIGHT * row + HEIGHT // 2

            # Draw each grid location as a slot on the Connect 4 board
            arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, arcade.color.BLUE)
            arcade.draw_circle_filled(x, y, RADIUS, colour)
    if game_over and turn % 2 == 0:
        arcade.draw_text("Player 1 Wins!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 20, width=200, align="center")
    elif game_over and turn % 2 == 1:
        arcade.draw_text("Player 2 Wins!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 20, width=200, align="center")


def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    column = x // WIDTH
    row = y // HEIGHT
    global turn
    global game_over

    if row < ROW_COUNT and column < COLUMN_COUNT:
        for r in range(row + 1):
            if grid[r][column] == 0 and turn % 2 == 1:
                grid[r][column] = 1
                break
            elif grid[r][column] == 0 and turn % 2 == 0:
                grid[r][column] = 2
                break
        turn += 1
        if winning_move(grid[r][column]):
            game_over = True


def setup():
    global game_over
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_mouse_press = on_mouse_press

    arcade.run()

    if game_over:
        arcade.finish_render()


if __name__ == '__main__':
    setup()