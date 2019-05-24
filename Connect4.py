import arcade

# Set the number of columns and rows for the board
ROW_COUNT = 6
COLUMN_COUNT = 7

# Set the dimensions of each grid location on the board
WIDTH = 50
HEIGHT = 50

# Set the dimensions of the header text
TEXT_HEIGHT = 50

# Compute the Screen's dimensions and set the name
SCREEN_WIDTH = WIDTH * COLUMN_COUNT
SCREEN_HEIGHT = HEIGHT * ROW_COUNT + TEXT_HEIGHT
SCREEN_TITLE = "Connect 4 Game"

# Generate empty grid
grid = [[0 for i in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]

def on_update(delta_time):
    pass

def on_draw():
    arcade.start_render()
    # Draw the game board
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            # Compute the centre coordinates for each grid location
            x = WIDTH * column + WIDTH // 2
            y = HEIGHT * row + HEIGHT // 2

            # Draw each grid location as a slot on the Connect 4 board
            arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, arcade.color.BLUE)
            arcade.draw_circle_filled(x, y, WIDTH // 2.2, arcade.color.BLACK)

def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass

def on_mouse_press(x, y, button, modifiers):
    pass

def setup():
    global grid

    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Array Backed Grids")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw

    arcade.run()


if __name__ == '__main__':
    setup()