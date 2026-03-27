
#copyright 2026 Gyslain Babineau part of this code is from thepythoncode.com with some modifications to make it more efficient and more for myself to learn how to code in python and make games.
#Use of this code is for educational purposes only and not for commercial use.


# Author: Gyslain Babineau
# Course: SMC 204 Python 
# Lab: Python Final Project
# Date: 2025-03-18
# Description: This is a Tetris game is my own version on the classic tetris game and added a high score system, a start screen and a upcoming piece display and also added a pause function and a game over screen and also added some sound effects to make it more fun to play and also to make it more enjoyable for the player and also to make it more visually appealing and to make it more fun for the player to play the game. I learned a lot during this process and I hope you enjoy playing the game as much as I enjoyed making it.



#all comments are added to the top of every comment boxes.



import random
import sys
from tkinter import messagebox
import sounds
import topscore



try:
    import pygame

except ModuleNotFoundError as vError:

    messagebox.showerror("Import Error", "Pygame module not found. Please install it using 'py -m pip install pygame-ce' and try again.")



################################################################################
# Ensure the sounds module is imported and initialized
    try:
        sounds
    except Exception as vError:
        print(f"Error importing sounds module: {vError}")
        sys.exit()
################################################################################

pygame.init()


# Set up the display
cCELL_SIZE = 42
cCOLS = 12
cROWS = 20
WIDTH = cCELL_SIZE * cCOLS
HEIGHT = cCELL_SIZE * cROWS


vscreen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gyslain-Tetris-Game")# Set the window title
pygame.display.set_icon(pygame.image.load('tetris_icon.jpg'))  # Set the window icon

vclock = pygame.time.Clock()
FPS = 60

cBACKGROUND = (50, 50, 50) # Dark gray background color for grid and game area
# Colors
cGRID_COLOR = (0, 0, 0)
cWHITE = (255, 255, 255)
cBLACK = (0, 0, 0)
cRED = (255, 0, 0)
cBLUE = (0, 0, 255)
cGREEN = (0, 255, 0)
cYELLOW = (255, 255, 0)
cCOLORS = [cRED, cBLUE, cGREEN, cYELLOW]
cMAGENTA = (255, 0, 255)


########################################################################################

#had to change learn how the tetrominoes are represented and change it cause the original code they were 3 times bigger and found out that for every piece there base on a 2x3 grid and the I piece is based on a 1x4 grid so I had to change the way they are represented to make it more efficient and easier to understand for myself and for others who want to learn how to code in python and make games. I learned alot during this process.

# Define the shapes of the tetrominoes

SHAPES = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]], 
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 1, 0], [0, 1, 1]]   
]



########################################################################################################################################

#this part was to fix the grid because on the original part of the code the left side had no wall and while i learned to fix it i also learned I could make a grid style game and I could also make it more efficient and easier to understand for myself and for others who want to learn how to code in python and make games.

class cTetromino:
    def __init__(pself, x, y, pshape, pcolor):
        try:
            pself.x = x
            pself.y = y
            pself.shape = pshape
            pself.color = pcolor
        except Exception as vError:
            print(f"Error initializing tetromino: {vError}")

    def fdraw(self):
        try:
            for row_idx, row in enumerate(self.shape):
                for col_idx, val in enumerate(row):
                    if val:
                        pygame.draw.rect(vscreen, self.color, ((self.x + col_idx) * cCELL_SIZE, (self.y + row_idx) * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE))
                        pygame.draw.rect(vscreen, cGRID_COLOR, ((self.x + col_idx) * cCELL_SIZE, (self.y + row_idx) * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE), 1)
        except Exception as vError:
            print(f"Error drawing tetromino: {vError}")


def fcreate_grid():
    try:
        return [[0 for _ in range(cCOLS)] for _ in range(cROWS)]
    except Exception as vError:
        print(f"Error creating grid: {vError}")
        return [[0 for _ in range(cCOLS)] for _ in range(cROWS)]
    

###############################################################################################################################################

def fdraw_text(ptext, pfont, pcolor, psurface, px, py):
    try:
        vtext_obj = pfont.render(ptext, True, pcolor)
        vtext_rect = vtext_obj.get_rect(center=(px, py))
        psurface.blit(vtext_obj, vtext_rect)
    except Exception as vError:
        print(f"Error drawing text: {vError}")

