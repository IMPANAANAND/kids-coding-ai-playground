"""Shared drawing helpers for Kids Coding & AI Playground."""
import math
import pygame

SKY = (100, 190, 248)
PURPLE = (111, 78, 190)
YELLOW = (255, 211, 76)
GREEN = (82, 190, 128)
ORANGE = (255, 151, 76)
PINK = (244, 112, 163)
INK = (46, 57, 85)
WHITE = (255, 255, 255)
PALE = (246, 249, 255)


class Button:
    """A simple rounded button; click handling is shared by every screen."""
    def __init__(self, rect, label, color=PURPLE, text_color=WHITE, font_size=22):
        self.rect = pygame.Rect(rect)
        self.label, self.color, self.text_color, self.font_size = label, color, text_color, font_size

    def draw(self, surface, font, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        shade = tuple(min(255, c + (16 if hovered else 0)) for c in self.color)
        pygame.draw.rect(surface, (35, 48, 79, 35), self.rect.move(0, 4), border_radius=18)
        pygame.draw.rect(surface, shade, self.rect, border_radius=18)
        label_font = pygame.font.Font(None, self.font_size)
        text = label_font.render(self.label, True, self.text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def hit(self, pos):
        return self.rect.collidepoint(pos)


def text(surface, message, pos, size=28, color=INK, center=False, bold=False):
    font = pygame.font.Font(None, size)
    font.set_bold(bold)
    image = font.render(str(message), True, color)
    rect = image.get_rect(center=pos) if center else image.get_rect(topleft=pos)
    surface.blit(image, rect)
    return rect


def panel(surface, rect, color=WHITE, radius=22):
    pygame.draw.rect(surface, color, pygame.Rect(rect), border_radius=radius)


def draw_background(surface, t=0):
    w, h = surface.get_size()
    surface.fill((220, 241, 255))
    for y in range(h):
        frac = y / max(1, h)
        pygame.draw.line(surface, (int(112+80*frac), int(190+38*frac), 249), (0, y), (w, y))
    for i in range(9):
        x = int((i * 173 + (t * (8 + i % 3))) % (w + 100)) - 50
        y = 35 + (i * 83) % 330
        pygame.draw.circle(surface, (255,255,255,150), (x,y), 3 + i % 3)


def draw_balloon(surface, x, y, color, scale=1, bomb=False):
    x, y = int(x), int(y)
    w, h = int(42*scale), int(54*scale)
    pygame.draw.ellipse(surface, color, (x-w//2, y-h//2, w, h))
    pygame.draw.ellipse(surface, tuple(min(255,c+60) for c in color), (x-w//3, y-h//3, max(3,w//5), max(5,h//3)))
    pygame.draw.polygon(surface, color, [(x-5,y+h//2-2),(x+5,y+h//2-2),(x,y+h//2+6)])
    pygame.draw.line(surface, (90,95,115), (x,y+h//2+6),(x+int(5*scale),y+int(45*scale)),1)
    if bomb:
        text(surface, "!", (x,y), 28, WHITE, center=True, bold=True)


def draw_fruit(surface, x, y, kind, size=1.0):
    """Draw an original, font-independent apple or orange illustration."""
    r = int(26*size)
    if kind == "apple":
        c = (225, 65, 78)
        pygame.draw.circle(surface, c, (int(x-r*.42),int(y)), int(r*.62))
        pygame.draw.circle(surface, c, (int(x+r*.42),int(y)), int(r*.62))
        pygame.draw.ellipse(surface, c, (int(x-r*.9),int(y-r*.2),int(r*1.8),int(r*1.45)))
        pygame.draw.line(surface, (100,70,45),(int(x),int(y-r*.65)),(int(x+2),int(y-r*1.05)),3)
        pygame.draw.ellipse(surface,(65,170,90),(int(x+1),int(y-r*1.1),int(r*.65),int(r*.3)))
        pygame.draw.ellipse(surface,(255,165,160),(int(x-r*.55),int(y-r*.35),int(r*.22),int(r*.45)))
    else:
        pygame.draw.circle(surface, (247, 151, 47), (int(x),int(y)), r)
        pygame.draw.ellipse(surface,(255,193,98),(int(x-r*.48),int(y-r*.55),int(r*.36),int(r*.58)))
        pygame.draw.circle(surface,(255,181,69),(int(x-r*.72),int(y-r*.8)),max(2,r//9))
        pygame.draw.line(surface,(100,70,45),(int(x),int(y-r*.9)),(int(x+2),int(y-r*1.2)),3)
        pygame.draw.ellipse(surface,(65,170,90),(int(x+1),int(y-r*1.25),int(r*.65),int(r*.3)))
