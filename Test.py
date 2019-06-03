import arcade

def play_sound(file_path: str):
    sound_effect = arcade.load_sound(file_path)
    arcade.play_sound(sound_effect)

play_sound("/home/robuntu/Downloads/game_connect_4_playing_disc_place_in_frame_1.wav")

# Winning sound not loading