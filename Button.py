class Button(object):
    def __init__(self, x,y, width, height, btn_id=None):
        self.x = x
        self.y = y
        self.btn_id = btn_id
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        self.disable = False
    
    def clicked(self, mouse_x, mouse_y):
       return self.rect.collidepoint(mouse_x, mouse_y)
    
    def getID(self):
        return self.btn_id
    
    