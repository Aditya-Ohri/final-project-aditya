import arcade
import random

# Set the number of columns and rows for the board
ROW_COUNT = 6
COLUMN_COUNT = 7

# Set the dimensions of each grid location on the board
WIDTH = 50
HEIGHT = 50
RADIUS = 23

# Set the dimensions of the header text
TEXT_HEIGHT = 50

# Compute the Screen's dimensions and set the title
SCREEN_WIDTH = WIDTH * COLUMN_COUNT
SCREEN_HEIGHT = HEIGHT * ROW_COUNT + TEXT_HEIGHT
SCREEN_TITLE = "Connect 4 Two-player Game"

# Assign the states/modes the game can be in
MENU = 0
TWO_PLAYER = 1
ONE_PLAYER = 2

# Generate 2-D grid filled with 0's to represent empty slots
grid = [[0 for column in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]

# Set variables to initialize game
turn = 1
game_over = False
current_state = MENU


def winning_move(piece: int):
    # Check horizontal for four in a row
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (grid[r][c] == piece and grid[r][c + 1] == piece
            and grid[r][c + 2] == piece and grid[r][c + 3] == piece):
                return True

    # Check vertical for four in a row
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if (grid[r][c] == piece and grid[r + 1][c] == piece
            and grid[r + 2][c] == piece and grid[r + 3][c] == piece):
                return True

    # Check positively sloping diagonal for four in a row
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if (grid[r][c] == piece and grid[r + 1][c + 1] == piece
            and grid[r + 2][c + 2] == piece and grid[r + 3][c + 3] == piece):
                return True

    # Check negatively sloping diagonal for four in a row
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (grid[r][c] == piece and grid[r - 1][c + 1] == piece
            and grid[r - 2][c + 2] == piece and grid[r - 3][c + 3] == piece):
                return True


def play_sound(file_path: str):
    sound_effect = arcade.load_sound(file_path)
    arcade.play_sound(sound_effect)


def on_update(delta_time):
    pass


def on_draw():
    arcade.start_render()
    if current_state == MENU:
        texture = arcade.load_texture("logo.jpeg")
        scale = 0.120
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 75, texture.width*scale, texture.height
                                      *scale, texture, 0)
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 135, texture.width*scale, 50, arcade.color.BLUE)
        arcade.draw_text("Single Player", SCREEN_WIDTH // 2 - texture.width*scale // 2, 125, arcade.color.WHITE, 18,
                         width=texture.width*scale, align="center")
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 50, texture.width*scale, 50, arcade.color.BLUE)
        arcade.draw_text("Two Player", SCREEN_WIDTH // 2 - texture.width * scale // 2, 40, arcade.color.WHITE, 18,
                         width=texture.width * scale, align="center")
        arcade.draw_circle_filled(30, SCREEN_HEIGHT - 30, 25, arcade.color.RED)
        arcade.draw_circle_filled(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30, 25, arcade.color.YELLOW)
    else:
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

        # Output the user prompt to move determined by the turn number
        if not game_over and turn % 2 == 1:
            arcade.draw_text("Player 1/Red, move!", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 18, width=300, align="center")
        elif not game_over and turn % 2 == 0:
            arcade.draw_text("Player 2/Yellow, move!", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 18, width=400, align="center")
        # Output the winner determined by the turn number
        elif game_over and turn % 2 == 0:
            arcade.draw_text("Red wins!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 24, width=200, align="center")
        else:
            arcade.draw_text("Yellow wins!", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 24, width=300, align="center")


def on_mouse_press(x, y, button, modifiers):
    global turn
    global game_over

    # Convert the x, y screen coordinates to grid coordinates
    column = x // WIDTH
    row = y // HEIGHT

    # Ensure the user clicks within the grid on an empty slot and there's no winner yet
    if row < ROW_COUNT and column < COLUMN_COUNT and not game_over and grid[row][column] == 0:
        # Drop piece in lowest available row in a given column
        for r in range(row + 1):
            # Flip the grid location from 0 to 1 or 2 depending on which player's turn
            if grid[r][column] == 0 and turn % 2 == 1:
                grid[r][column] = 1
                break
            elif grid[r][column] == 0 and turn % 2 == 0:
                grid[r][column] = 2
                break

        # Play sound of piece dropping in slot
        play_sound("game_connect_4_playing_disc_place_in_frame_1.wav")

        # Increment the turn number by 1 after every click/move
        turn += 1

        # If a winner is detected set game_over to True to disable any more clicks/moves
        if winning_move(grid[r][column]):
            game_over = True

    '''
    if game_over:
        play_sound("zapsplat_multimedia_male_voice_processed_says_winner_001_21568.wav")
    '''
def setup():
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_mouse_press = on_mouse_press
    window.on_update = on_update

    arcade.run()


if __name__ == '__main__':
    setup()
