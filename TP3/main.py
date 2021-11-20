#!/usr/bin/pip
# !/usr/bin
import argparse
from random import randrange

# parsing args
parser = argparse.ArgumentParser(description='parse main args')
parser.add_argument('-e', type=str, required=True, help='path to ex')
parser.add_argument('-p', action='store_true', dest='res', help='show res')
parser.set_defaults(res=False)
args = parser.parse_args()

# storing args in global variables
pathToEx = args.e
showRes = args.res

def main():
    print("TP4")


main()
