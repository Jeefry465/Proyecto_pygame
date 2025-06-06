from constantes import *

class Mundo:
    def __init__(self):
        self.map = []

    def cargar_mundo(self, data, mapa_list):
        self.nivel = len(data)
        for y, fila in enumerate(data):
            for x, tile in enumerate(fila):
                imagen = mapa_list[tile]
                imagen_rect = imagen.get_rect()
                imagen_x = x * TAMANO_CUADRICULA
                imagen_y = y * TAMANO_CUADRICULA
                imagen_rect.topleft = (imagen_x, imagen_y)
                mapa_data = [imagen, imagen_rect, imagen_x, imagen_y]
                self.map.append(mapa_data)

    def dibujar_mundo(self, ventana):
        for tile in self.map:
            ventana.blit(tile[0], tile[1])