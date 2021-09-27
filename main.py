import pygame
import numpy as np
import random
from copy import deepcopy
import math

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('tetris.mp3')
pygame.mixer.music.play(loops=-1)

width, height = 300, 380
ventana_juego = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")
white = (255, 255, 255)
red = (255, 0, 0)
tam_bloque = 15
posiciones = []
posiciones_tablero = []
coods_eliminar = []
reloj = pygame.time.Clock()
figura_actual = []
siguiente_figura = []
posiciones_siguiente_figura = []
puntaje = pygame.font.Font(None, 30)
puntos = 0
texto = puntaje.render("Puntaje: {}            Siguiente:".format(puntos), True, (255, 255, 255))

L = np.array((
    (1, 0, 0),
    (2, 1, 1),
))

L_invertida = np.array((
    (0, 0, 1),
    (1, 1, 2),
))

I = np.array((
    (1, 2, 1, 1),
))

O = np.array((
    (1, 1),
    (2, 1),
))

Z = np.array((
    (1, 2, 0),
    (0, 1, 1),
))

Z_inv = np.array((
    (0, 1, 1),
    (1, 2, 0),
))

T = np.array((
    (0, 1, 0),
    (1, 2, 1),
))

figuras = [L, L_invertida, I, O, Z, Z_inv, T]


def obtenerCuadricula():
    global coordenadas
    coordenadas = []
    for j in range(30, 346, 15):
        for i in range(10, 146, 15):
            coordenadas.append([i, j])


def Cuadricula(ventana_juego, tablero_actual):
    global pos
    pos = []
    for i in range(45, 361, 15):
        pygame.draw.line(ventana_juego, white, (10, i), (160, i))

    for i in range(10, 161, 15):
        pygame.draw.line(ventana_juego, white, (i, 30), (i, 360))

    pygame.draw.line(ventana_juego, red, (10, 30), (160, 30))
    pygame.draw.line(ventana_juego, red, (10, 30), (10, 360))
    pygame.draw.line(ventana_juego, red, (10, 360), (160, 360))
    pygame.draw.line(ventana_juego, red, (160, 360), (160, 30))

    pygame.draw.line(ventana_juego, red, (180, 30), (280, 30))
    pygame.draw.line(ventana_juego, red, (180, 30), (180, 130))
    pygame.draw.line(ventana_juego, red, (180, 130), (280, 130))
    pygame.draw.line(ventana_juego, red, (280, 130), (280, 30))

    if tablero_actual:
        for i in tablero_actual:
            x, y = i
            pygame.draw.rect(ventana_juego, white,
                             [x, y, tam_bloque, tam_bloque])


def ObtenerPosciones(figura):
    global posiciones, shape, asignar_pos, origen, ox, oy
    origen = []
    shape = figura
    asignar_pos = []
    for a, b in enumerate(figura):
        for c, d in enumerate(b):
            if d or d == 2:
                posiciones.append([70 + tam_bloque * c, 30 + a * tam_bloque])

            if d == 2:
                ox = 70 + tam_bloque * c
                oy = 30 + a * tam_bloque


def SeleccionarFigura():
    global figura_actual
    figura_actual = figuras[random.randint(0, 6)]


def DibujarFigura(figuras):
    global siguiente_figura
    for i in figuras:
        x, y = i
        pygame.draw.rect(ventana_juego, white,
                         [x, y, tam_bloque, tam_bloque])
    Cuadricula(ventana_juego, posiciones_tablero)
    ventana_juego.blit(texto, (10, 7))
    pygame.display.update()


def ComprobarPosicion(pos_pieza, coord):
    global coordenadas, posiciones_tablero, posiciones_siguiente_figura

    if coord == 'y':
        for i in range(len(pos_pieza)):
            pos_pieza[i][1] = pos_pieza[i][1] + 15

        for i in pos_pieza:
            if not i in coordenadas:
                for j in range(len(posiciones)):
                    posiciones_tablero.append(posiciones[j])

                for j in range(len(posiciones)):
                    coordenadas.remove(posiciones[j])

                for remover in posiciones_siguiente_figura:
                    posiciones_tablero.remove(remover)

                posiciones.clear()
                figura_actual = siguiente_figura
                posiciones_siguiente_figura.clear()
                SiguienteFigura()
                ObtenerPosciones(figura_actual)
                DibujarFigura(posiciones)
                return False

    if coord == 'xr':
        for i in range(len(pos_pieza)):
            pos_pieza[i][0] = pos_pieza[i][0] + 15

            if not pos_pieza[i] in coordenadas:
                return False

    if coord == 'xl':
        for i in range(len(pos_pieza)):
            pos_pieza[i][0] = pos_pieza[i][0] - 15

            if not pos_pieza[i] in coordenadas:
                return False

    return True


