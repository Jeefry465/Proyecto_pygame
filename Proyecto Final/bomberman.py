import pygame 
import time 
import random
from constantes import *

class Personaje:
    def __init__(self, x, y, animacion_jugador,energia, tipo):
        self.energia = energia
        self.vivo = True
        self.player = pygame.Rect(x, y, ANCHO_PERSONAJE - 10, ALTO_PERSONAJE - 10) # Crea un rectángulo que representa al jugador con su posición inicial y tamaño
        self.player.center = (x,y)
        self.animacion_jugador = animacion_jugador
        #inicializa el frame del jugador en 1
        self.frame = 0
        self.actualizar_tiempo = pygame.time.get_ticks() # Guarda el tiempo actual para controlar la animación
        self.imagen = self.animacion_jugador[self.frame] # Asigna la imagen del jugador desde la lista de animación
        self.flip = False # Variable para controlar la dirección de la imagen del jugador
        self.tipo = tipo  # Tipo de personaje (jugador o enemigo)

    def dibujar(self,ventana, desplazamiento_x = 0, desplazamiento_y = 0):
    
        # Selecciona la imagen volteada o normal según la dirección
        imagen_a_dibujar = pygame.transform.flip(self.imagen, self.flip, False)
        ventana.blit(imagen_a_dibujar, (self.player.x - desplazamiento_x, self.player.y - desplazamiento_y)) 

    def movimiento(self, dx, dy, paredes):
        nuevo_rect = self.player.move(dx, dy)
        if not any(nuevo_rect.colliderect(p) for p in paredes):
            self.player = nuevo_rect

        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False

        # Limita la posición al tamaño del mapa
        self.player.x = max(0, min(self.player.x, COLUMNAS * TAMANO_CUADRICULA - self.player.width))
        self.player.y = max(0, min(self.player.y, FILAS * TAMANO_CUADRICULA - self.player.height))
        
    
    # Actualiza la imagen del jugador
    def actualizar(self):
        #Comprobar si el jugador está vivo
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False  # Si la energía es menor o igual a 0, el jugador no está vivo
            
        tiempo_esperado = 200  # Tiempo en milisegundos entre cada cambio de imagen
        self.imagen = self.animacion_jugador[self.frame]  # Actualiza la imagen del jugador
        
        if pygame.time.get_ticks() - self.actualizar_tiempo >= tiempo_esperado:
            self.frame = self.frame + 1  # Avanza al siguiente frame que representa la siguiente imagen
            self.actualizar_tiempo = pygame.time.get_ticks()  # Actualiza el tiempo actual
        
        if self.frame >= len(self.animacion_jugador):
            self.frame = 0
        
        
    def mover_automatico(self, paredes):
        if self.tipo == 'enemigo':
            if not hasattr(self, 'contador'):
                self.contador = 0
                self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
            self.contador += 1
            if self.contador > 60:
                self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
                self.contador = 0

            dx, dy = 0, 0
            if self.direccion == 'arriba':
                dy = -VELOCIDAD_JUGADOR
            elif self.direccion == 'abajo':
                dy = VELOCIDAD_JUGADOR
            elif self.direccion == 'izquierda':
                dx = -VELOCIDAD_JUGADOR
            elif self.direccion == 'derecha':
                dx = VELOCIDAD_JUGADOR

            # Probar si puede moverse, si no, cambiar de dirección
            nuevo_rect = self.player.move(dx, dy)
            if not any(nuevo_rect.colliderect(p) for p in paredes):
                self.player = nuevo_rect
            else:
                # Cambia de dirección si hay colisión
                direcciones_posibles = ['arriba', 'abajo', 'izquierda', 'derecha']
                direcciones_posibles.remove(self.direccion)  # Evita repetir la misma dirección
                self.direccion = random.choice(direcciones_posibles)
        


