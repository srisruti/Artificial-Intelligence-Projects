__author__ = 'sri'

'''
PEG SOLITAIRE- A* Heuristic: Number of Isolated nodes on the board
'''

import copy
import Queue as Q
import timeit

goalState=[['-', '-', '0', '0', '0', '-', '-'], ['-', '-', '0', '0', '0', '-', '-'], ['0','0', '0', '0','0', '0', '0'],
            ['0', '0', '0', 'X', '0', '0', '0'],['0', '0', '0', '0', '0', '0', '0'],['-', '-', '0', '0', '0', '-', '-'],
            ['-', '-', '0', '0', '0', '-', '-']]

fringeList=Q.PriorityQueue() # A priority queue which maintains the nodes that are unexplored

nodeCount=0 # Number of nodes expanded

'''
The class "Moves" represents each node that is explored.
The members are the node(current board), the depth in which the node is present in the tree and a cost associated with each node
Cost= h(n) + g(n) where h(n) is the heuristic and g(n) uniform cost
'''

class Moves:
    node=list()
    cost=0

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

    print "\nEnter the initial state:"
    listnumbers = list()

    for i in range(0, index):
        numbersinput = raw_input()
        inputlist=list(numbersinput)
        listnumbers.append(inputlist)

    return listnumbers

'''
The "getHeuristic" method gives the number of isolated pegs on the board
'''
def getHeuristic(intstate):

    count=0 #Number of isolated pegs

    for i in range(0,7):
        for j in range(0,7):
            if(intstate[i][j]=='X'):
                if(i>0 and i<6 and j>0 and j<6):
                    if(intstate[i-1][j]!='X' and intstate[i+1][j]!='X' and intstate[i][j-1]!='X' and intstate[i][j+1]!='X'):
                        count+=1;
                elif(i==0):
                    if(intstate[i+1][j]!='X' and intstate[i][j-1]!='X' and intstate[i][j+1]!='X'):
                        count+=1;
                elif(i==6):
                    if(intstate[i-1][j]!='X' and intstate[i][j-1]!='X' and intstate[i][j+1]!='X'):
                        count+=1;
                elif(j==0):
                    if(intstate[i-1][j]!='X' and intstate[i+1][j]!='X' and intstate[i][j+1]!='X'):
                        count+=1
                elif(j==6):
                    if(intstate[i-1][j]!='X' and intstate[i+1][j]!='X' and intstate[i][j-1]!='X'):
                        count+=1


    return count

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

    print "------A* Algorithm (Heuristic: Isolated Pegs)------ "
    starttime=timeit.default_timer() # The time when the program starts its execution

    initialstate=getinput(7)

    heu=getHeuristic(initialstate)
    moveObj= Moves(initialstate,0,heu)
    fringeList.put(moveObj) # start state is added to the fringeList

    ret=aStarSearch(initialstate)

    if(ret == '1'):
        print "The goal is reached"

    else:
        print "The goal is not reached"

    endtime=timeit.default_timer() # The time when the program ends its execution
    runtime=endtime-starttime

    print "Number of Nodes Explored:",nodeCount
    print "Running time:",runtime
