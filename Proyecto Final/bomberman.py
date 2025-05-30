import pygame 
import time 
import math
import random

class Personaje:
    def __init__(self, x, y, animacion_jugador,energia):
        self.energia = energia
        self.player = pygame.Rect(0, 0, 20, 20)
        self.player.center = (x,y)
        self.animacion_jugador = animacion_jugador
        #inicializa el frame del jugador en 1
        self.frame = 0
        self.actualizar_tiempo = pygame.time.get_ticks() # Guarda el tiempo actual para controlar la animación
        self.imagen = self.animacion_jugador[self.frame] # Asigna la imagen del jugador desde la lista de animación
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

    # Actualiza la imagen del jugador
    def actualizar(self):
        tiempo_esperado = 200  # Tiempo en milisegundos entre cada cambio de imagen
        self.imagen = self.animacion_jugador[self.frame]  # Actualiza la imagen del jugador
        
        if pygame.time.get_ticks() - self.actualizar_tiempo >= tiempo_esperado:
            self.frame = self.frame + 1  # Avanza al siguiente frame que representa la siguiente imagen
            self.actualizar_tiempo = pygame.time.get_ticks()  # Actualiza el tiempo actual
        
        if self.frame >= len(self.animacion_jugador):
            self.frame = 0
        



class Bomba:

    def __init__(self, x, y, tiempo_expl = 3):
        self.rect = pygame.Rect(x, y, 20, 20) # Crea un rectángulo en la posición (x, y) de tamaño 20x20 para representar la bomba
        self.tiempo_colocdada = time.time() # Guarda el tiempo en que la bomba fue colocada
        self.tiempo_expl = tiempo_expl # Tiempo en segundos que tarda en explotar la bomba
        self.explotada = False # Tiempo en segundos que tarda en explotar la bomba
        self.tiempo_explotada = None # Guarda el tiempo en que la bomba explotó, inicialmente es None

    def actualizar(self,lista_enemigos):
        ahora = time.time() # Obtiene el tiempo actual en segundos
        #Si la bomba no ha explotado y han pasado el tiempo de explosión, cambia su estado a explotada
        if not self.explotada and (ahora - self.tiempo_colocdada ) >= self.tiempo_expl:
            self.explotada = True
            self.tiempo_explotada = ahora 

        #verificar colision con enenmigos
        if self.explotada:
            area = self.rect.inflate(40, 40)
            for enemi in lista_enemigos:
                if enemi.player.colliderect(area):
                    daño = 15 + random.randint(-7, 7)
                    enemi.energia -= daño
            # Si han pasado 0.5 s desde la explosión, indícale al juego que elimine el rectángulo de la bomba
            if (ahora - self.tiempo_explotada) >= 0.5:
                return True
            
        return False # Si la bomba no ha explotado o no ha pasado el tiempo de explosión, devuelve False para indicar que no debe eliminarse

            

    def dibujar(self, ventana):
        # Si la bomba no ha explotado, dibuja un rectángulo negro (la bomba)
        if not self.explotada:
            pygame.draw.rect(ventana, (0, 0, 0), self.rect)
        else:
            pygame.draw.rect(ventana, (255, 0, 0), self.rect.inflate(40, 40)) # Si explotó, dibuja un rectángulo rojo más grande para simular la explosión
            

    