def EliminarFila():
    global coordenadas, posiciones_tablero, coods_eliminar, puntos, texto

    x = [i for i in range(10, 146, 15)]
    y = [i for i in range(30, 346, 15)]

    for i in range(len(y)):
        for k in range(len(x)):
            if [x[k], y[i]] in posiciones_tablero:
                coods_eliminar.append([x[k], y[i]])
        if len(coods_eliminar) == 10:
            pos_mover_y = y[i]
            puntos = puntos + 10
            texto = puntaje.render("Puntaje: {}            Siguiente:".format(puntos), True, (255, 255, 255))
            for k in range(len(coods_eliminar)):
                posiciones_tablero.remove(coods_eliminar[k])
                coordenadas.append(coods_eliminar[k])

            prueba = deepcopy(posiciones_tablero)
            for mover in range(len(prueba)):
                if prueba[mover][1] < pos_mover_y:
                    if not prueba[mover] in coordenadas:
                        coordenadas.append(prueba[mover])

            for mover in range(len(posiciones_tablero)):
                if posiciones_tablero[mover][1] < pos_mover_y:
                    posiciones_tablero[mover][1] = posiciones_tablero[mover][1] + 15
                    if posiciones_tablero[mover] in coordenadas:
                        coordenadas.remove(posiciones_tablero[mover])

            coods_eliminar.clear()
        else:
            coods_eliminar.clear()


def Reloj():
    global posiciones, reloj, oy
    ventana_juego.fill((0, 0, 0))
    if ComprobarPosicion(deepcopy(posiciones), 'y'):
        for i in range(len(posiciones)):
            posiciones[i][1] = posiciones[i][1] + 15
    oy = oy + 15
    reloj.tick(4)


def Rotar(puntos):
    global ox, oy, coordenadas
    temporal = []
    angulo = math.pi / 2
    contador = 0
    for i in puntos:
        x, y = i
        if [ox, oy] != i:
            qx = ox + math.cos(angulo) * (x - ox) + math.sin(angulo) * (y - oy)
            qy = oy + -math.sin(angulo) * (x - ox) + math.cos(angulo) * (y - oy)

            temporal.append([int(qx), int(qy)])
        else:
            temporal.append([int(x), y])

    for i in temporal:
        if i in coordenadas:
            contador = contador + 1

    if contador == len(temporal):
        posiciones.clear()

        for i in temporal:
            posiciones.append(i)


def SiguienteFigura():
    global siguiente_figura, posiciones_siguiente_figura, posiciones_tablero
    siguiente_figura = figuras[random.randint(0, 6)]

    for a, b in enumerate(siguiente_figura):
        for c, d in enumerate(b):
            if d or d == 2:
                posiciones_siguiente_figura.append([205 + tam_bloque * c, 65 + a * tam_bloque])

    posiciones_tablero = posiciones_tablero + posiciones_siguiente_figura


SeleccionarFigura()
SiguienteFigura()
ObtenerPosciones(figura_actual)
DibujarFigura(posiciones)
obtenerCuadricula()
EliminarFila()


def main():
    global estado, posiciones, asd, array, asignar_pos, pos, posiciones_tablero, coordenadas, figura_actual, ox, oy
    run = True
    while (run):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                ventana_juego.fill((0, 0, 0))
                if event.key == pygame.K_LEFT:
                    if ComprobarPosicion(deepcopy(posiciones), 'xl'):
                        for i in range(len(posiciones)):
                            posiciones[i][0] = posiciones[i][0] - 15
                        ox = ox - 15

                if event.key == pygame.K_RIGHT:
                    if ComprobarPosicion(deepcopy(posiciones), 'xr'):
                        for i in range(len(posiciones)):
                            posiciones[i][0] = posiciones[i][0] + 15
                        ox = ox + 15

                if event.key == pygame.K_DOWN:
                    if ComprobarPosicion(deepcopy(posiciones), 'y'):
                        for i in range(len(posiciones)):
                            posiciones[i][1] = posiciones[i][1] + 15
                        oy = oy + 15

                if event.key == pygame.K_UP:
                    Rotar(posiciones)

        DibujarFigura(posiciones)
        EliminarFila()
        Reloj()
        Cuadricula(ventana_juego, posiciones_tablero)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
