import pygame as pg
import pygame.gfxdraw
import sys,os,math
from tkinter import *
from tkinter import ttk
import pyscreenshot


w = 400 # width for the Tk root
h = 450 # height for the Tk root

root = Tk()
root.title("tools")
embed = Frame(root, width=w, height=h)
embed.grid(row=0, column=2)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'



# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/28) - (w/17)
y = (hs/8) - (h/7)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

pg.init()
pg.event.set_allowed([pg.QUIT,pg.MOUSEMOTION,pg.MOUSEBUTTONDOWN,pg.KEYDOWN])

# Settings:
clock = pygame.time.Clock()
fps = 240
font = pg.font.SysFont('consolas',20)
screenres = (1000,800)
realres = (screenres[0]*1.2,screenres[1]*1.2)

updated = False
dirtyrects = []
vis = 255

# Colors | R | G | B | A |
clear =  (  0,  0,  0,  0)
white =  (255,255,255)
gray =   (150,150,150)
black =  (  0,  0,  0)
red =    (255,  0,  0)
orange = (255,125,  0)
yellow = (255,255,  0)
green =  (  0,225,  0)
blue =   (  0,  0,255)
purple = (150,  0,150)
lightblue = (70, 130, 180, 180)

brush = 2

colors = [black,white,red,orange,yellow,green,blue,purple, lightblue]


numkey = [
    pg.K_1,
    pg.K_2,
    pg.K_3,
    pg.K_4,
    pg.K_5,
    pg.K_6,
    pg.K_7,
    pg.K_8
]

# Surfaces:
window = pg.display.set_mode(screenres,pg.DOUBLEBUF)
window.fill(gray)
canvas = pg.Surface((realres[0],realres[1]*0.84)).convert_alpha()
canvas.fill(white)
latest1 = canvas.copy()
latest2 = canvas.copy()
latest3 = canvas.copy()
latest4 = canvas.copy()
latest5 = canvas.copy()
layers = [latest1,latest2,latest3,latest4,latest5]
for layer in layers:
    layer.fill(clear)
overlay = pg.Surface(screenres).convert_alpha()

# Rects:
realrect = pg.Rect(0,0,realres[0],int(realres[1]*0.84))
screenrect = pg.Rect(0,0,screenres[0],int(screenres[1]*0.84))
toolbar = pg.Rect(0,720,500,80)


r = 2
r1 = 1
clr = black
startpoint = None
endpoint = None
ongoing = False
undone = 6
maxundone = 7
holdingclick = False
bt = 0.999
index_draw0 = 0
index_draw1 = 1




def size_brpl():
    global r
    r += 5
    lbl['text'] = f"Size:{r}"

def size_brmin():
    global r
    r -= 5
    lbl['text'] = f"Size:{r}"


buttonplus = ttk.Button(root, text="+", command=size_brpl)
buttonplus.place(x=5, y=7)

buttonminus = ttk.Button(root, text="-", command=size_brmin)
buttonminus.place(x=155, y=7)

lbl = ttk.Label(root, text = 'Size:2')
lbl.place(x=96, y=11)

def tools1():
    global bt, index_draw0, clr
    bt = 100.999
    index_draw0 = 0
    clr = black

buttont1 = ttk.Button(root, text=" tools1 ", command=tools1)
buttont1.place(x=55, y=50)

def tools2():
    global index_draw0,bt, clr
    bt = 0.999
    index_draw0 = 1
    clr = black


buttont2 = ttk.Button(root, text=" tools2 ", command=tools2)
buttont2.place(x=55, y=100)

def brush():
    global index_draw0, bt, r1, clr
    r1 = 1
    bt = 0.999
    index_draw0 = 0
    clr = black


buttont3 = ttk.Button(root, text=" Brush ", command=brush)
buttont3.place(x=55, y=150)



def pen():
    global r1, bt, clr
    r1 += 2
    bt = 0.999
    clr = black

buttont4 = ttk.Button(root, text="pen", command=pen)
buttont4.place(x=55, y=200)

def save():
    img = pyscreenshot.grab(bbox=(500, 140,  1400, 826))
    img.save('unitled.jpg')
    img.show()

buttont5 = ttk.Button(root, text="save", command=save)
buttont5.place(x=55, y=300)

def eraser():
    global clr
    clr = white

buttont6 = ttk.Button(root, text=" eraser", command=eraser)
buttont6.place(x=55, y=250)




def button(color,rect):
    global clr,holdingclick, r
    if 0 <= rect <= 9:
        rect = pg.Rect(48*rect+12,740,44,44)
        if pg.mouse.get_pressed()[0] and rect.collidepoint(mousepos) and not holdingclick:
            clr = color
            dirtyrects.append(toolbar)
        if clr == color:
            pg.draw.rect(overlay,color,rect)
            pg.draw.rect(overlay,black,rect,3)
        else:
            pg.draw.rect(overlay,color,(rect[0]+4,rect[1]+4,rect[2]-8,rect[3]-8))
            pg.draw.rect(overlay,black,(rect[0]+4,rect[1]+4,rect[2]-8,rect[3]-8),3)