def fdraw_grid(pgrid):
    try:
        for y in range(cROWS):
            for x in range(cCOLS):
                color = pgrid[y][x] if pgrid[y][x] else cGRID_COLOR
                pygame.draw.rect(vscreen, color, (x * cCELL_SIZE, y * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE))
                pygame.draw.rect(vscreen, cBACKGROUND, (x * cCELL_SIZE, y * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE), 1)
    except Exception as vError:
        print(f"Error drawing grid: {vError}")

def fclear_lines(pgrid):
    try:
        vnew_grid = [row for row in pgrid if any(cell == 0 for cell in row)]
        vcleared = cROWS - len(vnew_grid)
        for _ in range(vcleared):
            vnew_grid.insert(0, [0 for _ in range(cCOLS)])
        return vnew_grid, vcleared
    except Exception as vError:
        print(f"Error clearing lines: {vError}")
        return pgrid, 0

def flock_piece(ptetromino, pgrid):
    try:
        for vrow_idx, row in enumerate(ptetromino.shape):
            for vcol_idx, val in enumerate(row):
                if val:
                    vnew_x = ptetromino.x + vcol_idx
                    vnew_y = ptetromino.y + vrow_idx
                    if 0 <= vnew_y < cROWS and 0 <= vnew_x < cCOLS:
                        pgrid[vnew_y][vnew_x] = ptetromino.color
    except Exception as vError:
        print(f"Error locking piece: {vError}")

def fcheck_collision(ptetromino, pgrid):
    try:
        for vrow_idx, row in enumerate(ptetromino.shape):
            for vcol_idx, val in enumerate(row):
                if val:
                    vnew_x = ptetromino.x + vcol_idx
                    vnew_y = ptetromino.y + vrow_idx
                    if vnew_x < 0 or vnew_x >= cCOLS or vnew_y < 0 or vnew_y >= cROWS:
                        return True
                    if vnew_y >= 0 and pgrid[vnew_y][vnew_x]:
                        return True
    except Exception as vError:
        print(f"Error checking collision: {vError}")
    return False


def fcalculate_score(pcleared_lines):
    try:
        return [0, 100, 300, 500, 800][pcleared_lines] if 0 <= pcleared_lines <= 4 else 0
    except Exception as vError:
        print(f"Error calculating score: {vError}")
        return 0

def fgame_over(pgrid):
    try:
        return any(pgrid[0][x] for x in range(cCOLS))
    except Exception as vError:
        print(f"Error checking game over: {vError}")
        return False

def fdraw_game_over(psurface, px, py):
    try:
        vgame_over_font = pygame.font.SysFont('Arial', 56, bold=True)
        vgame_over_text = vgame_over_font.render('GAME OVER', True, cMAGENTA)
        psurface.blit(vgame_over_text, (px, py))
    except Exception as vError:
        print(f"Error drawing game over: {vError}")

########################################################################################################################################################

#I added a function to display the upcoming tetromino in the top right corner of the screen and to show the text "Next Piece:" above it and to make it more efficient and easier to understand for myself and for others who want to learn how to code in python and make games.

def fupcoming_tetromino(vsurface, ptetromino):
    try:
        vfont = pygame.font.SysFont('Arial', 25, bold=False)
        vtext = vfont.render('Next Piece:', True, cWHITE)
        vsurface.blit(vtext, (WIDTH - 135, 10))
    except Exception as vError:
        print(f"Error displaying upcoming tetromino: {vError}")
    try:
        for row_idx, row in enumerate(ptetromino.shape):
            for col_idx, val in enumerate(row):
                if val:
                    pygame.draw.rect(vsurface, ptetromino.color, (WIDTH - 175 + col_idx * cCELL_SIZE, 50 + row_idx * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE))
                    pygame.draw.rect(vsurface, cGRID_COLOR, (WIDTH - 175 + col_idx * cCELL_SIZE, 50 + row_idx * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE), 1)
                elif val == 0:
                    pygame.draw.rect(vsurface, cBACKGROUND, (WIDTH - 175 + col_idx * cCELL_SIZE, 50 + row_idx * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE))
                    pygame.draw.rect(vsurface, cGRID_COLOR, (WIDTH - 175 + col_idx * cCELL_SIZE, 50 + row_idx * cCELL_SIZE, cCELL_SIZE, cCELL_SIZE), 1)
    except Exception as vError:
        print(f"Error drawing upcoming tetromino: {vError}")

