import time 
import pygame
import random
import json
from Button import Button
from screen import Screen
import constant as const
from state import State

# init game
pygame.init()
fullscreen = (const.SCREEN_WIDTH,const.SCREEN_HEIGHT)
screen = pygame.display.set_mode(fullscreen, pygame.NOFRAME)
clock = pygame.time.Clock()
# game data
f = open('sequences.json')
sequences = json.load(f)

        
sequence = [180,270,180,90]
seq = [3,2,4,1]
antworten = [0,1,3,2]

# load images
start_bg = pygame.image.load("assets/START.png")
question_bg = pygame.image.load("assets/FRAGE.png")
winning_bg = pygame.image.load("assets/GEWONNEN.png")


start_screen = pygame.Surface(fullscreen)
start_screen.blit(start_bg,(0,0))
question_screen = pygame.Surface(fullscreen)
question_screen.blit(question_bg,(0,0))

winning_screen = pygame.Surface(fullscreen)
winning_screen.blit(winning_bg,(0,0))

current_state = State.START
current_index = 0
current_display = start_screen
current_seq = seq[current_index]


start_btn = Button(262, 200, 500, 200)
answer_btns = []
winning_btns = []

def reset():
    global current_display
    global current_state
    global current_index
    current_display = start_screen
    current_state = State.START
    current_index = 0

for i in range(4):
    answer_btns.append(Button(const.ANSWER_BTN_STARTX,const.ANSWER_BTN_STARTY+(i*const.ANSWER_BTN_GAP),const.ANSWER_BTN_WIDTH, const.ANSWER_BTN_HEIGHT,i))

for i in range(2):
    winning_btns.append(Button(312,194+(i*133), 400, 80,i))

def checkButtons(mouse):
    global current_state
    global current_display
    match current_state:
        case State.START:
            if start_btn.clicked(mouse[0], mouse[1]):
                current_display = question_screen
                current_state = State.QUESTION
        case State.QUESTION:
            for btn in answer_btns:
                if btn.clicked(mouse[0], mouse[1]):
                    checkAnswer(btn.getID())
                    break
        case State.WINNING:
            if current_index <= 3:
                for btn in winning_btns:
                    if btn.clicked(mouse[0], mouse[1]):
                        if btn.getID() == 0:
                            current_display = question_screen
                            current_state = State.QUESTION
                        if btn.getID() == 1:
                            reset()
                        break
            else: 
                reset()

def checkAnswer(id):
      global antworten
      global current_index
      global current_display
      global current_state
      global start_time
      if id == antworten[current_index]:
          current_display = winning_screen
          current_state = State.WINNING
          current_index += 1  



running = True
while running:
    screen.blit(current_display, (0,0))
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            checkButtons(mouse)
    
    pygame.display.flip()
    clock.tick(60)