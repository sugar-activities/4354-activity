# FollowMe.py
import g
g.init()
import utils,pygame,simon,buttons
from pygame.locals import *

def display():
    g.screen.fill((0,255,0))
    for img in g.imgs: # img from ImgClickClass (centred)
        img.draw(g.screen)
    if g.wrong:
        img=g.imgs[g.wrong_ind]
        utils.centre_blit(g.screen,g.wrong_img,(img.cx,img.cy))
        img=g.imgs[g.right_ind]
        utils.centre_blit(g.screen,g.glow[g.right_ind],(img.cx,img.cy))
    buttons.draw()
    ladder()
    g.screen.blit(g.magician,(g.sx(3.2),g.sy(18.2)))

def ladder():
    if g.score>g.best: g.best=g.score
    if g.best>11:
        cx=g.sx(30.55); cy=g.sy(13.25)
        utils.centre_blit(g.screen,g.star,(cx,cy))
        utils.display_number(g.best,(cx,cy))
    if g.score>0:
        n=g.score-1
        if n>11: n=11
        g.screen.blit(g.ladder,(g.sx(26.95),g.sy(13.7)))
        x=g.man_x0+n*g.man_dx; y=g.man_y0+n*g.man_dy
        g.screen.blit(g.man,(x,y))
        cx=x+g.man_sc_dx; cy=y+g.man_sc_dy
        if g.score<g.best or g.best<12:
            utils.centre_blit(g.screen,g.star,(cx,cy))
            utils.display_number(g.score,(cx,cy))
    
def which():
    ind=0
    for img in g.imgs:
        if img.mouse_on(): return ind
        ind+=1
    return -1 # none clicked

def click():
    if aim.running: return False
    if g.wrong: return False
    ind=which()
    if ind==-1: return False
    if len(aim.list1)==0: return False
    player.glow_start(ind)
    buttons.off("back")
    if ind==aim.list1[g.player_n]:
        g.player_n+=1
        if g.player_n>g.score: g.score=g.player_n
        if g.player_n==len(aim.list1): # all correct - add another
            aim.inc(); g.player_n=0
    else:
        g.wrong=True; g.wrong_ind=ind; g.right_ind=aim.list1[g.player_n]
        buttons.on("green")
    return True # click processed
    
def do_button(bu):
    if bu=='green': # start
        aim.new1(); g.player_n=0; g.wrong=False; g.score=0
        buttons.off("green"); buttons.on("back")
    elif bu=='back': aim.start() # show again

def glow_off():
    aim.glow_off(); player.glow_off()
    
# initialisation
aim=simon.Simon(1200) # arg is glow time
player=simon.Simon(50)
x=g.sx(16); y=g.sy(20)
buttons.Button("green",(x,y),True)
buttons.Button("back",(x,y),True); buttons.off("back")

def main():
    while True:
        ms=pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type==QUIT:
                utils.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # allow any button - left, right or middle
                glow_off()
                if click(): break
                display(); pygame.display.flip() # no pointer in case button pressed
                bu=buttons.check()
                if bu<>'':do_button(bu)
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: utils.exit()
                if event.key==K_x: g.version_display=not g.version_display
        if g.player_n==0 and not buttons.active('green'):
            buttons.on("back")
        display()
        aim.do()
        aim.glow(); player.glow()
        if g.version_display:
            g.message=g.app+' Version '+g.ver
            g.message+='  '+str(g.w)+' x '+str(g.h)
            g.message+='  '+str(g.frame_rate)+'fps'
            utils.message(g.screen,g.font1,g.message)
        mx,my=pygame.mouse.get_pos()
        if my>g.pointer.get_height(): g.screen.blit(g.pointer,(mx,my))
        pygame.display.flip()
        g.clock.tick(40)
        d=pygame.time.get_ticks()-ms; g.frame_rate=int(1000/d)

if __name__=="__main__":
    main()
