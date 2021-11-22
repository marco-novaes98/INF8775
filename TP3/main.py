#!/usr/bin/pip
# !/usr/bin
import argparse

# parsing args
parser = argparse.ArgumentParser(description='parse main args')
parser.add_argument('-e', type=str, required=True, help='path to ex')
parser.add_argument('-p', action='store_true', dest='res', help='show res')
parser.set_defaults(res=False)
args = parser.parse_args()

# storing args in global variables
cheminVersEx = args.e
MontrerRes = args.res

# global variables
nbEcoliers = 0
nbPairesNonCham = 0
taillesEcolier = []
pairEcolier = []

def lireExemplaire():
    f = open(cheminVersEx, "r")
    nbEcoliers = int(f.readline())
    nbPairesNonCham =  int(f.readline())
    for x in range(nbEcoliers):
        taillesEcolier.append(int(f.readline()))
    for y in range(nbPairesNonCham):
        pairs = f.readline().split()
        if pairs.count!=0:
            pairs[0] = int(pairs[0])
            pairs[1] = int(pairs[1])
            pairEcolier.append(pairs)

def main():
    print("TP4")
    lireExemplaire()

main()
