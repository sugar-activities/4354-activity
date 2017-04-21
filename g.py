# g.py - globals
import pygame,utils

app='Follow Me'; ver='1.0'
ver='1.1'
# new bgd
# ladder
ver='1.2'
# scaled font @ imgf
# man on ladder
# green bgd -> new buttons
ver='1.3'
# star separate & left @ top
ver='1.4'
# added magician pic

XO=True # affects the pygame.display.set_mode() call only
screen=None
pointer=None
w=800; h=600 # screen width & height - set dynamically on XO box
font1=None
clock=None
factor=0.0 # measurement scaling factor (32x24 = design units)
offset=0 # we assume 4:3 - centre on widescreen
imgf=0.0 # image scaling factor - all images built for 1200x900
message=''
frame_rate=0; version_display=False

# this activity only
imgs=[]
glow=[]
player_n=0 # player click counter
wrong=False

def init(): # called by main()
    global screen,w,h,pointer,font1,font2,clock,click_snd
    global factor,offset,imgf
    pygame.init() # set up pygame
    pygame.display.set_caption(app+' Version '+ver)
    if XO:
        screen=pygame.display.set_mode(); w,h=screen.get_size()
    else:
        screen=pygame.display.set_mode((w,h))
    pygame.mouse.set_visible(False)
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(54*imgf); font1=pygame.font.Font(None,t)
        t=int(48*imgf); font2=pygame.font.Font(None,t)
    pointer=utils.load_image('pointer.png',True)
    
    # this activity only
    global imgs,glow,wrong_img,man,ladder,star,best,score,magician
    global man_x0,man_y0,man_dx,man_dy,man_sc_dx,man_sc_dy
    wrong_img=utils.load_image('wrong.png',True); wrong_ind=0; right_ind=0
    man=utils.load_image('man.png',True)
    man_x0=sx(25.5); man_y0=sy(18.31)
    man_dx=(sx(27.87)-man_x0)/11.0; man_dy=(sy(12.15)-man_y0)/11.0
    man_sc_dx=sx(25.38)-man_x0; man_sc_dy=sy(18.61)-man_y0
    ladder=utils.load_image('ladder.png',True)
    star=utils.load_image('star.png',True)
    magician=utils.load_image('magician.png',True)
    cy=sy(3.2); dx=sy(6.4); dy=sy(6.2); i=1
    score=0; best=0
    utils.load() # fetch best
    for r in range(1,4):
        cx=sx(3.2)
        for c in range(1,6):
            imgs.append(utils.ImgClickClass(utils.load_image(str(i)+'.png',True),(cx,cy),True))
            glow.append(utils.load_image(str(i)+'.png',True,'glow'))
            cx+=dx; i+=1
            if i==15: break
        cy+=dy

def sx(f): # scale x function
    return f*factor+offset

def sy(f): # scale y function
    return f*factor

def inc_level(): # inc difficulty level
    global level,steps
    level=level+1
    if level==7: level=6
    steps=8*level+32

