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
CAPTION= 'The Matrix of Conway\'s game'
SCREEN_SIZE =(640,480)
FONT_SIZE = 23
FONT_WIDTH = 10
FONT_HEIGHT = 20
assert SCREEN_SIZE[0]%FONT_WIDTH == 0, 'please change your display settings ^v^'
assert SCREEN_SIZE[1]%FONT_HEIGHT ==0, 'please change your display settings ^v^'
FONT_COLOR = (53,211,111)


COLUMN = int(SCREEN_SIZE[0]/FONT_WIDTH)
ROW =int(SCREEN_SIZE[1]/FONT_HEIGHT)

CELL_NUM = COLUMN * ROW

BG = []
for i in range(COLUMN):
    BG.append([])
    for j in range(ROW):
        BG[i].append('dead')

def print_text(surface,position,text,size,colour,bg_colour=None):
    font_layer = pg.font.Font(GAME_FONT,size)
    font_surface = font_layer.render(text,True,colour,bg_colour)
    surface.blit(font_surface,position)
    return surface

class World:
    def __init__(self):
        self.cells = {}
        self.cell_id = 0

    def add_cell(self,cell):
        self.cells[self.cell_id] = cell
        cell.id = self.cell_id
        self.cell_id += 1

    def alive_judge(self,neighbours):
        count = 0
        for i in neighbours:
            if self.cells[i].state == 'alive':
                count +=1
        if count == 2 or count == 3:
            return 'alive'
        else:
            return 'dead'
                

    def dead_judge(self,neighbours):
        count = 0
        for i in neighbours:
            if self.cells[i].state == 'alive':
                count +=1
        if count == 3:
            return 'alive'
        else:
            return 'dead'

    def update(self,dt,surface):
        for cell in list(self.cells.values()):
            if cell.state == 'alive':
                cell.state = self.alive_judge(cell.neighbours())
            elif cell.state == 'dead':
                cell.state = self.dead_judge(cell.neighbours())
            cell.update(dt,surface)

class Cell(pg.sprite.Sprite):
    def __init__(self,x,y,state):
        super().__init__()
        self.i = x
        self.j = y
        self.state = state
        self.time = 1
        self.looks = random.choice(STRING)
        self.id = None

    def neighbours(self):
        x = self.i
        y = self.j
        neighbours =[]
        for num in range(CELL_NUM):
            i = num//COLUMN
            j = num%COLUMN
            if (i-x<=1 and i-x >= -1) and (j-y<=1 and j-y >= -1) and not (i-x==0 and j-y==0):
                neighbours.append(num)
        return neighbours


    def update(self,dt,surface):
        self.draw(surface)

            
                      
    def draw(self,surface):
        if self.state =='alive':
            print_text(surface,(self.j*FONT_WIDTH,self.i*FONT_HEIGHT),self.looks,FONT_SIZE,FONT_COLOR,bg_colour=None)        


class Game(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.world = World()
        for i in range(ROW):
            for j in range(COLUMN):
                cell = Cell(i,j,random.choice(['dead','alive']))
                self.world.add_cell(cell)
        self.fullscreen = False
        self.done = False
        
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

    def update(self,dt):
        pg.display.set_caption(CAPTION)
        self.screen.fill((0,0,0))
        self.world.update(dt,self.screen)


    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            pg.display.update()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] ='1'
    pg.init()
    pg.display.set_mode(SCREEN_SIZE)    
    game = Game()
    game.run()
    pg.quit()
    sys.exit()
