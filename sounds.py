
#copyright 2026 Gyslain Babineau part of this code is from thepythoncode.com with some modifications to make it more efficient and more for myself to learn how to code in python and make games.
#Use of this code is for educational purposes only and not for commercial use.


# Author: Gyslain Babineau
# Course: SMC 204 Python 
# Lab: Python Final Project
# Date: 2025-03-18
# Description: This is a Tetris game is my own version on the classic tetris game and added a high score system, a start screen and a upcoming piece display and also added a pause function and a game over screen and also added some sound effects to make it more fun to play and also to make it more enjoyable for the player and also to make it more visually appealing and to make it more fun for the player to play the game. I learned a lot during this process and I hope you enjoy playing the game as much as I enjoyed making it.






import sys
import time
from tkinter import messagebox

try:
    import pygame

except ModuleNotFoundError as vError:

    messagebox.showerror("Import Error", "Pygame module not found. Please install it using 'py -m pip install pygame-ce' and try again.")
    sys.exit(1)

pygame.init()
pygame.mixer.init()
pygame.time.delay(3000)  # Delay to ensure mixer is initialized properly


# Initialize the mixer
try:
    if not pygame.mixer.get_init():
        pygame.mixer.init()
except Exception as verror:
    print(f"Error initializing mixer: {verror}")
if not pygame.mixer.get_init():
    pygame.mixer.init()

pygame.mixer.music.load('VERT_tetris.mp3')  
pygame.mixer.music.play(-1)  # Start playing the music, -1 means loop indefinitely

# Set the volume (optional, value from 0.0 to 1.0)
pygame.mixer.music.set_volume(0.5)  # Adjust the volume

