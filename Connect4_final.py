"""
------------------------------------------------------------------------------------------------------------------------
Name:		Connect4_final.py
Purpose:
Develop a program that first outputs a menu to give the user a choice to play a single or two player connect 4 game and
then creates the chosen game until finally detecting and announcing a winner.

Author:		Ohri. A

Created:    11/06/2019
------------------------------------------------------------------------------------------------------------------------
"""

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
SCREEN_TITLE = "Connect 4 Game"

# Set dimensions for uploaded texure/logo
texture = arcade.load_texture("logo.jpeg")
scale = 0.120
texture_width = texture.width * scale
texture_height = texture.height * scale

# Set starting y point for animated pieces in menu and centre point for text and other features
y_start = SCREEN_HEIGHT
centre_x = SCREEN_WIDTH // 2

# Assign the states/modes the game can be in
MENU = 0
ONE_PLAYER = 1
TWO_PLAYER = 2

# Assign player and AI to different values for single player mode
player = 1
AI = 2

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


def computer_move(col):
    global grid, turn

    # Drop computer/AI piece to lowest available slot given a random column
    for row in range(ROW_COUNT):
        if grid[row][col] == 0 and turn % 2 == 0:
            grid[row][col] = AI
            break

    # Play disc dropping in frame sound
    play_sound("game_connect_4_playing_disc_place_in_frame_1.wav")

    # Increment turn by 1or 2 depending on which player's turn
    turn += 1


def draw_menu():
    # Draw texture/Connect 4 logo
    arcade.draw_texture_rectangle(centre_x, SCREEN_HEIGHT - 75, texture_width, texture_height, texture, 0)

    # Draw buttons for single and two player modes
    arcade.draw_rectangle_filled(centre_x, 135, texture_width, 50, arcade.color.BLUE)
    arcade.draw_text("Single Player", centre_x - texture_width // 2, 125, arcade.color.WHITE, 18,
                     width=texture_width, align="center")
    arcade.draw_rectangle_filled(centre_x, 50, texture_width, 50, arcade.color.BLUE)
    arcade.draw_text("Two Player", centre_x - texture_width // 2, 40, arcade.color.WHITE, 18,
                     width=texture_width, align="center")

    # Draw animated pieces
    arcade.draw_circle_filled(30, y_start, 25, arcade.color.RED)
    arcade.draw_circle_filled(SCREEN_WIDTH - 30, y_start, 25, arcade.color.YELLOW)


def draw_board():
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


def draw_text(turn_prompt_1, turn_prompt_2, winner_message_1, winner_message_2):
    # Output the user prompt to move determined by the turn number
    if not game_over and turn % 2 == 1:
        arcade.draw_text(turn_prompt_1, centre_x - 150, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 18, width=300, align="center")
    elif not game_over and turn % 2 == 0:
        arcade.draw_text(turn_prompt_2, centre_x - 200, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 18, width=400, align="center")
    # Output the winner determined by the turn number
    elif game_over and turn % 2 == 0:
        arcade.draw_text(winner_message_1, centre_x - 100, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 24, width=200, align="center")
    else:
        arcade.draw_text(winner_message_2, centre_x - 150, SCREEN_HEIGHT -
                         TEXT_HEIGHT + 10, arcade.color.WHITE, 24, width=300, align="center")


def play_sound(file_path: str):
    # Load and play sound effect
    try:
        sound_effect = arcade.load_sound(file_path)
        arcade.play_sound(sound_effect)
    except:
        print("Unable to play sound.")

def on_update(delta_time):
    global y_start
    # Animate pieces on menu screen
    y_start -= 1
    # Once the pieces cross the bottom of the screen, bring them back up to the top, forming a cycle
    if (y_start + 25) <= 0:
        y_start = SCREEN_HEIGHT


def on_draw():
    # Draw everything in all 3 states of the game
    arcade.start_render()

    if current_state == MENU:
        # Draw menu
        draw_menu()
    else:
        # Draw game board
        draw_board()
        # Output user prompts/messages based on the game mode
        if current_state == TWO_PLAYER:
            draw_text("Player 1/Red, move!", "Player 2/Yellow, move!", "Red wins!", "Yellow wins!")
        else:
            draw_text("Player 1/Red, move!", "Computer's move.", "You win!", "You lost.")


def on_mouse_press(x, y, button, modifiers):
    global turn, game_over, current_state

    # Determine which button is pressed in the menu to advance to that game mode
    if current_state == MENU:
        if (x > (centre_x - (texture_width // 2)) and x < (centre_x + (texture_width // 2))
            and y > (135 - (50//2)) and y < (135 + (50//2))):
            current_state = ONE_PLAYER
        elif (x > (centre_x - (texture_width // 2)) and x < (centre_x + (texture_width // 2))
            and y > (50 - (50//2)) and y < (50 + (50//2))):
            current_state = TWO_PLAYER

    # Connect 4 game modes
    else:
        # Convert the x, y screen coordinates to grid coordinates
        column = x // WIDTH
        row = y // HEIGHT

        # Ensure the user clicks within the grid on an empty slot and there's no winner yet
        if row < ROW_COUNT and column < COLUMN_COUNT and not game_over and grid[row][column] == 0:
            # Two player game mode
            if current_state == TWO_PLAYER:
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
                    play_sound("zapsplat_multimedia_male_voice_processed_says_winner_001_21568.wav")

            # Single player mode
            else:
                # Drop piece in lowest available row in a given column
                for r in range(row + 1):
                    # Flip the grid location from 0 to 1 for human player
                    if grid[r][column] == 0 and turn % 2 == 1:
                        grid[r][column] = player
                        break

                # Play sound of piece dropping in slot
                play_sound("game_connect_4_playing_disc_place_in_frame_1.wav")

                # Increment the turn number by 1 after every click/move
                turn += 1

                # Check if human player has won
                if winning_move(player):
                    game_over = True
                    play_sound("zapsplat_multimedia_male_voice_processed_says_winner_001_21568.wav")

                # If not make a computer move after selecting a random column
                if not game_over:
                    col = random.randint(0, COLUMN_COUNT - 1)
                    computer_move(col)

                # If a winner is detected set game_over to True to disable any more clicks/moves
                if winning_move(AI):
                    game_over = True


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