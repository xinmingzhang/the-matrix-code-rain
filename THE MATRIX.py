import os
import sys
import pygame as pg
import random

def load_all_fonts(directory, accept=(".ttf")):
    fonts = {}
    for font in os.listdir(directory):
        name,ext = os.path.splitext(font)
        if ext.lower() in accept:
            fonts[name] = os.path.join(directory, font)
    return fonts


FONTS = load_all_fonts(os.path.join("font"))
GAME_FONT=FONTS['matrix code nfi']


STRING ='abcdefghijklmnopqrstuvwxyz1234567890!#$%^&*()-=+\|]}[{;:/?.>,<~'
CAPTION= 'The Matrix Code Rain'
SCREEN_SIZE =(640,480)
COLOR_KEY =(0,255,0)
FONT_SIZE = 23
FONT_WIDTH = 10
FONT_HEIGHT = 20
assert SCREEN_SIZE[0]%FONT_WIDTH == 0, 'please change your display settings ^v^'
assert SCREEN_SIZE[1]%FONT_HEIGHT ==0, 'please change your display settings ^v^'
FONT_COLOR = (53,211,111)
FONT_COLOR_H = (159,246,210)


COLUMN = int(SCREEN_SIZE[0]/FONT_WIDTH)
ROW =int(SCREEN_SIZE[1]/FONT_HEIGHT)

BG_TEXT = []
for i in range(COLUMN):
    BG_TEXT.append([])
    for j in range(ROW):
        BG_TEXT[i].append(random.choice(STRING))

def print_text(surface,position,text,size,colour,bg_colour=None):
    font_layer = pg.font.Font(GAME_FONT,size)
    font_surface = font_layer.render(text,True,colour,bg_colour)
    surface.blit(font_surface,position)
    return surface

class Rain(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos_x = pos
        self.length = random.randint(1,ROW)*FONT_HEIGHT
        self.rect = pg.Rect((pos,-SCREEN_SIZE[0]),(FONT_WIDTH,self.length))
        self.image = pg.Surface(self.rect.size)
        self.image.fill(COLOR_KEY)
        self.text_x = self.pos_x
        self.text_y = self.rect.bottom + FONT_HEIGHT


    def text_highlight(self,x,y,surface):
        aera = pg.Rect((0,0),SCREEN_SIZE)
        if aera.collidepoint(x,y):
            text_highlight_choice = random.randint(0,1)
            if text_highlight_choice:
                self.text = BG_TEXT[int(x//FONT_WIDTH)][int(y//FONT_HEIGHT)]
                print_text(surface,(x,y),self.text,FONT_SIZE,FONT_COLOR_H,bg_colour=None)
        
    def move(self):
        self.rect.y += random.randint(1,3)*FONT_HEIGHT
        self.text_y = self.rect.bottom + FONT_HEIGHT

    def update(self,surface):
        surface.blit(self.image,self.rect)
        self.text_highlight(self.text_x,self.text_y,surface)
        if self.rect.y > SCREEN_SIZE[1]:
            self.pos_y = -random.randint(3,ROW)*FONT_HEIGHT
            self.length = - self.pos_y
            self.rect = pg.Rect((self.pos_x,self.pos_y),(FONT_WIDTH,self.length))
        self.move()

class Game(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 20.0
        self.done = False
        self.background = None       
        self.rain = pg.sprite.Group()
        for i in range(COLUMN):
            self.rain.add(Rain(i*FONT_WIDTH))
        self.raincoat = None
        self.fullscreen = False
        
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode(SCREEN_SIZE)


    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            if self.keys[pg.K_f]:
                self.toggle_fullscreen()

    def make_raincoat(self):
        raincoat = pg.Surface(self.screen_rect.size).convert()
        raincoat.set_colorkey(COLOR_KEY)
        raincoat.fill((0,0,0))
        return raincoat

    def update(self):
        pg.display.set_caption(CAPTION)
        self.background = pg.image.load('Matrix_bg.png').convert()
        self.screen.blit(self.background,(0,0))
        self.raincoat = self.make_raincoat()
        self.rain.update(self.raincoat)
        self.screen.blit(self.raincoat,(0,0))

    def make_text_background(self):
        bg_surface = pg.Surface(SCREEN_SIZE)
        for i in range(COLUMN):
            print('loading...'+ str(int(i/(COLUMN-1)*100))+'%')
            for j in range(ROW):
                bg_surface1 = print_text(bg_surface,(i*FONT_WIDTH,j*FONT_HEIGHT),BG_TEXT[i][j],FONT_SIZE,FONT_COLOR,(0,0,0))
        pg.image.save(bg_surface1,'Matrix_bg.png')

    def run(self):
        self.make_text_background()
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] ='1'
    pg.init()
    pg.display.set_mode(SCREEN_SIZE)    
    game = Game()
    game.run()
    pg.quit()
    sys.exit()