def drawline():
    global startpoint,endpoint,start
    if startpoint == None:
        startpoint = x,y
    endpoint = x,y
    if r > 1:
        if startpoint != endpoint:
            dx,dy = endpoint[0]-startpoint[0],endpoint[1]-startpoint[1]
            angle = math.atan2(-dy,dx)%(2*math.pi)
            dx,dy = math.sin(angle)*(r*bt),math.cos(angle)*(r*bt)
            a = startpoint[index_draw0]+dx,startpoint[1]+dy
            b = startpoint[0]-dx,startpoint[1]-dy
            c = endpoint[index_draw0]-dx,endpoint[1]-dy
            d = endpoint[0]+dx,endpoint[1]+dy
            pointlist = [a,b,c,d]
            pg.draw.polygon(latest1,clr,pointlist)
        pg.draw.circle(latest1, (220, 220, 220), (x, y), r1)
        pg.draw.circle(latest1,clr,(x,y),r)
    else:
        pg.draw.line(latest1,clr,startpoint,endpoint,r)
    startpoint = x,y

def shiftdown():
    for layer in reversed(layers):
        if layer == latest5:
            canvas.blit(latest5,(0,0))
        else:
            layers[layers.index(layer)+1].blit(layer,(0,0))

def shiftup():
    for layer in layers:
        if layer == latest5:
            layer.fill(clear)
        else:
            layer.fill(clear)
            layer.blit(layers[layers.index(layer)+1],(0,0))

# Drawing static parts of overlay:
overlay.fill(clear)
pg.draw.rect(overlay,gray,toolbar)
pg.draw.rect(overlay,black,toolbar,3)


# Drawing number indicators for colors:
for color in colors:
    text = font.render(str(colors.index(color)+1),True,black)
    overlay.blit(text,(48*colors.index(color)+28,724))

overlaybg = overlay.copy()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEMOTION:
            mousepos = pg.mouse.get_pos()
            x = int(mousepos[0]*(realres[0]/screenres[0]))
            y = int(mousepos[1]*(realres[1]/screenres[1]))
            holdingclick = True
            if screenrect.collidepoint(mousepos):
                dirtyrects.append(screenrect)

        if event.type == pg.MOUSEBUTTONDOWN:
            holdingclick = False
            if screenrect.collidepoint(mousepos):
                dirtyrects.append(screenrect)

            # Changing brush size:
            if event.button == 4 and r < 100:
                r += 1
                dirtyrects.append(screenrect)
            elif event.button == 5 and r > 2:
                r -= 1
                dirtyrects.append(screenrect)

        if event.type == pg.KEYDOWN:

            if event.key in numkey:
                clr = colors[numkey.index(event.key)]
                dirtyrects.append(toolbar)

            # Emptying canvas:
            if event.key == pg.K_e:
                canvas.fill(white)
                latest5.fill(clear)
                latest4.fill(clear)
                latest3.fill(clear)
                latest2.fill(clear)
                latest1.fill(clear)
                undone = 0
                maxundone = 0
                dirtyrects.append(screenrect)

            # Undoing and redoing:
            if event.key == pg.K_u and undone < maxundone:
                undone += 1
                dirtyrects.append(screenrect)
            if event.key == pg.K_i and undone > 0:
                undone -= 1
                dirtyrects.append(screenrect)

    # Painting:
    if pg.mouse.get_pressed()[0] and screenrect.collidepoint(mousepos):
        if not ongoing:
            while undone > 0:
                shiftup()
                undone -= 1
                maxundone -= 1
            shiftdown()
        drawline()
        ongoing = True
    else:
        startpoint = None
        if ongoing:
            if maxundone < 5:
                maxundone += 1
            ongoing = False

    if screenrect in dirtyrects:

        # Drawing canvas:
        window.fill(white)
        for layer in layers:
            if layers.index(layer) == undone:
                window.blit(pg.transform.smoothscale(layer,(screenrect[2],screenrect[3])),screenrect)

        # Drawing overlay:
        overlay.fill(clear)
        if r > 1:
            pg.gfxdraw.aacircle(overlay,mousepos[0],mousepos[1],int(r*screenres[0]/realres[0]),gray)
    overlay.blit(overlaybg,screenrect)
    for color in colors:
        button(color,colors.index(color))
    window.blit(overlay,screenrect)

    pg.display.set_caption('ColBrush   |   FPS: ' + str(int(clock.get_fps())))
    clock.tick(fps)


    # Updating display:
    if not updated:
        pg.display.update()
        updated = True
    pg.display.update(dirtyrects)
    dirtyrects.clear()
    root.update()



