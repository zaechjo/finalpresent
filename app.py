# Load and initialize Modules here
import pygame
import time
import constant as const
from state import State
from functools import partial
import json
#import board
# import Adafruit_ADS1x15
# import RPi.GPIO as GPIO
# from adafruit_motor import stepper
# from adafruit_motorkit import MotorKit


pygame.init()
fullscreen = (const.SCREEN_WIDTH,const.SCREEN_HEIGHT)
window = pygame.display.set_mode(fullscreen, pygame.NOFRAME)

# electronics
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

sequences = json.load(open("sequences.json", encoding='utf-8'))

sequence = sequences["sequences"][0]["grad"]
seq = sequences["sequences"][0]["bereich"]
antworten = sequences["sequences"][0]["antworten"]
antwort_text = sequences["antwort_text"]
antwort_index = sequences["sequences"][0]["antwort_index"]

# assets and bg
start_bg = pygame.image.load("assets/START.png")
question_bg = pygame.image.load("assets/FRAGE.png")
winning_bg = pygame.image.load("assets/GEWONNEN.png")
end_bg = pygame.image.load("assets/END.png");

# info bilder


## Button assets
start_btn_img = pygame.image.load("assets/start_btn/0.png")
end_btn_img = pygame.image.load("assets/end_btn/0.png")

question_btn_img = []
solution_btn_img = []
info_img = []
user_score = 0

for i in range(4):
    tmp = pygame.image.load("assets/question_btns/"+str(i)+".png")
    tmp_info = pygame.image.load("assets/info_bg/"+str(i)+".png")
    question_btn_img.append(tmp)
    info_img.append(tmp_info)
    

for i in range(2):
    tmp = pygame.image.load("assets/solution_btns/"+str(i)+".png")
    solution_btn_img.append(tmp)

# Clock
windowclock = pygame.time.Clock()
global current_state 
global current_index
current_state = State.START
current_index = 0

def resetAll():
    global current_state
    global current_index
    current_state = State.START
    current_index = 0
    # homeCube()

## GUI Klassen

class Text(object):
    def __init__(self, text, fontsize, x, y, color ,h_center=None,center=None):
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

    

class Button(object):
    def __init__(self, x,y, width, height,img, btn_id=None, action=None):
        self.x = x
        self.y = y
        self.img = img
        self.btn_id = btn_id
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        self.disable = False
        self.action = action
    
    def clicked(self, mouse_x, mouse_y):
       return self.rect.collidepoint(mouse_x, mouse_y)
    
    def getID(self):
        return self.btn_id

    def draw(self, surf):
        surf.blit(self.img, (self.x, self.y))

    def handle_event(self):
        if self.action != None:
            self.action()


class Screen(object): 
    def __init__(self, width, height,surf, img):
        self.width  = width
        self.height = height
        self.surf = surf
        self.img = img
        self.btns = []
        self.text = []

    def addText(self, text, x, y, fontsize, color, h_center=None, center=None):
        text = Text(text, fontsize, x,y, color, h_center, center)
        self.text.append(text)
    
    def changeText(self, index, text):
        self.text[index].setText(text)
    
    def appendText(self,index, text):
        self.text[index].appendText(text)
    
    def centerText(self, index):
        self.text[index]
    
    def addButton(self,x,y, width, height,img, btn_id=None, action=None):
        btn = Button(x,y,width,height,img, btn_id, action)
        self.btns.append(btn)

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


def switch(State):
    global current_state
    current_state = State

def switchInfoScreen():
    global current_state
    global current_index
    current_index += 1
    if current_index == 4:
       switch(State.END)
    else:
        current_state = State.QUESTION

def getPrize():
    print("Get prize")
    # gebe Fahrrad aus mit drive(deg)
    time.sleep(10) # delay after click the btn
    resetAll()


# start screen
start = Screen(1024, 600, pygame.Surface(fullscreen), start_bg)
start.addButton(262, 200, 500, 200,start_btn_img, None, partial(switch, State.QUESTION))

# winning screen
after_question = Screen(1024, 600, pygame.Surface(fullscreen), winning_bg)
after_question.addButton(312, 194, 400, 80,solution_btn_img[0], None, partial(switch, State.INFO_PAGE))
after_question.addButton(312, 327, 400, 80,solution_btn_img[1], None, resetAll)
after_question.addText("", 0, 0, 32, pygame.Color(255,255,255), True)

# info seite 
info_page = Screen(1024, 600, pygame.Surface(fullscreen), info_img[0])
info_page.addButton(606, 496, 400, 80,solution_btn_img[0], None, switchInfoScreen)

def checkAnswer(btn_id):
    global current_index
    global antworten
    global user_score
    global antwort_text
    # check answer
    if btn_id == antworten[current_index]:
        after_question.changeText(0,"Richtig, " + antwort_text[antwort_index[current_index]])
        user_score += 1
    else: 
        after_question.changeText(0,"Falsch, "+ antwort_text[antwort_index[current_index]])
    
    info_page.changeImage(info_img[antwort_index[current_index]])
    end_page.changeText(0, str(user_score)+"/4")
    switch(State.AFTER_QUESTION)
    # drive(sequence[current_index])
    # rotiere zur nächsten Station
# question screen
question = Screen(1024, 600, pygame.Surface(fullscreen), question_bg)
for i in range(4):
    question.addButton(const.ANSWER_BTN_STARTX,const.ANSWER_BTN_STARTY+(i*const.ANSWER_BTN_GAP),
                       const.ANSWER_BTN_WIDTH, const.ANSWER_BTN_HEIGHT,question_btn_img[i],i, partial(checkAnswer, i))

end_page = Screen(1024, 600, pygame.Surface(fullscreen), end_bg)
end_page.addButton(312, 440, 400, 80, end_btn_img, None, getPrize)
end_page.addText("", 0,0, 48, pygame.Color(255,255,255), None, True)

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
            

            # Remember to update your clock and display at the end
        pygame.display.update()
        windowclock.tick(60)

