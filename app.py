# Load and initialize Modules here
import pygame
import time
import constant as const
from state import State
from functools import partial
import random
import json
import copy
# import board
# import Adafruit_ADS1x15
# import RPi.GPIO as GPIO
# from adafruit_motor import stepper
# from adafruit_motorkit import MotorKit


pygame.init()
fullscreen = (const.SCREEN_WIDTH,const.SCREEN_HEIGHT)
window = pygame.display.set_mode(fullscreen, pygame.NOFRAME)

# adc = Adafruit_ADS1x15.ADS1115()
# kit = MotorKit(i2c=board.I2C())
# kit.stepper1.release()
# kit.stepper2.release()

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GAIN = 1
# Digital_PIN = 23
# Time_Delay = 0.05
# GPIO.setup(Digital_PIN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

# def drive(deg):
#     steps = round(deg/1.8)
#     for i in range(steps):
#         kit.stepper1.onestep()
#         time.sleep(0.02)
#     kit.stepper1.release()

# def drive2(deg):
#     steps = round(deg/1.8)
#     for i in range(steps):
#         kit.stepper2.onestep()
#         time.sleep(0.02)
#     kit.stepper2.release()

# def homeCube():
#     while True:
#         value = adc.read_adc(0, gain=GAIN)
#         if value <= 1000:
#             kit.stepper1.release()
#             break
#         kit.stepper1.onestep()
#         time.sleep(0.02)
#     kit.stepper1.release()

# 1=laser, 2=stanze, 3=biegen, 4=am

# JSON Settings
sequences = json.load(open("sequences.json", encoding='utf-8'))

sequence = sequences["sequences"][0]["grad"]
seq = sequences["sequences"][0]["bereich"]
antwort_text = sequences["antwort_text"]
antwort_index = sequences["sequences"][0]["antwort_index"]

antwort_moeglich = sequences["antwort_moeglich"]
antwort_moeglich_index = sequences["sequences"][0]["antwort_moeglich_index"]
# JSON Settings


# assets and bg
start_bg = pygame.image.load("assets/START.png")
question_bg = pygame.image.load("assets/FRAGE.png")
winning_bg = pygame.image.load("assets/GEWONNEN.png")
end_bg = pygame.image.load("assets/END.png")
qr_bg = pygame.image.load("assets/end_bg/ABGESCHLOSSEN.png")

# info bilder
start_time = 0

## Button assets
start_btn_img = pygame.image.load("assets/start_btn/0.png")
end_btn_img = pygame.image.load("assets/end_btn/0.png")
reset_btn_img = pygame.image.load("assets/end_bg/0.png")

question_btn_img = []
solution_btn_img = []
info_img = []

# load question buttons
for i in range(4):
    tmp = pygame.image.load("assets/question_btns/"+str(i)+".png")
    tmp_info = pygame.image.load("assets/info_bg/"+str(i)+".png")
    question_btn_img.append(tmp)
    info_img.append(tmp_info)
    
# load solution buttons
for i in range(2):
    tmp = pygame.image.load("assets/solution_btns/"+str(i)+".png")
    solution_btn_img.append(tmp)

# Clock
windowclock = pygame.time.Clock()
global current_state 
global current_index


current_state = State.START
current_index = 0
current_answers = []
user_score = 0

def resetAll():
    global current_state
    global start_time
    global current_index
    global current_answers
    global user_score
    current_state = State.START
    current_index = 0
    start_time = 0
    user_score = 0
    generateRandomAns()
    # homeCube()

def checkRestart():
    global start_time
    if time.time() - start_time >= const.RESTART_TIME:
        resetAll()

