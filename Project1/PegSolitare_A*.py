__author__ = 'sri'

'''
PEG SOLITAIRE- A* Heuristic: Average between all the pegs on the board
'''

import copy
import Queue as Q
import math
import timeit

goalState=[['-', '-', '0', '0', '0', '-', '-'], ['-', '-', '0', '0', '0', '-', '-'], ['0','0', '0', '0','0', '0', '0'],
            ['0', '0', '0', 'X', '0', '0', '0'],['0', '0', '0', '0', '0', '0', '0'],['-', '-', '0', '0', '0', '-', '-'],
            ['-', '-', '0', '0', '0', '-', '-']]

fringeList=Q.PriorityQueue() # A priority queue which maintains the nodes that are unexplored

nodeCount=0 # Number of nodes expanded

pointList=list() # Maintains the peg coordinates to compute the average distance

'''
The class "Moves" represents each node that is explored.
The members are the node(current board), the depth in which the node is present in the tree and a cost associated with each node
Cost= h(n) + g(n) where h(n) is the heuristic and g(n) uniform cost
'''
class Moves:

    node=list()
    cost=0
    depth=0


    def __init__(self,node,depth,cost):
        self.node=node
        self.depth=depth
        self.cost=cost

    def __cmp__(self,other):
            return cmp(self.cost,other.cost)

'''
The "getinput" method gets the initial state of the board as input
'''
def getinput(index):

    print "Enter the initial state:\n"
    listnumbers = list()

    for i in range(0, index):
        numbersinput = raw_input()
        inputlist=list(numbersinput)
        listnumbers.append(inputlist)

    return listnumbers

'''
The "distance" method calculates the distance between two given points
'''
def distance(instate,i,j,k,l):

    diff= (math.pow((i-k),2))+(math.pow((j-l),2))
    dis=math.sqrt(diff)

    return dis

'''
The "findDistance" method calculates the sum of distances between a given peg and all other pegs on the board
'''
def findDistance(instate,i,j):

    d=0

    for k in range(i,7):
        for l in range(0,7):
            if(instate[k][l]=='X') and ((k,l) not in pointList):
                d+=distance(instate,i,j,k,l)
    return d

'''
The "getHeuristic" method gives the average distance between all the pegs in the current state of board
'''
def getHeuristic(intstate):

    del pointList[:]
    dist=0
    count=0 # number of pegs on the board

    for i in range(0,7):
        for j in range(0,7):
            if(intstate[i][j]=='X'):
                point=(i,j)
                pointList.append(point)
                dist+=findDistance(intstate,i,j)
                count=count+1

    return (dist/count)

'''
The "findPossibleMoves" method generates the children of the each node i.e. all the possible moves from the given state
The new children are inserted into the priority queue(fringe list)
'''
def findPossibleMoves(interstate):
    global nodesCount
    for i in range(0, 7):
        for j in range(0, 7):
            if(interstate.node[i][j]== 'X'):
                if(j<5):
                    if(interstate.node[i][j+1]== 'X' and interstate.node[i][j+2]== '0'):
                        posstate=copy.deepcopy(interstate.node)
                        posstate[i][j]='0'
                        posstate[i][j+1]='0'
                        posstate[i][j+2]='X'
                        gn=interstate.depth+1
                        heu=getHeuristic(posstate)
                        fn=gn+heu
                        moveObj= Moves(posstate,interstate.depth+1,fn)
                        fringeList.put(moveObj)

                if(i<5):
                    if(interstate.node[i+1][j]=='X' and interstate.node[i+2][j]=='0'):
                        posstate=copy.deepcopy(interstate.node)
                        posstate[i][j]='0'
                        posstate[i+1][j]='0'
                        posstate[i+2][j]='X'
                        gn=interstate.depth+1
                        heu=getHeuristic(posstate)
                        fn=gn+heu
                        moveObj= Moves(posstate,interstate.depth+1,fn)
                        fringeList.put(moveObj)



                if(i>1):
                    if(interstate.node[i-1][j] == 'X' and interstate.node[i-2][j] == '0'):
                        posstate=copy.deepcopy(interstate.node)
                        posstate[i][j]='0'
                        posstate[i-1][j]='0'
                        posstate[i-2][j]='X'
                        gn=interstate.depth+1
                        heu=getHeuristic(posstate)
                        fn=gn+heu
                        moveObj= Moves(posstate,interstate.depth+1,fn)
                        fringeList.put(moveObj)

                if(j>1):
                    if(interstate.node[i][j-1] == 'X' and interstate.node[i][j-2] == '0'):
                        posstate=copy.deepcopy(interstate.node)
                        posstate[i][j]='0'
                        posstate[i][j-1]='0'
                        posstate[i][j-2]='X'
                        gn=interstate.depth+1
                        heu=getHeuristic(posstate)
                        fn=gn+heu
                        moveObj= Moves(posstate,interstate.depth+1,fn)
                        fringeList.put(moveObj)

'''
The "aStarSearch" method is used to search for the goal state.
A node is removed from the beginning of the priority queue and checked if it is the goal state. If yes, the function returns
Otherwise, children are determined using "findPossibleMoves" and are added to the priority queue.
'''
def aStarSearch(inistate):

    global nodeCount

    while not fringeList.empty():

        fringeNode=fringeList.get()

        if(fringeNode.node == goalState):
            return '1'

        findPossibleMoves(fringeNode)
        nodeCount=nodeCount+1


if __name__ == '__main__':

    print "------A* Algorithm (Heuristic: Average distance)------ "
    starttime=timeit.default_timer() # The time when the program starts its execution
    initialstate=getinput(7)

    heu=getHeuristic(initialstate)
    moveObj= Moves(initialstate,0,heu)
    fringeList.put(moveObj) # start state is added to the fringeList

    ret=aStarSearch(initialstate)

    if(ret == '1'):
        print "The goal is reached."

    else:
        print "The goal is not reached"

    endtime=timeit.default_timer() # The time when the program ends its execution
    runtime=endtime-starttime

    print "Number of Nodes Explored:",nodeCount
    print "Running time:",runtime
