from constantes import *

class Mundo:
    def __init__(self): # Inicializa el mundo del juego
        self.map = [] # Lista que contendrá los datos del mapa

    def cargar_mundo(self, data, mapa_list): # Carga el mundo desde los datos y la lista de imágenes del mapa
        self.nivel = len(data) # Número de filas en el mapa
        for y, fila in enumerate(data): # Recorre cada fila del mapa
            for x, tile in enumerate(fila): # Recorre cada columna de la fila
                if tile < 0 or tile >= len(mapa_list):# Asegúrese de que el tile esté dentro del rango de la lista de imágenes
                    # Si el tile está fuera de rango, se asigna un valor por defecto (0) y se imprime un mensaje de error
                    print(f"Error: Tile fuera de rango en ({y},{x}): {tile}.")
                    tile = 0
                imagen = mapa_list[tile] # Obtiene la imagen correspondiente al tile
                imagen_rect = imagen.get_rect() # Obtiene el rectángulo de la imagen para posicionarla
                imagen_x = x * TAMANO_CUADRICULA # Calcula la posición x de la imagen
                imagen_y = y * TAMANO_CUADRICULA # Calcula la posición y de la imagen
                imagen_rect.topleft = (imagen_x, imagen_y) # Establece la posición de la imagen en el rectángulo
                mapa_data = [imagen, imagen_rect, imagen_x, imagen_y] # Crea una lista con la imagen, el rectángulo y las coordenadas
                self.map.append(mapa_data) # Añade la lista al mapa

    def actualizar_mundo(self, posicion_pantalla):
        for tile in self.map:
            tile[1].x += posicion_pantalla[0]
            tile[1].y += posicion_pantalla[1]
            tile[1].topleft = (tile[2] + posicion_pantalla[0], tile[3] + posicion_pantalla[1])

    def dibujar_mundo(self, ventana, desplazamineto_x = 0, desplazamiento_y = 0): # Dibuja el mundo en la ventana
        for tile in self.map: # Recorre cada tile en el mapa
            imagen, imagen_rect, imagen_x, imagen_y = tile
            ventana.blit(imagen, (imagen_x - desplazamineto_x, imagen_y - desplazamiento_y)) # Dibuja la imagen en la ventana en la posición calculada