# generates a text object
class Text(object):
    def __init__(self, text, fontsize, x, y, color,h_center=None,center=None):
        self.font = pygame.font.Font("assets/font/Roboto.ttf", fontsize)
        self.text = text
        self.color = color
        self.x = x
        self.h_center = h_center
        self.center = center
        self.y = y

    def draw(self, surf):
        text = self.font.render(self.text, True, self.color)
        if self.h_center != None: 
           rect = text.get_rect(center = (const.SCREEN_WIDTH // 2, 100))
           surf.blit(text, rect)
        elif self.center != None: 
            rect = text.get_rect(center = (const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT // 2))
            surf.blit(text, rect)
        else:
            surf.blit(text, (self.x, self.y))
    
    def setText(self, text):
        self.text = text
    
    def appendText(self,text):
        self.text += text
    
# generates a button object
class Button(object):
    def __init__(self, x,y, width, height,img, btn_id=None, action=None, text=None):
        self.x = x
        self.y = y
        self.img = img
        self.btn_id = btn_id
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        self.disable = False
        self.action = action
        self.text = text
        self.font = pygame.font.Font("assets/font/Roboto.ttf", 32)
        self.rendered_text = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)
    
    def clicked(self, mouse_x, mouse_y):
       return self.rect.collidepoint(mouse_x, mouse_y)
    
    def getID(self):
        return self.btn_id

    def changeText(self,text):
        self.text = text
        self.rendered_text = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, surf):
        surf.blit(self.img, (self.x, self.y))
        if self.text != None:
            surf.blit(self.rendered_text, self.text_rect)

    def handle_event(self):
        if self.action != None:
            self.action()

# generates a screen object
class Screen(object): 
    def __init__(self, width, height,surf, img):
        self.width  = width
        self.height = height
        self.surf = surf
        self.img = img
        self.btns = []
        self.text = []

    def addText(self,text):
        self.text.append(text)
    
    def changeText(self, index, text):
        self.text[index].setText(text)
    
    def appendText(self,index, text):
        self.text[index].appendText(text)
    
    def centerText(self, index):
        self.text[index]
    
    def addButton(self, btn):
        self.btns.append(btn)
    
    def changeButtonText(self, i, text):
        self.btns[i].changeText(text)

    def checkEvent(self, mouse_x, mouse_y):
        for b in self.btns:
            if  b.clicked(mouse_x, mouse_y):
                b.handle_event()
                return True
    
    def changeImage(self, img):
        self.img = img

    def draw(self):
        self.surf.blit(self.img, (0,0))
        for b in self.btns:
            b.draw(self.surf)
        for t in self.text:
            t.draw(self.surf)
        window.blit(self.surf, (0,0))

# switch states and screens
def switch(State):
    global current_state
    current_state = State

def generateRandomAns():
    global antwort_moeglich
    global antwort_moeglich_index
    global current_index
    global current_answers
    tmp = copy.deepcopy(antwort_moeglich)
    final = []
    correct_ans = tmp[antwort_moeglich_index[current_index]]
    del tmp[antwort_moeglich_index[current_index]]

    for i in range(3):
        element = random.choice(tmp)
        final.append(element)
        tmp.remove(element)
    final.insert(antwort_index[current_index],correct_ans)
    current_answers = copy.deepcopy(final)
    

def switchInfoScreen():
    global current_state
    global current_index
    current_index += 1
    if current_index == 4:
       switch(State.END)
    else:
        generateRandomAns()
        for i in range(4):
            question.changeButtonText(i, current_answers[i])
        switch(State.QUESTION)
        # drive(sequence[current_index])

def getPrize():
    switch(State.OUTPUT)
    global start_time
    start_time = time.time()
    # drive2(120)
    # gebe Fahrrad aus mit drive(deg)
    # time.sleep(10) # delay after click the btn


# start screen
start = Screen(1024, 600, pygame.Surface(fullscreen), start_bg)
start.addButton(Button(262, 200, 500, 200,start_btn_img, None, partial(switch, State.QUESTION)))

# winning screen
after_question = Screen(1024, 600, pygame.Surface(fullscreen), winning_bg)
after_question.addButton(Button(312, 194, 400, 80,solution_btn_img[0], None, partial(switch, State.INFO_PAGE)))
after_question.addButton(Button(312, 327, 400, 80,solution_btn_img[1], None, resetAll))
after_question.addText(Text("", 32, 0, 0, pygame.Color(255,255,255), True))

# info seite 
info_page = Screen(1024, 600, pygame.Surface(fullscreen), info_img[0])
info_page.addButton(Button(606, 496, 400, 80,solution_btn_img[0], None, switchInfoScreen))

# end page
end_page = Screen(1024, 600, pygame.Surface(fullscreen), end_bg)
end_page.addButton(Button(312, 440, 400, 80, end_btn_img, None, getPrize))
end_page.addText(Text("",48, 0,0, pygame.Color(255,255,255), None, True))

# qr-code page
qr_page = Screen(1024, 600, pygame.Surface(fullscreen), qr_bg)
qr_page.addButton(Button(387, 486, 250, 50, reset_btn_img, None, resetAll))

question = Screen(1024, 600, pygame.Surface(fullscreen), question_bg)

def checkAnswer(btn_id):
    global info_page
    global end_page
    global current_index
    global antwort_index
    global user_score
    global antwort_text
    global question
    global after_question
    # check answer
    if btn_id == antwort_index[current_index]:
        after_question.changeText(0,"Richtig, " + antwort_text[antwort_index[current_index]])
        user_score += 1
    else: 
        after_question.changeText(0,"Falsch, "+ antwort_text[antwort_index[current_index]])

    info_page.changeImage(info_img[antwort_index[current_index]])
    end_page.changeText(0, str(user_score)+"/4")
    switch(State.AFTER_QUESTION)
    # drive(sequence[current_index])
    # rotiere zur nächsten Station

resetAll()
# question page
for i in range(4):
    btn = Button(const.ANSWER_BTN_STARTX,const.ANSWER_BTN_STARTY+(i*const.ANSWER_BTN_GAP),
                       const.ANSWER_BTN_WIDTH, const.ANSWER_BTN_HEIGHT,question_btn_img[i],i, partial(checkAnswer, i), current_answers[i])
    question.addButton(btn)


# main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if current_state.value == State.START.value:
                start.checkEvent(mouse[0], mouse[1])
            elif current_state.value == State.QUESTION.value:
                question.checkEvent(mouse[0], mouse[1])
            elif current_state.value == State.AFTER_QUESTION.value:
                after_question.checkEvent(mouse[0], mouse[1])
            elif current_state.value == State.INFO_PAGE.value:
                info_page.checkEvent(mouse[0], mouse[1])
            elif current_state.value == State.END.value:
                end_page.checkEvent(mouse[0], mouse[1])
            elif current_state.value == State.OUTPUT.value:
                qr_page.checkEvent(mouse[0], mouse[1])

    if current_state.value == State.START.value:
        start.draw()
    elif current_state.value == State.QUESTION.value:
        question.draw()
    elif current_state.value == State.AFTER_QUESTION.value:
        after_question.draw()
    elif current_state.value == State.INFO_PAGE.value:
        info_page.draw()
    elif current_state.value == State.END.value:
        end_page.draw()
    elif current_state.value == State.OUTPUT.value:
        qr_page.draw()
        checkRestart()
    
            # Remember to update your clock and display at the end
    pygame.display.update()
    windowclock.tick(60)
# main loop