import pygame
import sys 
from bomberman import Personaje


# Inicializar pygame
if __name__ == '__main__':
    pygame.init()

    # Crear una ventana
    ventana = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("BomberMan")

    # Se crea el jugador, forma actual caudrado
    jugador = Personaje(34,34)

    # Colores
    BLANCO = (255, 255, 255)

    # Bucle principal
    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Llenar la pantalla con un color
        ventana.fill(BLANCO)

        # Dibujar el jugador
        jugador.dibujar(ventana)

        # Actualizar la pantalla
        pygame.display.update()

