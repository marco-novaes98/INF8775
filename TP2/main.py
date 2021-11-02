#!/usr/bin/pip
#!/usr/bin
import argparse
import numpy as np
import time as tt

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

def readMatrix(): 
    with open(pathToEx) as f:
    	numberOfNodes = int(f.readline())
    	for i in range(0, numberOfNodes):
    	    graph.append(list(map(int, f.readline().split(' ')[:numberOfNodes])))

    
#----------
  

def choixGlouton(c,nbDegre,voisins,n):
    sommetsSansCouleur = [i for i in range(n) if c[i] == None]
    listeCouleursVoisins=[]
    for i in sommetsSansCouleur:
        listeCouleursVoisins.append([c[i] for i in voisins[i]])
    listeCouleursVoisins = [set(i) for i in listeCouleursVoisins]
    for i in listeCouleursVoisins:
        if None in i: i.remove(None)
    nbCouleursVoisins = [len(a) for a in listeCouleursVoisins]
    max_value = max(nbCouleursVoisins) 
    indices = [index for index, element in enumerate(nbCouleursVoisins) if element == max_value]
    if len(indices) == 1:
        return sommetsSansCouleur[indices[0]] , listeCouleursVoisins[indices[0]]
    else:
        nbDegreDsatMax = [nbDegre[sommetsSansCouleur[i]] for i in indices]
        max_value = max(nbDegreDsatMax)
        v = nbDegreDsatMax.index(max_value)
        return sommetsSansCouleur[indices[v]] , listeCouleursVoisins[v]
        
def minValue(couleursVoisins):
    chosingColor = True
    color = 0
    while chosingColor:
        if color in couleursVoisins:
            color += 1
        else:
            chosingColor = False
    return color

    

def glouton(m):
    #initialisation
    n = len(m[0]) 
    c = [None]*n
    voisins = []
    for i in range(n):
        voisins.append([idx for idx in range(n) if m[i][idx]==1])
    nbDegre = [len(i) for i in voisins] 
    max_value = max(nbDegre)
    v = nbDegre.index(max_value)
    c[v] = 0
    
    while any(x == None for x in c):
        v , couleursVoisins = choixGlouton(c,nbDegre,voisins,n)
        c[v] = minValue(couleursVoisins)
    return c
    
    

#----------


def possibleColor(couleursVoisins, color) : 
    if color in couleursVoisins:
        return False
    return True

def exploreNode(c,nbDegre,voisins,n) : 
    listNodes = []
    c = [None if x==-1 else x for x in c]
    v , couleursVoisins = choixGlouton(c,nbDegre,voisins,n)
    c = [-1 if x==None else x for x in c]
    for i in range(max(c)+2) :        
        if possibleColor(couleursVoisins, i) :
            newC = c
            newC[v] = i
            listNodes.append(newC)
    return listNodes


def branchBound():
    res = glouton(graph)
    ub = max(res)+1
    stack = []
    n = len(graph[0]) 
    c = [-1]*n #le couleur des noeau from 0 to n
    voisins = []
    for i in range(n):
        voisins.append([idx for idx in range(n) if graph[i][idx]==1])
    nbDegre = [len(i) for i in voisins] 
    max_value = max(nbDegre)
    v = nbDegre.index(max_value) #sommet qui a plus de donnees
    c[v] = 0 # premier couleur
    
    stack.append(c)
    while len(stack):
        c = stack.pop()
        if not(any(x == -1 for x in c)):
            if (max(c)+1) < max(res)+1 :
                res = c
                ub = max(c)+1
        else :
            if max(c) + 1 < ub:  
                for i in exploreNode(c,nbDegre,voisins,n) :
                    stack.append(i)
    return res

def main():
    if algoType == "glouton": 
        readMatrix()
        t0 = tt.time()
        resultG = glouton(graph)
        t1 = tt.time()
        if showRes:
            print(resultG)
        if showTime:
       	    print(t1 - t0)
    elif algoType=="branch_bound":
    	readMatrix()
    	t2 = tt.time()
    	resultBB = branchBound()
    	t3 = tt.time()
    	if showRes:
    	    print(resultBB)
    	if showTime:
    	    print(t3 - t2)
    elif algoType == "tabou":
	    print("tabou")
    else: 
	    print("this algorithm is not supported. please make sure to use 'glouton', 'branch_bound' or 'tabou'.")

main()