class Bomba:
    def __init__(self, x, y, imagen_bomba, imagen_explosion, imagen_bomba_final, tiempo_expl=2):
        self.rect = pygame.Rect(x, y, imagen_bomba.get_width(), imagen_bomba.get_height())# Crea un rectángulo en la posición (x, y) de tamaño 20x20 para representar la bomba
        self.imagen_bomba = imagen_bomba # Asigna la imagen de la bomba
        self.imagen_explosion = imagen_explosion # Asigna la imagen de la explosión de la bomba 
        self.imagen_bomba_final = imagen_bomba_final # Asigna la imagen final de la bomba (opcional, si se usa en el juego)
        self.tiempo_colocdada = time.time() # Guarda el tiempo en que la bomba fue colocada
        self.tiempo_expl = tiempo_expl # Tiempo en segundos que tarda en explotar la bomba
        self.explotada = False # Tiempo en segundos que tarda en explotar la bomba
        self.tiempo_explotada = None # Guarda el tiempo en que la bomba explotó, inicialmente es None 
        self.jugador_danado = False  # bandera para indicar si ya se hizo daño al jugador
        self.sonido_explosion = pygame.mixer.Sound("Proyecto Final//Recursos//Music//retro-explode-1-236678.mp3")  # Carga el sonido de explosión
        self.sonido_explosion.set_volume(0.5)  # Ajusta el volumen del sonido de explosión

    def actualizar(self, lista_enemigos, jugador=None):
        ahora = time.time()
        if not self.explotada and (ahora - self.tiempo_colocdada) >= self.tiempo_expl:
            self.explotada = True
            self.tiempo_explotada = ahora
            self.sonido_explosion.play() # Reproduce el sonido de explosión

        if self.explotada:
            area_explosion = self.rect.inflate(120, 120)

            # Daño a los enemigos
            for enemi in lista_enemigos:
                if enemi.player.colliderect(area_explosion):
                    enemi.energia = 0

            # Daño al jugador - solo una vez
            if (jugador 
                and not self.jugador_danado 
                and jugador.player.colliderect(area_explosion)):
                jugador.energia = max(1, jugador.energia - 33)
                self.jugador_danado = True  # marcamos que ya se aplicó el daño

            # Quitar la bomba tras 0.5s
            if (ahora - self.tiempo_explotada) >= 0.5:
                return True

        return False # Si la bomba no ha explotado o no ha pasado el tiempo de explosión, devuelve False para indicar que no debe eliminarse

            

    def dibujar(self, ventana, desplazamiento_x = 0, desplazamiento_y = 0):
        
        # Si la bomba no ha explotado, dibuja un rectángulo negro (la bomba)
        if not self.explotada:
            ventana.blit(self.imagen_bomba, (self.rect.x - desplazamiento_x, self.rect.y - desplazamiento_y)) # 
        else:
            tiempo_explosion = time.time() - self.tiempo_explotada
            # Mostrar la explosión durante 0.3s, luego la imagen final hasta eliminar
            if tiempo_explosion < 0.3:
                # Centro de la explosión
                x_centro = self.rect.x - desplazamiento_x - (self.imagen_explosion.get_width() - self.rect.width)//2
                y_centro = self.rect.y - desplazamiento_y - (self.imagen_explosion.get_height() - self.rect.height)//2
                ventana.blit(self.imagen_explosion, (x_centro, y_centro))
                
                # Brazos (hacia cada dirección)
                rango_extra = 60
                ventana.blit(self.imagen_explosion, (x_centro - rango_extra, y_centro))  # Izquierda
                ventana.blit(self.imagen_explosion, (x_centro + rango_extra, y_centro))  # Derecha
                ventana.blit(self.imagen_explosion, (x_centro, y_centro - rango_extra))  # Arriba
                ventana.blit(self.imagen_explosion, (x_centro, y_centro + rango_extra))  # Abajo
            else:
                ventana.blit(self.imagen_bomba_final, (self.rect.x - desplazamiento_x, self.rect.y - desplazamiento_y))


