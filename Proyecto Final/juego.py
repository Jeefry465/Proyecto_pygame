import pygame
import sys 
from bomberman import Personaje, Bomba
from constantes import *


# Inicializar pygame
if __name__ == '__main__':
    pygame.init()

    # Crear una ventana
    ventana = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("BomberMan")

    animacion_jugador = []
    #for i in range(7):
        #img = pygame.image.load(f"Proyecto Final//Recursos//Imagenes_personaje//{i}.png")

    #Se carga una imagen del jugador 
    imagen_jugador = pygame.image.load("Proyecto Final//Recursos//Imagenes_personaje//1.png")

    #Tamaño de la imagen del jugador
    imagen_jugador = pygame.transform.scale(imagen_jugador,(imagen_jugador.get_width()*TAMANO, imagen_jugador.get_height()*TAMANO))

    # Se crea el jugador,posicion en el plano, adopta imagen jugador la cual es la imagen 1
    jugador = Personaje(30,30,imagen_jugador)

#Variables de movimiento del personaje.

    mover_arriba = False
    mover_abajo = False
    mover_izquierda = False
    mover_derecha = False

    # Se crea un reloj para controlar la velocidad de fotogramas
    reloj = pygame.time.Clock()

    bombas = []

    # Bucle principal
    while True:

        # Controlar la velocidad de fotogramas
        reloj.tick(FPS)

        #Movimiento del jugador
        eje_x = 0
        eje_y = 0

        if mover_derecha == True:
            eje_x = VELOCIDAD_JUGADOR

        if mover_izquierda == True:
            eje_x = -VELOCIDAD_JUGADOR

        if mover_arriba == True:
            eje_y = -VELOCIDAD_JUGADOR

        if mover_abajo == True:
            eje_y = VELOCIDAD_JUGADOR


        #hacer mover al jugador
        jugador.movimiento(eje_x, eje_y)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Se crea un evento el cual si apretamos una tecla va hacer un movimiento
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_a:
                   mover_izquierda = True

                if evento.key == pygame.K_d:
                    mover_derecha = True
                
                if evento.key == pygame.K_w:
                    mover_arriba = True
                
                if evento.key == pygame.K_s:
                    mover_abajo = True
            #Se crea un evento el cual si soltamos una tecla va dejar de moverse        
            if evento.type == pygame.KEYUP:

                if evento.key == pygame.K_a:
                    mover_izquierda = False

                if evento.key == pygame.K_d:
                    mover_derecha = False
                
                if evento.key == pygame.K_w:
                    mover_arriba = False
                
                if evento.key == pygame.K_s:
                    mover_abajo = False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE:
                    bombas.append(Bomba(jugador.player.x, jugador.player.y))
        
        # Llenar la pantalla con un color
        ventana.fill(BLANCO)

        for bomba in bombas:
            bomba.actualizar()
            bomba.dibujar(ventana)

        # Dibujar el jugador
        jugador.dibujar(ventana)

        # Actualizar la pantalla
        pygame.display.update()

