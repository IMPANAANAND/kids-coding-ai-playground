"""Entry point: run `python main.py` from this folder."""
import math
import random
import pygame
from ui import *
from balloon_game import BalloonGame
from fruit_ai_game import FruitGame

WIDTH, HEIGHT = 1100, 700


class Playground:
    def __init__(self):
        pygame.init()
        try: pygame.mixer.init()
        except pygame.error: pass  # Audio is optional; graphics and controls still work.
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Kids Coding & AI Playground")
        self.clock=pygame.time.Clock(); self.running=True; self.scene="home"; self.elapsed=0
        self.muted=False; self.balloon=None; self.fruit=None

    def home(self): self.scene="home"

    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: self.running=False
            elif self.scene=="balloon": self.balloon.event(event)
            elif self.scene=="fruit": self.fruit.event(event)
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if pygame.Rect(20,20,110,44).collidepoint(event.pos): self.scene="help"
                elif pygame.Rect(WIDTH-142,20,122,44).collidepoint(event.pos): self.scene="exit_confirm"
                elif self.scene=="home":
                    if pygame.Rect(100,320,400,275).collidepoint(event.pos):
                        self.balloon=BalloonGame((WIDTH,HEIGHT),self.home); self.scene="balloon"
                    elif pygame.Rect(600,320,400,275).collidepoint(event.pos):
                        self.fruit=FruitGame((WIDTH,HEIGHT),self.home); self.scene="fruit"
                elif self.scene=="help": self.scene="home"
                elif self.scene=="exit_confirm":
                    if pygame.Rect(WIDTH//2-155,390,135,55).collidepoint(event.pos): self.running=False
                    elif pygame.Rect(WIDTH//2+20,390,135,55).collidepoint(event.pos): self.scene="home"
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                if self.scene in ("help","exit_confirm"): self.scene="home"
                elif self.scene=="home": self.scene="exit_confirm"

    def draw_home(self):
        draw_background(self.screen,self.elapsed)
        # Floating playful confetti dots.
        for i,c in enumerate([PINK,YELLOW,GREEN,ORANGE,PURPLE]):
            x=int(60+i*240+math.sin(self.elapsed+i)*18); y=int(155+math.sin(self.elapsed*1.4+i*2)*12)
            pygame.draw.circle(self.screen,c,(x,y),8)
        text(self.screen,"KIDS CODING & AI PLAYGROUND",(WIDTH//2,70),49,INK,True,True)
        text(self.screen,"Play Games. Learn Python. Train AI.",(WIDTH//2,123),28,PURPLE,True)
        # Game cards
        for rect,color,title,sub,button in [((100,205,400,400),(255,255,255),"BALLOON POP","Learn Python Game Coding","PLAY NOW"),((600,205,400,400),(255,255,255),"AI FRUIT ROBOT","Teach a Robot with Machine Learning","TRAIN & PLAY")]:
            panel(self.screen,rect,color)
        # Art created from Pygame shapes
        for i,c in enumerate([(240,82,98),(70,150,240),(70,190,120),(255,198,50)]):
            draw_balloon(self.screen,185+i*72,300+math.sin(self.elapsed*1.7+i)*12,c,.8)
        pygame.draw.rect(self.screen,(142,123,212),(735,250,130,115),border_radius=30)
        pygame.draw.circle(self.screen,WHITE,(770,293),14); pygame.draw.circle(self.screen,WHITE,(830,293),14)
        pygame.draw.circle(self.screen,INK,(770,295),6); pygame.draw.circle(self.screen,INK,(830,295),6)
        pygame.draw.arc(self.screen,INK,(778,315,44,25),0,3.14,3)
        draw_fruit(self.screen,685,335,"apple",.8); draw_fruit(self.screen,900,335,"orange",.8)
        text(self.screen,"BALLOON POP",(300,390),35,INK,True,True)
        text(self.screen,"Learn Python Game Coding",(300,426),23,PURPLE,True)
        text(self.screen,"AI FRUIT ROBOT",(800,390),35,INK,True,True)
        text(self.screen,"Teach a Robot with Machine Learning",(800,426),21,PURPLE,True)
        Button((175,490,250,62),"PLAY NOW",PINK).draw(self.screen,None,pygame.mouse.get_pos())
        Button((675,490,250,62),"TRAIN & PLAY",GREEN).draw(self.screen,None,pygame.mouse.get_pos())
        text(self.screen,"Python • Creativity • Smart guesses",(WIDTH//2,635),24,WHITE,True)
        Button((20,20,110,44),"? HELP",PURPLE,font_size=20).draw(self.screen,None,pygame.mouse.get_pos())
        Button((WIDTH-142,20,122,44),"EXIT",ORANGE,font_size=20).draw(self.screen,None,pygame.mouse.get_pos())

    def draw(self):
        if self.scene=="home": self.draw_home()
        elif self.scene=="balloon": self.balloon.draw(self.screen,self.elapsed)
        elif self.scene=="fruit": self.fruit.draw(self.screen,self.elapsed)
        elif self.scene=="help":
            draw_background(self.screen,self.elapsed); panel(self.screen,(170,100,760,500))
            text(self.screen,"WELCOME, CODE EXPLORER!",(WIDTH//2,150),42,PURPLE,True,True)
            text(self.screen,"BALLOON POP",(260,230),29,PINK,True,True)
            text(self.screen,"Click balloons to collect points.",(260,273),24,INK,True)
            text(self.screen,"Avoid the dark bomb balloon!",(260,310),24,INK,True)
            text(self.screen,"AI FRUIT ROBOT",(WIDTH-260,230),29,GREEN,True,True)
            text(self.screen,"Choose labels for 8 fruits.",(WIDTH-260,273),24,INK,True)
            text(self.screen,"Then see how AI guesses!",(WIDTH-260,310),24,INK,True)
            text(self.screen,"Press ESC to go back.",(WIDTH//2,410),24,PURPLE,True)
            Button((WIDTH//2-105,490,210,58),"LET'S PLAY!",GREEN).draw(self.screen,None,pygame.mouse.get_pos())
        elif self.scene=="exit_confirm":
            draw_background(self.screen,self.elapsed); panel(self.screen,(330,230,440,260))
            text(self.screen,"READY TO GO?",(WIDTH//2,285),39,INK,True,True)
            text(self.screen,"Your adventure will be here next time.",(WIDTH//2,335),22,INK,True)
            Button((WIDTH//2-155,390,135,55),"EXIT",ORANGE).draw(self.screen,None,pygame.mouse.get_pos())
            Button((WIDTH//2+20,390,135,55),"STAY",GREEN).draw(self.screen,None,pygame.mouse.get_pos())

    def run(self):
        while self.running:
            dt=min(self.clock.tick(60)/1000,0.05); self.elapsed+=dt
            self.events()
            if self.scene=="balloon": self.balloon.update(dt)
            elif self.scene=="fruit": self.fruit.update(dt)
            self.draw(); pygame.display.flip()
        pygame.quit()


if __name__=="__main__":
    Playground().run()
