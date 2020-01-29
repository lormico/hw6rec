#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In una immagine tutta nera sono disegnati un certo numero di rettangoli di colori
distinti. I rettangoli sono stati disegnati in ordine, in modo che il primo sia
stato parzialmente coperto dal secondo, il secondo dal terzo e così via fino
all'ultimo rettangolo che è l'unico a non essere coperto da un altro rettangolo.

Lo scopo dell'esercizio è ricostruire la sequenza esatta dei rettangoli, salvando
in un file le coordinate colonna riga dei due vertici alto a sinistra e basso a destra 
e il colore di ogni rettangolo come tupla.

Progettare una funzione es1(fname1, fname2) che prenda come argomento il file
con una immagine fname1 sopra descritta e produca in fname2 l'output sopra
descritto. La funzione ritorna il numero di rettangoli distinti riconosciuti
nell'immagine.

Es: la funzione deve restituire 5 quando riceve 'rettangoli_5.png' come fname1 e
    deve produrre in fname2 il seguente output:

    3 16 161 57 (43, 39, 102)
    72 49 269 187 (162, 201, 115)
    180 50 276 109 (82, 19, 174)
    210 92 279 175 (231, 39, 88)
    230 166 280 208 (6, 161, 199)

Per caricare e salvare  file PNG si devono usare load e save della
libreria immagini allegata.

NOTA: il timeout per ciascun test è fissato a 1 secondo.

ATTENZIONE: quando caricate il file assicuratevi che sia nella codifica UTF8
(ad esempio editatelo dentro Spyder)
"""

from typing import Dict, Tuple, List, Set

import immagini


class Rectangle:
    def __init__(self, initial_x, initial_y, color):
        self.x_max = initial_x
        self.x_min = initial_x
        self.y_max = initial_y
        self.y_min = initial_y
        self.color = color

    def add_pixel(self, x, y):
        self.x_max = max(x, self.x_max)
        self.x_min = min(x, self.x_min)
        self.y_max = max(y, self.y_max)
        self.y_min = min(y, self.y_min)

    def __str__(self):
        return "%(x_min)d %(y_min)d %(x_max)d %(y_max)d %(color)s" % self.__dict__


def find_rectangles_1(picture) -> List[Rectangle]:
    last_color = (0, 0, 0)
    rectangle_dict: Dict[Tuple[int, int, int], Rectangle] = dict()

    for y, row in enumerate(picture):
        for x, current_color in enumerate(row):
            if last_color != current_color:
                if current_color not in rectangle_dict.keys():
                    rectangle_dict[current_color] = Rectangle(
                        x, y, current_color)
                else:
                    rectangle_dict[current_color].add_pixel(x, y)

    return list(rectangle_dict.values())


def find_rectangles_2(picture) -> Dict[Tuple[int, int, int], List[int]]:
    last_color = (0, 0, 0)
    rectangle_dict: Dict[Tuple[int, int, int], List[int]] = dict()

    for y, row in enumerate(picture):
        for x, current_color in enumerate(row):
            if last_color != current_color:
                if current_color not in rectangle_dict:
                    rectangle_dict[current_color] = [x, y, x, y] # xmin ymin xmax ymax
                else:
                    curr_rect = rectangle_dict[current_color]
                    curr_rect[0] = min(x, curr_rect[0])
                    curr_rect[1] = min(y, curr_rect[1])
                    curr_rect[2] = max(x, curr_rect[2])
                    curr_rect[3] = max(y, curr_rect[3])

    return rectangle_dict


def find_rectangles_3(picture: List[List[Tuple[int, int, int]]]) -> Dict[Tuple[int, int, int], List[int]]:
    rectangle_dict: Dict[Tuple[int, int, int], List[int]] = dict()

    color_dict: Dict[Tuple[int, int, int], Dict[str, Set[int]]] = dict()
    for y, row in enumerate(picture):
        for x, current_color in enumerate(row):
            color_dict.setdefault(current_color, dict()).setdefault('x', set()).add(x)
            color_dict.setdefault(current_color, dict()).setdefault('y', set()).add(y)

    for color, pixeldict in color_dict.items():
        rectangle_dict[color] = [min(pixeldict['x']), min(pixeldict['y']), max(pixeldict['x']), max(pixeldict['y'])]

    return rectangle_dict


def es1(filepng, filetxt) -> int:
    pic = immagini.load(filepng)
    
    ## modo 1 ##
    rectangles = find_rectangles_1(pic)

    with open(filetxt, 'w') as fh:
        for rectangle in rectangles:
            fh.write(str(rectangle) + "\n")

    return len(rectangles)
    ############

    ## modo 2 ##
    rectangles = find_rectangles_2(pic)

    with open(filetxt, 'w') as fh:
        for color, rectangle in rectangles.items():
            fh.write(f"{rectangle[0]} {rectangle[1]} {rectangle[2]} {rectangle[3]} {color}\n")

    return len(rectangles)

if __name__ == '__main__':
    import cProfile
    # data = (  
    #         ("appoggiata",            5),
    #         ("rettangoli_5",          5),
    #         ("rettangoli_10",        10),
    #         ("rettangoli_20",        20),
    #         ("rettangoli_grande_5",  10),
    #         ("rettangoli_grande_10", 20),
    #         ("rettangoli_grande_20", 40),
    #         ("casuale_5",             5),
    #         ("casuale_25",           25),
    #         ("casuale_45",           45),
    #        )
    # for datum in data:
    #     cProfile.run('es1(f"{datum[0]}.png", f"test_{datum[0]}.txt")')

    cProfile.run('es1("casuale_45.png", f"test_casuale_45.txt")')
