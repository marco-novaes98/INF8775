#!/usr/bin/pip
#!/usr/bin
import argparse
import numpy as np
import time as tt
from random import randrange

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
aretes = []
numberOfNodes = 0; 
voisins = []

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
        return sommetsSansCouleur[indices[v]] , listeCouleursVoisins[indices[v]]
        
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
    print("\nnb couleur glouton :",max(c)+1)
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

def getNbConflit(c):
    nbConflit = 0
    for a,b in aretes:
        if c[a] == c[b]:
            nbConflit += 1
    return nbConflit

def tabou(c):
    print("\nInit algo tabou \n")
    #constantes
    solutionSansConflit = c.copy()
    alpha = 2
    g = 10
    critereArret = 5000 #à déterminer
    n = len(graph[0]) 
    
    #variables d'interet
    nbIter = 0
    counterNoModif = 0
    
    listeTabou = [] #couple (noued,couleur,iterLimite)
    
    
    #---------REDUCTION DE COULEUR
    k = max(c) + 1 # nb couleurs utilisé dans c
    for currentNoued in range(n):
        if c[currentNoued] == k-1:
            nbConflit = [] # nbConflit[0] = nb voisin de couleur 0
            for j in range(k-1):                
                nbConflit.append(len([voisin for voisin in voisins[currentNoued] if c[voisin] == j]))
            minValue = min(nbConflit)
            c[currentNoued] = nbConflit.index(minValue)
    #---------
    cStar = c.copy()
    while counterNoModif < critereArret:
        
        #------ RECHERCHE TABOU
        #generation de voisin
        listeTabouReduite = [(el[0],el[1]) for el in listeTabou]
        nbConflitMin = n*n #initialisation a grande valeur
        for currentNoeud in range(n):
            for i in range(max(c) + 1):
                if i != c[currentNoeud] and (currentNoeud,i) not in listeTabouReduite: #check couleur legale
                    candidat = c.copy()
                    candidat[currentNoeud] = i
                    conflits = getNbConflit(candidat)
                    if conflits < nbConflitMin:
                        #print("conflit minimal: ",conflits)
                        nbConflitMin = conflits                    
                        bestCandidat = [candidat,currentNoeud,c[currentNoeud]] #coloration, noeud modif, ancienne couleur
                        if conflits == 0: #solution optimal
                            print("PAS DE CONFLITS")
                            print("candidat: ",candidat)
                            tabou(candidat)
                            return 
                            
                            
                        
        #actualisation solution courante
        if nbConflitMin != n*n: #que faire si aucun candidat à cause de listetabou?
            c = bestCandidat[0]
            #print(c)
        
    
                    
        #MaJ listeTabou
        l = alpha * nbConflitMin + randrange(0,g) + 1
        if nbConflitMin != n*n:
            listeTabou.append([bestCandidat[1],bestCandidat[2],l+nbIter])
        listeTabou = [a for a in listeTabou if a[2] > nbIter]
        #print("taille liste tabou", len(listeTabou))
        #actualisation solution optimale
        if getNbConflit(c) < getNbConflit(cStar):
            cStar = c.copy()
            counterNoModif = 0
        else:
            counterNoModif += 1
        #print("counterNoModif ",counterNoModif)
        #------
        
        nbIter += 1
        
    #print("solution tabou:         ",solutionSansConflit)
    print("nb couleur algo tabou: ",max(solutionSansConflit)+1,"\n")
    return(solutionSansConflit)

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
        readMatrix()
        t0 = tt.time()
        n = len(graph[0])
        for i in range(n):
                for j in range (n):
                    if i>j and graph[i][j] == 1:
                        aretes.append((i,j))
        for i in range(n):
            voisins.append([idx for idx in range(n) if graph[i][idx]==1])
        resultT = tabou(glouton(graph))
        t1 = tt.time()
        if showRes:
            print(resultT)
        if showTime:
       	    print(t1 - t0)
    else: 
	    print("this algorithm is not supported. please make sure to use 'glouton', 'branch_bound' or 'tabou'.")

main()