
#copyright 2026 Gyslain Babineau part of this code is from thepythoncode.com with some modifications to make it more efficient and more for myself to learn how to code in python and make games.
#Use of this code is for educational purposes only and not for commercial use.


# Author: Gyslain Babineau
# Course: SMC 204 Python 
# Lab: Python Final Project
# Date: 2025-03-18
# Description: This is a Tetris game is my own version on the classic tetris game and added a high score system, a start screen and a upcoming piece display and also added a pause function and a game over screen and also added some sound effects to make it more fun to play and also to make it more enjoyable for the player and also to make it more visually appealing and to make it more fun for the player to play the game. I learned a lot during this process and I hope you enjoy playing the game as much as I enjoyed making it.






# This code manages the high score for the Tetris game. It provides functions to load and save the high score from a file. The high score is stored in a JSON file named 'high_score.json'.

import json


vhigh_score_file = 'high_score.json'

def fload_high_score():
    try:
        with open(vhigh_score_file, 'r') as vfile:
            return json.load(vfile)
    except (FileNotFoundError, ValueError):
        return 0

def fsave_high_score(pscore):
    try:
        with open(vhigh_score_file, 'w') as vfile:
            json.dump(pscore, vfile)
    except IOError:
        pass

