"""A visual k-nearest-neighbours lesson using labelled fruit examples."""
import random
import pygame
from ui import *
from ml_model import knn_predict, make_fruit

TRAINING_COUNT = 8
TEST_ROUNDS = 10
K_NEIGHBOURS = 3


class FruitGame:
    def __init__(self,size,home):
        self.w,self.h=size; self.home=home; self.phase="training"; self.reset_training()

    def reset_training(self):
        self.phase="training"; self.training=[]; self.index=0
        self.current=make_fruit(); self.test_index=0; self.correct=0; self.score=0

    def train_model(self):
        self.phase="trained"

    def start_test(self):
        self.phase="test"; self.test_index=0; self.correct=0; self.score=0
        self.current=make_fruit()

    def event(self,event):
        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE: self.home(); return
        if event.type!=pygame.MOUSEBUTTONDOWN or event.button!=1: return
        p=event.pos
        if pygame.Rect(20,18,116,42).collidepoint(p): self.home(); return
        if pygame.Rect(self.w-150,18,130,42).collidepoint(p): self.phase="help"; return
        if self.phase=="training":
            if pygame.Rect(220,420,245,62).collidepoint(p): self.add_label("apple")
            elif pygame.Rect(635,420,245,62).collidepoint(p): self.add_label("orange")
            elif len(self.training)>=TRAINING_COUNT and pygame.Rect(self.w//2-110,545,220,55).collidepoint(p): self.train_model()
        elif self.phase=="trained":
            if pygame.Rect(self.w//2-125,500,250,60).collidepoint(p): self.start_test()
        elif self.phase=="test":
            if self.test_index>=TEST_ROUNDS:
                if pygame.Rect(self.w//2-275,585,170,50).collidepoint(p): self.reset_training()
                elif pygame.Rect(self.w//2-80,585,170,50).collidepoint(p): self.start_test()
                elif pygame.Rect(self.w//2+115,585,170,50).collidepoint(p): self.home()
            elif self.phase=="test" and self.test_index>=0 and not hasattr(self,"prediction"):
                if pygame.Rect(self.w//2-135,475,270,58).collidepoint(p): self.guess()
            elif hasattr(self,"prediction") and pygame.Rect(self.w//2-130,500,260,56).collidepoint(p): self.next_fruit()
        elif self.phase=="help": self.phase=self.previous_phase

    def add_label(self,label):
        if len(self.training)>=TRAINING_COUNT: return
        self.training.append((self.current["features"][:],label))
        self.current=make_fruit()

    def guess(self):
        self.prediction=knn_predict(self.training,self.current["features"])
        self.was_correct=self.prediction==self.current["kind"]
        if self.was_correct: self.correct+=1; self.score+=10

    def next_fruit(self):
        del self.prediction
        self.test_index+=1
        if self.test_index<TEST_ROUNDS: self.current=make_fruit()

    def update(self,dt): pass

    def draw(self,surface,t):
        draw_background(surface,t)
        text(surface,"AI FRUIT SORTING ROBOT",(self.w//2,35),36,INK,True,True)
        Button((20,18,116,42),"⌂ HOME",PURPLE,font_size=20).draw(surface,None,pygame.mouse.get_pos())
        Button((self.w-150,18,130,42),"LEARN AI",ORANGE,font_size=20).draw(surface,None,pygame.mouse.get_pos())
        if self.phase=="help":
            panel(surface,(170,105,760,500)); text(surface,"HOW DOES THE ROBOT LEARN?",(self.w//2,150),38,PURPLE,True,True)
            text(surface,"DATA: examples we show the robot",(240,220),27)
            text(surface,"TRAINING: teaching it from examples",(240,270),27)
            text(surface,"PREDICTION: its guess for a new fruit",(240,320),27)
            text(surface,"ACCURACY: how many guesses were right",(240,370),27)
            text(surface,"FRUIT EXAMPLES  →  ROBOT LEARNS  →  NEW FRUIT  →  GUESS",(self.w//2,455),23,PURPLE,True,True)
            Button((self.w//2-100,520,200,55),"GOT IT!",GREEN).draw(surface,None,pygame.mouse.get_pos()); return
        self.previous_phase=self.phase
        # Baskets and cartoon robot are shared across all stages.
        for x,label,color in [(175,"APPLE BASKET",(225,83,83)),(925,"ORANGE BASKET",(244,151,57))]:
            panel(surface,(x-85,190,170,190),WHITE)
            pygame.draw.rect(surface,color,(x-65,315,130,48),border_radius=10)
            text(surface,label,(x,210),19,INK,True,True)
            for j in range(3): draw_fruit(surface,x-38+j*38,290,"apple" if x<500 else "orange",.48)
        # Friendly robot, with blinking animated eyes.
        pygame.draw.rect(surface,(142,123,212),(480,160,140,120),border_radius=35)
        pygame.draw.rect(surface,(111,91,177),(505,275,90,65),border_radius=16)
        pygame.draw.circle(surface,WHITE,(520,208),16); pygame.draw.circle(surface,WHITE,(580,208),16)
        pygame.draw.circle(surface,INK,(520,210),7); pygame.draw.circle(surface,INK,(580,210),7)
        pygame.draw.arc(surface,INK,(525,220,50,32),0,3.14,3)
        pygame.draw.line(surface,(142,123,212),(480,215),(445,260),10); pygame.draw.line(surface,(142,123,212),(620,215),(655,260),10)
        if self.phase=="training":
            text(surface,"STEP 1: TEACH THE ROBOT",(self.w//2,120),29,INK,True,True)
            text(surface,f"Choose a label for this fruit  •  Example {len(self.training)+1} of {TRAINING_COUNT}",(self.w//2,400),25,INK,True)
            draw_fruit(surface,self.w//2,270,self.current["kind"],1.35)
            Button((220,420,245,62),"LABEL: APPLE",(222,80,91)).draw(surface,None,pygame.mouse.get_pos())
            Button((635,420,245,62),"LABEL: ORANGE",(240,145,49)).draw(surface,None,pygame.mouse.get_pos())
            # Data visibly accumulates as labeled dots.
            for i,(_,lab) in enumerate(self.training):
                x=self.w//2+(i-(TRAINING_COUNT-1)/2)*32
                pygame.draw.circle(surface,(225,83,83) if lab=="apple" else (244,151,57),(int(x),510),10)
            if len(self.training)==TRAINING_COUNT:
                Button((self.w//2-110,545,220,55),"TRAIN ROBOT",GREEN).draw(surface,None,pygame.mouse.get_pos())
        elif self.phase=="trained":
            text(surface,"ROBOT TRAINED!",(self.w//2,410),37,GREEN,True,True)
            text(surface,f"Your robot learned from {len(self.training)} examples.",(self.w//2,450),25,INK,True)
            Button((self.w//2-125,500,250,60),"TEST MY ROBOT",PURPLE).draw(surface,None,pygame.mouse.get_pos())
        elif self.phase=="test":
            text(surface,"STEP 2: CAN YOUR ROBOT GUESS?",(self.w//2,120),29,INK,True,True)
            draw_fruit(surface,self.w//2,270,self.current["kind"],1.35)
            # Feature meters make the numerical inputs concrete.
            text(surface,"Color",(415,340),20,INK); pygame.draw.rect(surface,(245,245,250),(480,346,160,13),border_radius=6)
            pygame.draw.rect(surface,(229,89,90),(480,346,int(self.current["features"][0]*160),13),border_radius=6)
            text(surface,"Size",(415,372),20,INK); pygame.draw.rect(surface,(245,245,250),(480,378,160,13),border_radius=6)
            pygame.draw.rect(surface,PURPLE,(480,378,int(self.current["features"][1]*160),13),border_radius=6)
            text(surface,f"Test {min(TEST_ROUNDS,self.test_index+1)} of {TEST_ROUNDS}   •   Score {self.score}",(self.w//2,430),22,INK,True)
            if self.test_index>=TEST_ROUNDS:
                accuracy=round(self.correct/TEST_ROUNDS*100)
                panel(surface,(255,445,590,125)); text(surface,"YOUR AI ROBOT RESULTS",(self.w//2,462),28,PURPLE,True,True)
                text(surface,f"Correct {self.correct}   Wrong {TEST_ROUNDS-self.correct}   Accuracy {accuracy}%   Score {self.score}",(self.w//2,500),24,INK,True)
                pygame.draw.rect(surface,(230,232,240),(330,517,440,14),border_radius=7); pygame.draw.rect(surface,GREEN,(330,517,int(4.4*accuracy),14),border_radius=7)
                Button((self.w//2-275,585,170,50),"TRAIN AGAIN",ORANGE,font_size=19).draw(surface,None,pygame.mouse.get_pos())
                Button((self.w//2-80,585,170,50),"TEST AGAIN",GREEN,font_size=19).draw(surface,None,pygame.mouse.get_pos())
                Button((self.w//2+115,585,170,50),"HOME",PURPLE,font_size=19).draw(surface,None,pygame.mouse.get_pos())
            elif hasattr(self,"prediction"):
                guess=self.prediction.upper()
                message=f"Robot says {guess}!  " + ("Correct! +10" if self.was_correct else f"Fruit was {self.current['kind'].upper()}. Let's learn more!")
                text(surface,message,(self.w//2,455),25,GREEN if self.was_correct else ORANGE,True,True)
                Button((self.w//2-130,500,260,56),"NEXT FRUIT",PURPLE).draw(surface,None,pygame.mouse.get_pos())
            else:
                Button((self.w//2-135,475,270,58),"ASK ROBOT TO GUESS",PURPLE).draw(surface,None,pygame.mouse.get_pos())