###########################################################################################################################################################

def fget_next_piece():
    try:
        return cTetromino(4, 0, random.choice(SHAPES), random.choice(cCOLORS))
    except Exception as vError:
        print(f"Error getting next piece: {vError}")
        return None

def fpause_game():
    try:
        paused = True
        font = pygame.font.SysFont('Arial', 25, bold=True)
        pause_text = font.render('Game Paused. Press P to Resume.', True, cMAGENTA)
        vscreen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
        pygame.display.update()
    except Exception as vError:
        print(f"Error pausing game: {vError}")
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        else:
            pygame.mixer.music.stop() # Stop the music when the game is paused
            pygame.mixer.music.play(-1)  # Restart the music when the game is resumed

#######################################################################################################################################################################

#made a start screen function to show the start screen before the game starts and to show the instructions on how to play the game and also to make it easier for the player to see the instructions before playing the game.

def fstart_screen():
    try:
        vfont_large = pygame.font.SysFont('Arial', 36, bold=True)
        vfont_small = pygame.font.SysFont('Arial', 36, bold=True)
        vmenu_active = True
        pygame.mixer.music.stop()  # Stop the music on the start screen
    except Exception as vError:
        print(f"Error initializing start screen: {vError}")

    
    while vmenu_active:
        vscreen.fill(cBLACK)
        dysplay_image = pygame.image.load('tetris_main.jpg')  #This Loads the image I chose for the start screen and to make it more visually appealing and to make it more fun for the player to see the image before playing the game.
        vscreen.blit(dysplay_image, (WIDTH // 2 - dysplay_image.get_width() // 2, HEIGHT // 10 - dysplay_image.get_height() // 10))
        fdraw_text('Gyslain Tetris Game', vfont_large, cWHITE, vscreen, WIDTH // 2, HEIGHT // 2.5)
        fdraw_text('Press SPACE to Start', vfont_small, cWHITE, vscreen, WIDTH // 2, HEIGHT // 2)
        fdraw_text('Press ESC to Quit', vfont_small, cWHITE, vscreen, WIDTH // 2, HEIGHT // 1.7)
        fdraw_text('Use Arrow Keys to Move', vfont_small, cWHITE, vscreen, WIDTH // 2, HEIGHT // 1.5)
        fdraw_text('Press P to Pause', vfont_small, cWHITE, vscreen, WIDTH // 2, HEIGHT // 1.3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    vmenu_active = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


#################################################################################################################################################################################################

def main():
    try:
        fstart_screen()  # Show the start screen before starting the game
    except Exception as vError:
        print(f"Error starting game: {vError}")
    vrunning = True
    vcurrent = cTetromino(4, 0, random.choice(SHAPES), random.choice(cCOLORS))
    vgrid = fcreate_grid()
    vfall_speed = 500 #milliseconds
    vlast_fall_time = pygame.time.get_ticks()
    vscore = 0
    vlines_cleared_total = 0
    vLevel = 1
    vfont = pygame.font.SysFont('Arial', 25, bold=True)
    vgame_over_flag = False
    vnext_piece = fget_next_piece()  # Get the next piece at the start of the game

###########################################################################################################################################################

#this part makes it that each level the pieces fall faster and also to make it more challenging for the player as they progress through the levels and to make it more fun.

    while vrunning:
        try:
            current_time = pygame.time.get_ticks()
            if current_time - vlast_fall_time > vfall_speed:
                vcurrent.y += 1
                if fcheck_collision(vcurrent, vgrid):
                    vcurrent.y -= 1
                    flock_piece(vcurrent, vgrid)
                    vgrid, cleared = fclear_lines(vgrid)
                    if cleared > 0:
                        vscore += fcalculate_score(cleared)
                        vlines_cleared_total += cleared
                        if vlines_cleared_total >= vLevel * 10:
                            vLevel += 1
                            vfall_speed = max(100, 500 - (vLevel - 1) * 35) # Increase speed with level            
                    vcurrent = vnext_piece
                    vnext_piece = fget_next_piece()
                    fupcoming_tetromino(vscreen, vnext_piece)  # Update the upcoming piece display
                    if fgame_over(vgrid):
                        vgame_over_flag = True
                vlast_fall_time = current_time
        except Exception as vError:
            print(f"Error in game loop: {vError}")

#############################################################################################################################################################

#this is the modified high score system because when i added the grid it broke most of my code so i had to change the way the high score is displayed and also to make it more efficient and easier to understand for myself and for others who want to learn how to code in python and make games.        

        vhigh_score = topscore.fload_high_score()    # Load the high score at the beginning of the game
        if vscore > vhigh_score:
            topscore.fsave_high_score(vscore)



##########################################################################################################################

        vscreen.fill(cBACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vrunning = False
            elif event.type == pygame.KEYDOWN:
                if vgame_over_flag:
                    # Restart the game
                    return main()
                if event.key == pygame.K_LEFT:
                    vcurrent.x -= 1
                    if fcheck_collision(vcurrent, vgrid): vcurrent.x += 1
                elif event.key == pygame.K_RIGHT:
                    vcurrent.x += 1
                    if fcheck_collision(vcurrent, vgrid): vcurrent.x -= 1
                elif event.key == pygame.K_DOWN:
                    vcurrent.y += 1
                    if fcheck_collision(vcurrent, vgrid): vcurrent.y -= 1
                elif event.key == pygame.K_UP:
                    vcurrent.shape = [list(row) for row in zip(*vcurrent.shape[::-1])]
                    if fcheck_collision(vcurrent, vgrid):
                        vcurrent.shape = [list(row) for row in zip(*vcurrent.shape)][::-1]
                elif event.key == pygame.K_SPACE:
                    while not fcheck_collision(vcurrent, vgrid):
                        vcurrent.y += 1
                    vcurrent.y -= 1
                elif event.key == pygame.K_ESCAPE:
                    vrunning = False
                elif event.key == pygame.K_p:
                    fpause_game()
                

######################################################################################################################################################################################################

#this part is how all the text is displayed on the screen and also to show the score, level, and high score on the screen and to make it more efficient and easier to understand for myself and for others who want to learn how to code in python and make games.Its also easier to change to location on screen of were everything is like if i want i can change the top score to be on the left just by changing the vscreen.blit(topscore_text, (130, 10)) numbers that are inside.


        fdraw_grid(vgrid)
        vcurrent.fdraw()
        score_text = vfont.render(f'Score: {vscore}', True, (255, 255, 255))
        level_text = vfont.render(f'Level: {vLevel}', True, (255, 255, 255))
        topscore_text = vfont.render(f'High Score: {vhigh_score}', True, (255, 255, 0))
        vscreen.blit(score_text, (10, 10))
        vscreen.blit(level_text, (12, 50))
        vscreen.blit(topscore_text, (150, 10))
        fupcoming_tetromino(vscreen, vnext_piece)  # Show the upcoming piece in the top right corner of the screen
    
########################################################################################################################

#This is the modified gameover screen because when i added the grid it broke most of my code so i had to change the way the gameover screen is displayed and also to make it more efficient and easier to understand for myself and for others who want to learn how to code in python and make games.

        try:
             if vgame_over_flag:
                fdraw_game_over(vscreen, WIDTH // 2 - 150, HEIGHT // 2 - 30)
                pause_text = vfont.render('Press any key to restart', True, cMAGENTA)
                vscreen.blit(pause_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        except Exception as vError:
            print(f"Error displaying game over screen: {vError}")
        if vgame_over_flag:
            # Draw the "Game Over" message
            fdraw_game_over(vscreen, WIDTH // 2 - 150, HEIGHT // 2 - 30)
            pause_text = vfont.render('Press any key to restart', True, cMAGENTA)
            vscreen.blit(pause_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        if vgame_over_flag:  # Stop the music when the game is over
            pygame.mixer.music.stop()
        if not vgame_over_flag and not pygame.mixer.music.get_busy():  # Restart music if it stopped and game is not over
            pygame.mixer.music.play(-1)


########################################################################################

        pygame.display.update()
        vclock.tick(FPS)



if __name__ == "__main__":
    main()

pygame.quit()

