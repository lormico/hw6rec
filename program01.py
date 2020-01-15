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

import immagini
def es1(filepng, filetxt):
    # inserite qui il vostro codice
    pass


if __name__ == '__main__':
    # inserite qui i vostri test
    pass
