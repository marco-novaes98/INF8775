#!/usr/bin/pip
#!/usr/bin
import argparse
import os
import sys
import numpy as np

#parsing args
parser = argparse.ArgumentParser(description='parse main args')
parser.add_argument('-a', type=str, required=True, help='algotype used')
parser.add_argument('-e', type=str, required=True, help='path to ex')
parser.add_argument('-p', action='store_true', dest='res', help='show res')
parser.set_defaults(res=False)
parser.add_argument('-t', action='store_true', dest='time', help='show time')
parser.set_defaults(res=False)
args = parser.parse_args()

#storing args in global variables
algoType = args.a
pathToEx = args.e
showRes = args.res
showTime = args.time

#global variables 
time = 0
graph = []
numberOfNodes = 0; 

def printRes(): 
    print(graph)

def readMatrix(): 
    with open(pathToEx) as f:
    	numberOfNodes = int(f.readline())
    	for i in range(0, numberOfNodes):
    	    graph.append(list(map(int, f.readline().split(' ')[:numberOfNodes])))

def branchBound():
    print("here")

def main():
    if algoType == "glouton": 
    	print("glouton")
    elif algoType=="branch_bound":
    	readMatrix()
    	branchBound()
    	if showRes:
    	    printRes()
    	if showTime:
    	    print("showTime")
    elif algoType == "tabou":
	    print("tabou")
    else: 
	    print("this algorithm is not supported. please make sure to use 'glouton', 'branch_bound' or 'tabou'.")

main()