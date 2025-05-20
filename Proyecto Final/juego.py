import pygame
import sys 
from bomberman import Personaje


# Inicializar pygame
if __name__ == '__main__':
    pygame.init()

    # Crear una ventana
    ventana = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("BomberMan")

    # Se crea el jugador, forma actual caudrado y posicion en el plano
    jugador = Personaje(160,300)

    # Color fondo
    BLANCO = (255, 255, 255)

#Variables de movimiento del personaje.

    mover_arriba = False
    mover_abajo = False
    mover_izquierda = False
    mover_derecha = False

    # Bucle principal
    while True:

        #Movimiento del jugador
        eje_x = 0
        eje_y = 0

        if mover_derecha == True:
            eje_x = 5

        if mover_izquierda == True:
            eje_x = -5

        if mover_arriba == True:
            eje_y = -5

        if mover_abajo == True:
            eje_y = 5

        #hacer mover al jugador
        Personaje.movimiento(eje_x, eje_y)

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
                    


        # Llenar la pantalla con un color
        ventana.fill(BLANCO)

        # Dibujar el jugador
        jugador.dibujar(ventana)

        # Actualizar la pantalla
        pygame.display.update()

