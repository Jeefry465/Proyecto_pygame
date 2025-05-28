import pygame
import sys 
from bomberman import Personaje, Bomba
from constantes import *
import os


  #Funcion que ayuda a ajustar el tamaño de las imagenes 
def tamano_imagenes(imagen,tamano):
    ancho = imagen.get_width()
    alto = imagen.get_height()
    nueva_imagen = pygame.transform.scale(imagen, (int(ancho * tamano), int(alto * tamano)))

    return nueva_imagen 

#Funcion para contar elementos(Carpetas de enemigos)
def contar_carpeta(carpeta):
    return len(os.listdir(carpeta))

#Funcion listar nombre elementos 
def nombre_carpeta(carpeta):
    return os.listdir(carpeta)

# Inicializar pygame
if __name__ == '__main__':
    pygame.init()

    # Crear una ventana
    ventana = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("BomberMan")

  

    animacion_jugador = []

    for i in range(1,7):
        img = pygame.image.load(f"Proyecto Final//Recursos//Imagenes_personaje//imagen{i}.png")
        img = tamano_imagenes(img, TAMANO)

        animacion_jugador.append(img)
    
    #Imagens de los enemigos
    carpeta_enemigos = "Proyecto Final/Recursos/Enemigos"
    clase_enemigos = nombre_carpeta(carpeta_enemigos)
    animacion_enemigos = []

    for enemi in clase_enemigos:
        lista_temporal = []
        ruta_temporal = f"Proyecto Final/Recursos/Enemigos/{enemi}"
        numero_animacion = contar_carpeta(ruta_temporal)
        print(f"Numero de animaciones de {enemi}: {numero_animacion}")

        """for i in range(numero_animacion):
            imagen_enemigo = pygame.image.load(f"{ruta_temporal}//{enemi}.{i + 1}.png").convert_alpha()
            imagen_enemigo = tamano_imagenes(imagen_enemigo, TAMANO_ENEMIGO)
            lista_temporal.append(imagen_enemigo)

        animacion_enemigos.append(lista_temporal)"""
    




    # Se crea el jugador,posicion en el plano, adopta imagen jugador la cual es la imagen 1
    jugador = Personaje(30,30,animacion_jugador)

    #Se crea los enemigos que adopta la clase personaje 
    """enemigo1 = Personaje(400,500,animacion_enemigos[0])
    enemigo2 = Personaje(800,700,animacion_enemigos[1])

    #Crear lista de enemigos en donde vamos a añadir cada uno de ellos 
    lista_enemigos = []
    lista_enemigos.append(enemigo1)
    lista_enemigos.append(enemigo2)"""



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



        # Actualizar el jugador
        jugador.actualizar()

        #Actualizar enemigo
        """for enemi in lista_enemigos:
            enemi.actualizar()"""


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

        # Dibujar enemigo
        """for enemi in lista_enemigos:
            enemi.dibujar(ventana)"""
        

        # Actualizar la pantalla
        pygame.display.update()

