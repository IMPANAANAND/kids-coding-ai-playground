"""Balloon Pop Challenge: edit the constants below to change the game."""
import random
import pygame
from ui import *

# Teaching variables: change these values and restart to see the effect.
BALLOON_SPEED = 95
SPAWN_RATE = 0.72                 # seconds between balloons
GAME_DURATION = 45
RED_POINTS = 10
GOLD_POINTS = 50
BOMB_PENALTY = -20

BALLOONS = [((238,75,92), RED_POINTS, "red"), ((65,145,238),15,"blue"),
            ((60,185,116),20,"green"), ((255,196,48),GOLD_POINTS,"gold"),
            ((48,54,68),BOMB_PENALTY,"bomb")]


class BalloonGame:
    def __init__(self, size, home):
        self.w, self.h = size
        self.home = home
        self.best = 0
        self.reset()

    def reset(self):
        self.score, self.time_left = 0, float(GAME_DURATION)
        self.spawn_clock, self.balloons, self.effects = 0, [], []
        self.state = "playing"

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.home(); return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            p = event.pos
            if pygame.Rect(20, 18, 116, 42).collidepoint(p): self.home(); return
            if self.state == "playing":
                for b in self.balloons[:]:
                    if (p[0]-b["x"])**2+(p[1]-b["y"])**2 < (b["radius"]*1.2)**2:
                        self.score = max(0, self.score + b["points"])
                        self.effects.append([b["x"],b["y"],0.5,"+"+str(b["points"]) if b["points"]>0 else str(b["points"]),b["color"]])
                        self.balloons.remove(b); break
            elif self.state == "over":
                if pygame.Rect(self.w//2-160,self.h//2+125,145,52).collidepoint(p): self.reset()
                elif pygame.Rect(self.w//2+15,self.h//2+125,160,52).collidepoint(p): self.home()
            if pygame.Rect(self.w-118,18,98,42).collidepoint(p) and self.state == "playing": self.state = "paused"
            elif self.state == "paused" and pygame.Rect(self.w//2-80,self.h//2+55,160,52).collidepoint(p): self.state="playing"

    def update(self, dt):
        if self.state != "playing": return
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left=0; self.state="over"; self.best=max(self.best,self.score); return
        self.spawn_clock += dt
        while self.spawn_clock >= SPAWN_RATE:
            self.spawn_clock -= SPAWN_RATE
            color, points, kind = random.choices(BALLOONS, weights=[25,22,20,6,8])[0]
            self.balloons.append({"x":random.randint(50,self.w-50),"y":self.h+30,"color":color,
                                 "points":points,"kind":kind,"radius":22,"speed":BALLOON_SPEED*random.uniform(.65,1.45),"phase":random.random()*6})
        for b in self.balloons:
            b["y"] -= b["speed"]*dt
            b["x"] += math.sin(pygame.time.get_ticks()/450+b["phase"])*20*dt
        self.balloons=[b for b in self.balloons if b["y"]>-70]
        for e in self.effects: e[2]-=dt; e[1]-=28*dt
        self.effects=[e for e in self.effects if e[2]>0]

    def draw(self, surface, t):
        draw_background(surface,t)
        pygame.draw.ellipse(surface,(93,194,117),(-100,self.h-90,self.w+200,190))
        # clouds and warm sun
        pygame.draw.circle(surface,(255,225,121),(self.w-80,92),40)
        text(surface,"BALLOON POP CHALLENGE",(self.w//2,30),34,INK,True,True)
        Button((20,18,116,42),"⌂ HOME",PURPLE,font_size=20).draw(surface,None,pygame.mouse.get_pos())
        panel(surface,(220,72,190,52)); panel(surface,(455,72,190,52)); panel(surface,(690,72,190,52))
        text(surface,"SCORE  "+str(self.score),(315,98),24,INK,True,True)
        text(surface,"TIME  "+str(int(self.time_left+0.99)),(550,98),24,INK,True,True)
        text(surface,"BEST  "+str(self.best),(785,98),24,INK,True,True)
        for b in self.balloons: draw_balloon(surface,b["x"],b["y"],b["color"],1,b["kind"]=="bomb")
        for x,y,left,label,color in self.effects: text(surface,label,(x,y),30,color,True,True)
        text(surface,"Click balloons to score! Avoid the dark bomb.",(self.w//2,self.h-27),22,WHITE,True)
        if self.state == "playing":
            Button((self.w-118,18,98,42),"Ⅱ PAUSE",ORANGE,font_size=20).draw(surface,None,pygame.mouse.get_pos())
        elif self.state == "paused":
            panel(surface,(self.w//2-220,self.h//2-80,440,200)); text(surface,"TAKE A BREATHER!",(self.w//2,self.h//2-25),42,INK,True,True)
            Button((self.w//2-80,self.h//2+35,160,52),"RESUME",GREEN).draw(surface,None,pygame.mouse.get_pos())
        elif self.state == "over":
            panel(surface,(self.w//2-260,self.h//2-150,520,330)); text(surface,"TIME'S UP!",(self.w//2,self.h//2-105),48,PURPLE,True,True)
            text(surface,f"Your score: {self.score}    Best: {self.best}",(self.w//2,self.h//2-35),30,INK,True)
            text(surface,"Wonderful popping!",(self.w//2,self.h//2+12),26,GREEN,True)
            Button((self.w//2-160,self.h//2+125,145,52),"PLAY AGAIN",GREEN,font_size=20).draw(surface,None,pygame.mouse.get_pos())
            Button((self.w//2+15,self.h//2+125,160,52),"BACK HOME",PURPLE,font_size=20).draw(surface,None,pygame.mouse.get_pos())
