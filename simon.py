# simon.py
import g,pygame,random,utils

delay=1000 # between item displays - only used by aim instance

class Simon: # most methods only used by aim instance

    def __init__(self,glow_time):
        self.glow_time=glow_time; self.list1=[]
        self.running=False; self.ind=0; self.started=False
        self.glow_active=False
    
    def new1(self):
        self.list1=[]; self.inc(); self.started=False

    def do(self):
        if self.running and not self.glow_active:
            d=pygame.time.get_ticks()-self.ms
            if d<0 or d>=delay: # time to display
                self.glow_start(self.list1[self.ind]); self.ind+=1
                self.ms=pygame.time.get_ticks()+self.glow_time
                if self.ind==len(self.list1): self.running=False

    def inc(self):
        while True: # don't allow double at the start
            r=random.randint(0,len(g.imgs)-1)
            if self.list1==[]: break
            if len(self.list1)>1: break
            if r<>self.list1[0]: break
        #if len(self.list1)>1: r=self.list1[0]+1 ###
        self.list1.append(r)
        self.play(); self.started=True
        
    def play(self): # delayed start
        self.running=True; self.ind=0
        self.ms=pygame.time.get_ticks()
        
    def start(self): # immediate start
        self.running=True; self.ind=0
        self.ms=pygame.time.get_ticks()-delay
        
    def glow(self):
        if self.glow_active:
            ind=self.glow_ind
            cx=g.imgs[ind].cx; cy=g.imgs[ind].cy
            utils.centre_blit(g.screen,g.glow[ind],(cx,cy))
            d=pygame.time.get_ticks()-self.glow_ms
            if d<0 or d>=self.glow_time: self.glow_active=False

    def glow_start(self,ind):
        self.glow_ms=pygame.time.get_ticks()
        self.glow_active=True
        self.glow_ind=ind

    def glow_off(self):
        self.glow_active=False


    

