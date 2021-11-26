#!/usr/bin/pip
# !/usr/bin
import argparse
from collections import Counter

# storing args in global variables
cheminVersEx = "./instances/66_99.0"
MontrerRes = True

# global variables
nbEcoliers = 0
nbPairesNonCham = 0
taillesEcolier = []
pairEcolier = []


def lireExemplaire():
    f = open(cheminVersEx, "r")
    nbEcoliers = int(f.readline())
    nbPairesNonCham = int(f.readline())
    for x in range(nbEcoliers):
        taillesEcolier.append(int(f.readline()))
    for y in range(nbPairesNonCham):
        pairs = f.readline().split()
        if pairs.count != 0:
            pairs[0] = int(pairs[0]) - 1
            pairs[1] = int(pairs[1]) - 1
            pairEcolier.append(pairs)

    allowedNeighbors = [[] for i in range(nbEcoliers)]
    for a, b in pairEcolier:
        allowedNeighbors[a].append(b)
        allowedNeighbors[b].append(a)

    nb_voisin = [len(l) for l in allowedNeighbors]

    print("average number of neighbors = ", nbPairesNonCham * 2 / nbEcoliers)


    return nbEcoliers, nbPairesNonCham, allowedNeighbors

def get_wrong_assigments(taille_index):
    for a, b in zip(taille_index):
        if Counter([a, b]) == Counter([2, 1]):
            pass

def v1(nbEcoliers, nbPairesNonCham, allowedNeighbors):
    print("nbEcoliers: ", nbEcoliers)
    taille_index = [(index + 1, taille) for index, taille in enumerate(taillesEcolier)]
    taille_index.sort(key=lambda x: x[1])



def main():
    print("TP4")
    nbEcoliers, nbPairesNonCham, allowedNeighbors = lireExemplaire()
    v1(nbEcoliers, nbPairesNonCham, allowedNeighbors)


main()
