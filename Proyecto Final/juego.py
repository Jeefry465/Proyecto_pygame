import pygame
import sys 
from bomberman import Personaje, Bomba
from constantes import *
import os
from mundo import Mundo
import csv

def mostrar_game_over(ventana):
    game_over_fuente = pygame.font.SysFont(None, 80)
    game_over_texto = game_over_fuente.render("GAME OVER", True, (255, 0, 0)) # Renderiza el texto "GAME OVER" en rojo
    ventana.fill((0, 0, 0)) # Rellena la ventana
    ventana.blit(game_over_texto, (ventana.get_width() // 2 - game_over_texto.get_width() // 2, ventana.get_height() // 2 - game_over_texto.get_height() // 2)) # Centra el texto en la ventana

    pygame.display.update() # Actualiza la pantalla para mostrar el texto

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
    ventana = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("BomberMan")

    posicion_pantalla = [0, 0]

    #Importar barra de energia
    corazon_vacio = pygame.image.load("Proyecto Final//Recursos//Corazon Vida//barra1.png").convert_alpha()
    corazon_lleno = pygame.image.load("Proyecto Final//Recursos//Corazon Vida//barra2.png").convert_alpha()
    corazon_vacio = tamano_imagenes(corazon_vacio, TAMANO_COARAZON)
    corazon_lleno = tamano_imagenes(corazon_lleno, TAMANO_COARAZON)

    # Cargar imágenes del mapa
    mapa_list = []
    for i in range(425):
        imagen = pygame.image.load(f"Proyecto Final//Recursos//Imagenes Mapa//mapa_{i+1}.png").convert_alpha()
        imagen = pygame.transform.scale(imagen,(TAMANO_CUADRICULA, TAMANO_CUADRICULA))
        # Ajustar el tamaño de la imagen al tamaño de la cuadrícula
        mapa_list.append(imagen)

    animacion_jugador = []

    for i in range(1,7):
        img = pygame.image.load(f"Proyecto Final//Recursos//Imagenes_personaje//imagen{i}.png")
        img = pygame.transform.scale(img, (ANCHO_PERSONAJE, ALTO_PERSONAJE)) # Ajusta el tamaño de la imagen al tamaño del personaje

        animacion_jugador.append(img)
    
    #Imagens de los enemigos
    carpeta_enemigos = "Proyecto Final/Recursos/Enemigos"
    clase_enemigos = nombre_carpeta(carpeta_enemigos)
    animacion_enemigos = []

    for enemi in clase_enemigos: # Recorre cada enemigo en la carpeta
        # Crea una lista temporal para almacenar las imágenes de cada enemigo
        lista_temporal = []
        ruta_temporal = f"Proyecto Final/Recursos/Enemigos/{enemi}"
        numero_animacion = contar_carpeta(ruta_temporal)
        print(f"Numero de animaciones de {enemi}: {numero_animacion}")

        for i in range(1, numero_animacion + 1): # Carga las imágenes de cada enemigo

            ruta_imagen = f"{ruta_temporal}/{enemi}{i}.png"
            try: # Intenta cargar la imagen
                imagen_enemigo = pygame.image.load(ruta_imagen).convert_alpha() # Convierte la imagen para que sea compatible con Pygame
                # Ajusta el tamaño de la imagen al tamaño del enemigo
                imagen_enemigo = pygame.transform.scale(imagen_enemigo, (TAMANO_ENEMIGO, TAMANO_ENEMIGO)) # Ajusta el tamaño de la imagen al tamaño del enemigo
                lista_temporal.append(imagen_enemigo)
            except Exception as e: # Si ocurre un error al cargar la imagen, imprime un mensaje de error
                # Manejo de errores al cargar la imagen
                print(f"No se pudo cargar la imagen: {ruta_imagen} - {e}")

        animacion_enemigos.append(lista_temporal)
    

    #Vida jugador 
    def vida_jugador():
        for i in range(3): # Dibujar 3 corazones
            if jugador.energia >= (i + 1) * 33: # Corazones llenos
                ventana.blit(corazon_lleno, (10 + i * 40, 10)) # Posición de los corazones
            else:
                ventana.blit(corazon_vacio, (10 + i * 40, 10)) # Posición de los corazones

    #Matriz del mundo del juego
    mundo_data = []

    for fila in range(FILAS):
        filas = [58] * COLUMNAS # Valor por defecto para cada celda
        mundo_data.append(filas) # Añadir la fila a la matriz

    #Cargar el archivo que contine el nivel 
    with open("Proyecto Final//Recursos//Niveles//Mapa1.1.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';') # Lea el archivo CSV 
        for x, fila in enumerate(reader): # Recorre cada fila del archivo CSV
            if x < FILAS: # Asegúrese de que no exceda el número de filas
                for y, columna in enumerate(fila): # Recorre cada columna de la fila
                    if y < COLUMNAS: # Asegúrese de que no exceda el número de columnas
                        if columna.strip() == '': # Si la celda está vacía, asigna un valor por defecto
                            mundo_data[x][y] = 0  # Valor por defecto si la celda está vacía
                        else:
                            mundo_data[x][y] = int(columna) # Asigna el valor de la celda del CSV a la matriz

    mundo = Mundo() # Crear una instancia de la clase Mundo
    mundo.cargar_mundo(mundo_data, mapa_list) # Cargar el mundo con los datos y las imágenes del mapa

    #Se dibuja una cuadricula en la pantalla
    def dibujar_cuadricula():
        for x in range(30): # Dibujar lineas verticales y horizontales
            pygame.draw.line(ventana, GRIS, (x * TAMANO_CUADRICULA, 0), (x * TAMANO_CUADRICULA, 1000)) # Linea vertical
            pygame.draw.line(ventana, GRIS, (0, x * TAMANO_CUADRICULA ), (1000, x * TAMANO_CUADRICULA)) # Linea horizontal

    # Se crea el jugador,posicion en el plano, adopta imagen jugador la cual es la imagen 1
    jugador = Personaje(80,80,animacion_jugador, energia = 100, tipo='jugador')

    #Se crea los enemigos que adopta la clase personaje 
    enemigo1 = Personaje(400,500,animacion_enemigos[0], energia = 100, tipo='enemigo')
    enemigo2 = Personaje(600,300,animacion_enemigos[1], energia =100, tipo='enemigo')
    enemigo3 = Personaje(800,200,animacion_enemigos[2], energia = 100, tipo='enemigo')
    enemigo4 = Personaje(200,100,animacion_enemigos[3] ,energia = 100, tipo='enemigo')
    
    

    #Crear lista de enemigos en donde vamos a añadir cada uno de ellos 
    lista_enemigos = []
    lista_enemigos.append(enemigo1)
    lista_enemigos.append(enemigo2) 
    lista_enemigos.append(enemigo3)
    lista_enemigos.append(enemigo4)
    


#Variables de movimiento del personaje.

    mover_arriba = False
    mover_abajo = False
    mover_izquierda = False
    mover_derecha = False

    # Se crea un reloj para controlar la velocidad de fotogramas
    reloj = pygame.time.Clock()

    # Imagenes de la bomba
    imagen_bomba = tamano_imagenes(pygame.image.load("Proyecto Final//Recursos//Bomba//bomba_1.png").convert_alpha(), TAMANO_BOMBA)
    imagen_explosion = tamano_imagenes(pygame.image.load("Proyecto Final//Recursos//Bomba//bomba_2.png").convert_alpha(), TAMANO_BOMBA)
    imagen_bomba_final = tamano_imagenes(pygame.image.load("Proyecto Final//Recursos//Bomba//bomba_3.png").convert_alpha(), TAMANO_BOMBA)

    bombas = []

    game_over = False # Variable para controlar el estado del juego

    # Bucle principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Eventos de teclado solo si el juego NO ha terminado
            if not game_over:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_a:
                        mover_izquierda = True
                    if evento.key == pygame.K_d:
                        mover_derecha = True
                    if evento.key == pygame.K_w:
                        mover_arriba = True
                    if evento.key == pygame.K_s:
                        mover_abajo = True
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
                        if len(bombas) < MAX_BOMBAS:
                            bombas.append(Bomba(jugador.player.x, jugador.player.y, imagen_bomba, imagen_explosion, imagen_bomba_final))

        if not game_over:
            # Controlar la velocidad de fotogramas
            reloj.tick(FPS)

            # Movimiento del jugador
            eje_x = 0
            eje_y = 0
            if mover_derecha:
                eje_x = VELOCIDAD_JUGADOR
            if mover_izquierda:
                eje_x = -VELOCIDAD_JUGADOR
            if mover_arriba:
                eje_y = -VELOCIDAD_JUGADOR
            if mover_abajo:
                eje_y = VELOCIDAD_JUGADOR

            jugador.actualizar()

            desplazamiento_x = jugador.player.x - ventana.get_width() // 2
            desplazamiento_y = jugador.player.y - ventana.get_height() // 2
            maximo_desplazamiento_x = (COLUMNAS * TAMANO_CUADRICULA) - ventana.get_width()
            maximo_desplazamiento_y = (FILAS * TAMANO_CUADRICULA) - ventana.get_height()
            maximo_desplazamiento_x = max(0, maximo_desplazamiento_x)
            maximo_desplazamiento_y = max(0, maximo_desplazamiento_y)
            desplazamiento_x = max(0, min(desplazamiento_x, maximo_desplazamiento_x))
            desplazamiento_y = max(0, min(desplazamiento_y, maximo_desplazamiento_y))

            for enemi in lista_enemigos:
                enemi.actualizar()

            posicion_pantalla = jugador.movimiento(eje_x, eje_y)

            # Llenar la pantalla con un color
            ventana.fill(BLANCO)
            dibujar_cuadricula()
            mundo.dibujar_mundo(ventana, desplazamiento_x, desplazamiento_y)

            nuevas_bombas = []
            for bomba in bombas:
                eliminar = bomba.actualizar(lista_enemigos)
                bomba.dibujar(ventana, desplazamiento_x, desplazamiento_y)
                if not eliminar:
                    nuevas_bombas.append(bomba)
            bombas = nuevas_bombas

            jugador.dibujar(ventana, desplazamiento_x, desplazamiento_y)
            for enemi in lista_enemigos:
                enemi.dibujar(ventana, desplazamiento_x, desplazamiento_y)

            for enemi in lista_enemigos:
                enemi.mover_automatico()
                enemi.actualizar()

            # Comprobar colisiones entre el jugador y los enemigos
            for enemi in lista_enemigos:
                if jugador.player.colliderect(enemi.player):
                    jugador.energia -= 1

            # Comprobar si el jugador ha muerto
            if jugador.energia <= 0:
                game_over = True

            vida_jugador()
            pygame.display.update()

        else:
            mostrar_game_over(ventana)
            # Espera a que el usuario cierre la ventana
            # (ya se procesan eventos arriba, así que aquí solo se muestra la pantalla)

