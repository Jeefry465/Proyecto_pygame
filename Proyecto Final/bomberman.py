import pygame 
import time 

class Personaje:
    def __init__(self, x, y,imagen):
        self.player = pygame.Rect(0, 0, 20, 20)
        self.player.center = (x,y)
        self.imagen = imagen
        self.flip = False # Variable para controlar la dirección de la imagen del jugador
    
    def dibujar(self,ventana):
        # Selecciona la imagen volteada o normal según la dirección
        imagen_a_dibujar = pygame.transform.flip(self.imagen, self.flip, False)
        ventana.blit(imagen_a_dibujar, self.player)
       

    def movimiento(self, eje_x, eje_y):
        if eje_x < 0:
            self.flip = True
        elif eje_x > 0:
            self.flip = False

        self.player.x = self.player.x + eje_x
        self.player.y = self.player.y + eje_y




class Bomba:

    def __init__(self, x, y, tiempo_expl = 3):
        self.rect = pygame.Rect(x, y, 20, 20) # Crea un rectángulo en la posición (x, y) de tamaño 20x20 para representar la bomba
        self.tiempo_colocdada = time.time() # Guarda el tiempo en que la bomba fue colocada
        self.tiempo_expl = tiempo_expl # Tiempo en segundos que tarda en explotar la bomba
        self.explotada = False # Tiempo en segundos que tarda en explotar la bomba

    def actualizar(self):
        if not self.explotada and time.time() - self.tiempo_colocdada >= self.tiempo_expl:
            self.explotada = True
            

    def dibujar(self, ventana):
        # Si la bomba no ha explotado, dibuja un rectángulo negro (la bomba)
        if not self.explotada:
            pygame.draw.rect(ventana, (0, 0, 0), self.rect)
        else:
            pygame.draw.rect(ventana, (255, 0, 0), self.rect.inflate(40, 40)) # Si explotó, dibuja un rectángulo rojo más grande para simular la explosión
            
