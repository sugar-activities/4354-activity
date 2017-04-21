# utils.py
import g,pygame,sys,os,random,copy

#constants
RED,BLUE,GREEN,BLACK,WHITE=(255,0,0),(0,0,255),(0,255,0),(0,0,0),(255,255,255)
CYAN,ORANGE=(0,255,255),(255,165,0)

def exit():
    save(str(g.best))
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def save(str):
    dir=''
    dir=os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir==None: dir=''
    fname=os.path.join(dir,'data','save.dat')
    f=open(fname, 'w')
    f.write(str+'\n')
    f.close
    
def load():
    dir=''
    dir=os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir==None: dir=''
    fname=os.path.join(dir,'data','save.dat')
    try:
        f=open(fname, 'r')
    except:
        return None #****
    try:
        g.best=int(f.read())
    except:
        pass
    f.close
    
# loads an image (eg pic.png) from the data subdirectory
# converts it for optimum display
# resizes it using the image scaling factor, g.imgf
#   so it is the right size for the current screen resolution
#   all images are designed for 1200x900
def load_image(file1,alpha=False,subdir=''): # eg subdir='glow'
    data='data'
    if subdir!='': data=os.path.join('data',subdir)
    fname=os.path.join(data,file1)
    try:
        img=pygame.image.load(fname)
    except:
        print "Peter says: Can't find "+fname; exit()
    if alpha:
        img=img.convert_alpha()
    else:
        img=img.convert()
    if abs(g.imgf-1.0)>.1: # only scale if factor <> 1
        w=img.get_width(); h=img.get_height()
        img=pygame.transform.smoothscale(img,(int(g.imgf*w),int(g.imgf*h)))
    return img
        
def load_sound(file):
    fname=os.path.join('data',file)
    try:
        snd=pygame.mixer.Sound(fname)
    except:
        print "Peter says: Can't find "+fname; exit()
    return snd

# eg new_list=copy_list(old_list)
def copy_list(l):
    new_list=[];new_list.extend(l)
    return new_list

def shuffle(lst):        
    l1=lst; lt=[]
    for i in range(len(lst)):
        ln=len(l1); r=random.randint(0,ln-1);
        lt.append(lst[r]); l1.remove(lst[r])
    return lt

def centre_blit(screen,img,(cx,cy),angle=0): # rotation is clockwise
    img1=img
    if angle!=0: img1=pygame.transform.rotate(img,-angle)
    rect=img1.get_rect()
    screen.blit(img1,(cx-rect.width/2,cy-rect.height/2))
    
# m is the message
# d is the # of pixels in the border around the text
# (cx,cy) = co-ords centre - (0,0) means use screen centre
def message(screen,font,m,(cx,cy)=(0,0),d=20):
    if m!='':
        if pygame.font:
            text=font.render(m,True,(255,255,255))
            shadow=font.render(m,True,(0,0,0))
            rect=text.get_rect();
            if cx==0: cx=screen.get_width()/2
            if cy==0: cy=screen.get_height()/2
            rect.centerx=cx;rect.centery=cy
            bgd=pygame.Surface((rect.width+2*d,rect.height+2*d))
            bgd.fill((0,255,255))
            bgd.set_alpha(128)
            screen.blit(bgd,(rect.left-d,rect.top-d))
            screen.blit(shadow,(rect.x+2,rect.y+2,rect.width,rect.height))
            screen.blit(text,rect)

# eg click_img=ImgClickClass(img,(x,y)) (x,y)=top left
#   if click_img.mouse_on():
#   click_img.draw(gscreen)
class ImgClickClass: # for clickable images
    def __init__(self,img,(x1,y1),centre=False):
        w=img.get_width();h=img.get_height();x=x1;y=y1
        if centre: x=x-w/2; y=y-h/2; self.cx=x1; self.cy=y1
        self.rect=pygame.Rect(x,y,w,h)
        self.x=x; self.y=y; self.img=img

    def mouse_on(self):
        (mx,my)=pygame.mouse.get_pos()
        return self.rect.collidepoint(mx,my)

    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))
        
class Slider:
    def __init__(self,cx,cy,steps,colour=BLACK):
        self.easy=load_image('easy.png',True)
        self.hard=load_image('hard.png',True)
        self.xo=load_image('xo.png',True)
        iw=self.hard.get_width(); ih=self.hard.get_height()
        w=g.sy(20); w2=w/2; h2=ih/2
        self.x1=cx-w2; self.y=cy-h2; self.x2=cx+w2-iw
        x=cx-w2+iw*1.2; w=w-2*iw*1.2; h=g.sy(.12);y=cy+g.sy(.34)
        self.rect=pygame.Rect(x,y,w,h)
        mh=g.sy(.5);self.mark=pygame.Rect(x,y-mh/2+h/2,h,mh)
        self.steps=steps; self.dx=w/(steps-1);self.colour=colour
        self.cx=cx; self.cy=cy
        marks=[]; x=self.rect.left
        for i in range(self.steps):
            rect=copy.copy(self.mark); rect.left=x-5; rect.width=10; marks.append(rect); x+=self.dx
        self.marks=marks

    def draw(self):
        g.screen.blit(self.easy,(self.x1,self.y));
        g.screen.blit(self.hard,(self.x2,self.y))
        pygame.draw.rect(g.screen,self.colour,self.rect) # horizontal line
        x=self.rect.left # now draw marks
        for i in range(self.steps):
            self.mark.left=x; pygame.draw.rect(g.screen,self.colour,self.mark)
            if i==(g.level-1):
                dx=self.xo.get_width()/2; dy=self.xo.get_height()/2
                g.screen.blit(self.xo,(x-dx+self.mark.w/2,self.cy-dy))
            x+=self.dx

    def mouse(self):
        (mx,my)=pygame.mouse.get_pos()
        rect=self.easy.get_rect(topleft=(self.x1,self.y))
        if rect.collidepoint(mx,my):
            if g.level>1: g.level-=1; return True#****
        rect=self.hard.get_rect(topleft=(self.x2,self.y))
        if rect.collidepoint(mx,my):
            if g.level<self.steps: g.level+=1; return True#****
        n=1
        for rect in self.marks:
            if rect.collidepoint(mx,my):
                if g.level==n:
                    return False#****
                else:
                    g.level=n; return True#****
            n+=1
        return False
    
def display_number(n,(cx,cy)):
    if pygame.font:
        text=g.font2.render(str(n),True,BLUE)
        centre_blit(g.screen,text,(cx,cy))

