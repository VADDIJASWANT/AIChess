import pygame
from pygame.locals import *
from board import Board

#initialize pygame
pygame.init()

# set up screen 
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

#button details
BUTTON_WIDTH,BUTTON_HEIGHT = 200,50
button_font = pygame.font.Font(None, 36)

#create buttons
singleplayer_button = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, SCREEN_HEIGHT/2 - BUTTON_HEIGHT/2 - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
multiplayer_button = pygame.Rect(SCREEN_WIDTH/2 - BUTTON_WIDTH/2, SCREEN_HEIGHT/2, BUTTON_WIDTH, BUTTON_HEIGHT)

#flag the game mode
game_mode_selected = False
game_mode = "singleplayer"#default 

#board variable in global scope
board = None

running= True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:                
                if board is None and singleplayer_button.collidepoint(event.pos):
                    game_mode_selected = True
                    game_mode = "singleplayer"
                elif board is None and multiplayer_button.collidepoint(event.pos):
                    game_mode_selected = True
                    game_mode = "Multiplayer"
                else:
                    if board:
                        board.handle_click(event.pos)

    if not game_mode_selected:
        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, singleplayer_button)
        pygame.draw.rect(screen, GRAY, multiplayer_button)
        #creating text element for buttons
        single_player_text = button_font.render("Single Player", True, WHITE)
        multi_player_text = button_font.render("Multi Player", True, WHITE)
        #adding text element to the buttons on screen
        screen.blit(single_player_text, (singleplayer_button.x + 30, singleplayer_button.y + 12))
        screen.blit(multi_player_text, (multiplayer_button.x + 30, multiplayer_button.y + 12))
    else:
        if board is None:
            board = Board(screen)
            board.draw()
    
    #update the display
    pygame.display.update()
pygame.quit()