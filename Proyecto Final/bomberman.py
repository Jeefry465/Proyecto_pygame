import pygame 

class Personaje:
    def init__(self, x, y):
        self.player = pygame.Rect(0, 0, 20, 20)
        self.player.center = (x,y)
    
    def dibujar(self,ventana):
        pygame.draw.rect(ventana, (255,255,0), self.player)