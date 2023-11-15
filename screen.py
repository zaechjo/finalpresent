from Button import Button
class Screen(object): 
    def __init__(self, width, height, bgImage=None):
        self.width  = width
        self.height = height
        self.surf = pygame.Surface(1024, 600)
        self.btns = []
        self.bgImage = pygame.image.load(bgImage)
    

    def addButton(self,x,y, width, height, btn_id=None):
        btn = Button(x,y,width,height, btn_id)
        self.btns.append(btn)

    def checkEvent(self, mouse_x, mouse_y):
        for b in self.btns:
            b.clicked(mouse_x, mouse_y)
    
    def drawScreen(self):
        self.surf.blit(self.bgImage, (0,0))