import pygame 

class Personaje:
    def __init__(self, x, y):
        self.player = pygame.Rect(0, 0, 20, 20)
        self.player.center = (x,y)
    
    def dibujar(self,ventana):
        pygame.draw.rect(ventana, (255,255,0), self.player)

    def movimiento(self, eje_x, eje_y):
        self.player.x = self.player.x + eje_x
        self.player.y = self.player.y + eje_y
