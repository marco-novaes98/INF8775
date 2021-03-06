#!/usr/bin/pip
# !/usr/bin
import argparse
import math
from collections import Counter
import time

# storing args in global variables
cheminVersEx = "./instances/66_970.0"
MontrerRes = True

# global variables
nbEcoliers = 0
nbPairesNonCham = 0
taillesEcolier = []
pairEcolier = []
allowedNeighbors = []
taille_index = []


def lireExemplaire():
    global allowedNeighbors
    global taille_index
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
    taille_index = [[taille, index + 1] for index, taille in enumerate(taillesEcolier)]

    print("average number of neighbors = ", nbPairesNonCham * 2 / nbEcoliers)

    return nbEcoliers

def exploreNode(c):
    newStates = []
    voisins = allowedNeighbors[c[2][-1]]
    visitedNodes = [n for n in c[2]]
    newVoisins = [voisin for voisin in voisins if voisin not in visitedNodes]  # list of indexes
    for nv in newVoisins:
        height = taillesEcolier[nv]
        if height > c[1]:
            newStates.append([c[0], height, c[2] + [nv]])
        elif height <= c[1]:
            newStates.append([c[0] + 1, c[1], c[2] + [nv]])
        else:  # equal height
            #TODO
            pass
    return newStates

def branchBound(nbEcoliers):
    global taille_index
    listSort = sorted(taille_index, key=lambda x: x[0])
    ub = math.inf
    best_solution = None
    best_score = math.inf

    for i in range(nbEcoliers):
        t0 = time.time()
        print("iteration nº: ", i)
        v = listSort[i]  # iteratif lower student
        stack = []
        c = [0, v[0], [v[1]]] #[nbConflits, max height, [index, index, ...]]
        stack.append(c)
        while len(stack):
            c = stack.pop()
            if len(c[2]) == nbEcoliers: #final state
                if c[0] < best_score:
                    print("SOLUTION FOUND!", c)
                    print("Time since iteration start: ", time.time() - t0)
                    best_solution = c.copy()
                    ub = c[0]
            elif c[0] < ub:
                for i in exploreNode(c):
                    stack.append(i)
        print("Time interation: ", time.time() - t0)
    return best_solution



def main():
    nbEcoliers = lireExemplaire()
    t0 = time.time()
    best_solution = branchBound(nbEcoliers)
    print("Total time: ", time.time() - t0)

main()

"""
    Idée d'amélioration
    
- heuristique pour explorer en priorité les noueds les plus prometteurs (attention a maintenir la recherche en profondeur)
- check si noeud isolé, dans ce cas on rejette cette solution
- utiliser BnB pour atteindre une solution intermédiaire (ex: solution correcte de longueur totalLength/2) et 
  implementer une auutre methode à partir de ce point (switchs ...)
"""
