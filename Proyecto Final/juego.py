import pygame
import sys 
from bomberman import Personaje, Bomba
from constantes import *
import os
from mundo import Mundo
import csv

def pantalla_inicio(ventana):
    """Muestra la pantalla de inicio con dos botones: Iniciar y Salir."""
    # Fuentes y texto
    fondo = pygame.image.load("Proyecto Final//Recursos//Imagen fondo//fondo.jpg").convert_alpha()
    fondo = pygame.transform.scale(fondo, (ventana.get_width(), ventana.get_height()))  # Ajusta el fondo al tamaño de la ventana 

    fuente = pygame.font.SysFont(None, 50)
    titulo = fuente.render("Bienvenido a Grid Blast", True, (255, 255, 255))

    #rectángulos para ubicar los botones en pantalla
    boton_iniciar = pygame.Rect(ventana.get_width()//2 - 100, 300, 200, 50)
    boton_salir = pygame.Rect(ventana.get_width()//2 - 100, 400, 200, 50)

    while True:
        ventana.blit(fondo, (0, 0))
        ventana.blit(titulo, (ventana.get_width()//2 - titulo.get_width()//2, 150))

        # Dibujamos los botones
        pygame.draw.rect(ventana, (0, 200, 0), boton_iniciar)  # color verde
        pygame.draw.rect(ventana, (200, 0, 0), boton_salir)    # color rojo

        texto_iniciar = fuente.render("Iniciar", True, (255, 255, 255))
        texto_salir = fuente.render("Salir", True, (255, 255, 255))

        ventana.blit(texto_iniciar, (boton_iniciar.centerx - texto_iniciar.get_width()//2,boton_iniciar.centery - texto_iniciar.get_height()//2))
        ventana.blit(texto_salir,(boton_salir.centerx - texto_salir.get_width()//2,boton_salir.centery - texto_salir.get_height()//2))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # clic izquierdo
                    if boton_iniciar.collidepoint(evento.pos):
                        return  # salir de esta función y continuar el juego
                    elif boton_salir.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()

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
def main():
    pygame.init()

    #inicializar el mixer de pygame y cargar el sonido de fondo
    pygame.mixer.init()
    pygame.mixer.music.load("Proyecto Final//Recursos//Music//exploration-chiptune-rpg-adventure-theme-336428.mp3") # Cargar música de fondo
    pygame.mixer.music.set_volume(0.5)  # Ajustar volumen de la música
    pygame.mixer.music.play(-1)  # Reproducir música en bucle


    # Crear una ventana
    ventana = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Grid Blast")

    pantalla_inicio(ventana)  # Mostrar pantalla de inicio
    

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
        reader = csv.reader(csvfile, delimiter = ',') # Lea el archivo CSV 
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
    enemigo1 = Personaje(410,570,animacion_enemigos[0], energia = 100, tipo='enemigo')
    enemigo2 = Personaje(610,370,animacion_enemigos[1], energia =100, tipo='enemigo')
    enemigo3 = Personaje(800,270,animacion_enemigos[2], energia = 100, tipo='enemigo')
    enemigo4 = Personaje(200,170,animacion_enemigos[3] ,energia = 100, tipo='enemigo')
    
    

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
    victoria = False # Variable para controlar el estado de victoria

    score = 0 # Inicializar el score del jugador

    # Bucle principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Eventos de teclado solo si el juego NO ha terminado
            if not game_over and not victoria:
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

        if not game_over and not victoria:
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

            
            paredes_base = []
            for y, fila in enumerate(mundo_data):
                for x, valor in enumerate(fila):
                    if valor in [205,3,20,71,105,122,4,263,262,264,372,389,388,382,126,127,128,125,124,123]:
                        rect = pygame.Rect(x * TAMANO_CUADRICULA,y *TAMANO_CUADRICULA,TAMANO_CUADRICULA,TAMANO_CUADRICULA)
                        paredes_base.append(rect)

    
            paredes_jugador = list(paredes_base)
            for bomba in bombas:
                # Si la bomba no colisiona con el jugador, añádela
                if not bomba.rect.colliderect(jugador.player):
                    paredes_jugador.append(bomba.rect)

            # Construye paredes para los enemigos (incluye todas las bombas)
            paredes_enemigos = paredes_base + [b.rect for b in bombas]

            # Mueve al jugador usando su lista
            posicion_pantalla = jugador.movimiento(eje_x, eje_y, paredes_jugador)

            # Mueve a los enemigos usando su lista
            for enemi in lista_enemigos:
                enemi.mover_automatico(paredes_enemigos)
                enemi.actualizar()

            paredes = []
            for y, fila in enumerate(mundo_data):
                for x, valor in enumerate(fila):
                    if valor in [205,3,20,71,105,122,4,263,262,264,372,389,388,382,126,127,128,125,124,123]:  
                        rect = pygame.Rect(x * TAMANO_CUADRICULA, y * TAMANO_CUADRICULA, TAMANO_CUADRICULA, TAMANO_CUADRICULA)
                        paredes.append(rect)
            #Añadir colision de las bombasw
            for bomba in bombas:
                paredes.append(bomba.rect)

            # Llenar la pantalla con un color
            ventana.fill(BLANCO)
            dibujar_cuadricula()
            mundo.dibujar_mundo(ventana, desplazamiento_x, desplazamiento_y)

            nuevas_bombas = []
            for bomba in bombas:
                eliminar = bomba.actualizar(lista_enemigos, jugador)
                bomba.dibujar(ventana, desplazamiento_x, desplazamiento_y)
                if not eliminar:
                    nuevas_bombas.append(bomba)
            bombas = nuevas_bombas

            jugador.dibujar(ventana, desplazamiento_x, desplazamiento_y)
            for enemi in lista_enemigos:
                enemi.dibujar(ventana, desplazamiento_x, desplazamiento_y)

            # Eliminar enemigos con energía 0
            nuevos_enemigos = []
            for enemi in lista_enemigos:
                if enemi.energia > 0:
                    nuevos_enemigos.append(enemi)
                else:
                    score += 100
            lista_enemigos = nuevos_enemigos

            # Si no quedan enemigos, el jugador gana
            if len(lista_enemigos) == 0:
                # Detener la música de fondo y reproducir la de victoria
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Proyecto Final//Recursos//Music//win.mp3")
                pygame.mixer.music.play()
                # marcamos estado de victoria y salimos de este bloque
                victoria = True

            # Comprobar colisiones entre el jugador y los enemigos
            for enemi in lista_enemigos:
                if jugador.player.colliderect(enemi.player):
                    jugador.energia -= 1

            # Comprobar si el jugador ha muerto
            if jugador.energia <= 0:
                game_over = True

            # Mostrar el score en la pantalla
            font_score = pygame.font.SysFont(None, 36)
            texto_score = font_score.render(f"Puntaje: {score}", True, (255, 255, 255)) # Renderiza el texto del score en blanco

            score_x = ventana.get_width() - texto_score.get_width() - 10
            score_y = 10
            ventana.blit(texto_score, (score_x, score_y))
            # Dibujar el score en la esquina superior derecha

            vida_jugador()
            pygame.display.update()

        elif game_over:
            # sales del bucle principal
            return pantalla_final(ventana, "GAME OVER", "Proyecto Final//Recursos//Music//game_over.mp3")

        elif victoria:
            return pantalla_final(ventana, "¡YOU WIN!",  "Proyecto Final//Recursos//Music//win.mp3")

def pantalla_final(ventana, mensaje, ruta_musica):
    """Muestra Game Over o You Win, y dos botones: Reiniciar / Salir."""
    # Detén la música y carga el tema correspondiente
    pygame.mixer.music.stop()
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.play()

    # Prepara texto y botones
    fuente_tit = pygame.font.SysFont(None, 80)
    txt_tit = fuente_tit.render(mensaje, True, (255,255,255))
    w, h = ventana.get_size()
    tit_x = w//2 - txt_tit.get_width()//2
    tit_y = h//2 - txt_tit.get_height()//2 - 80

    btn_w, btn_h = 200, 50
    btn_re = pygame.Rect(w//2 - btn_w//2, tit_y + 100, btn_w, btn_h)
    btn_sal = pygame.Rect(w//2 - btn_w//2, tit_y + 180, btn_w, btn_h)

    fuente_btn = pygame.font.SysFont(None, 40)
    txt_re = fuente_btn.render("Reiniciar", True, (255,255,255))
    txt_sa = fuente_btn.render("Salir",      True, (255,255,255))

    # Bucle propio
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if btn_re.collidepoint(ev.pos):
                    return True   # quiere reiniciar
                if btn_sal.collidepoint(ev.pos):
                    pygame.quit(); sys.exit()

        #Dibujar todo cada frame
        ventana.fill((0,0,0))
        ventana.blit(txt_tit, (tit_x, tit_y))

        pygame.draw.rect(ventana, (0,150,0), btn_re)
        pygame.draw.rect(ventana, (150,0,0), btn_sal)

        ventana.blit(
            txt_re,
            (btn_re.centerx - txt_re.get_width()//2,
            btn_re.centery - txt_re.get_height()//2)
        )
        ventana.blit(
            txt_sa,
            (btn_sal.centerx - txt_sa.get_width()//2,
            btn_sal.centery - txt_sa.get_height()//2)
        )

        pygame.display.update()

if __name__ == '__main__':
    while True:
        reiniciar = main()
        if not reiniciar:
            break
    pygame.quit()



