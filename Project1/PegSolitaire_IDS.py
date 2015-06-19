__author__ = 'sri'

'''
PEG SOLITAIRE- ITERATIVE DEEPENING SEARCH
'''

import copy
import timeit

goalState=[['-', '-', '0', '0', '0', '-', '-'], ['-', '-', '0', '0', '0', '-', '-'], ['0','0', '0', '0','0', '0', '0'],
            ['0', '0', '0', 'X', '0', '0', '0'],['0', '0', '0', '0', '0', '0', '0'],['-', '-', '0', '0', '0', '-', '-'],
            ['-', '-', '0', '0', '0', '-', '-']]

moveboard = [['0', '0', '1', '2', '3', '0', '0'], ['0', '0', '4', '5', '6', '0', '0'], ['7', '8', '9', '10', '11', '12', '13'],
             ['14', '15', '16', '17', '18', '19','20'],['21', '22', '23', '24', '25', '26','27'], ['0', '0', '28', '29', '30', '0', '0'],
              ['0', '0', '31', '32', '33', '0', '0']]

fringeList=[] # A stack which maintains the nodes that are unexplored

nodesCount=0 # Number of nodes expanded

'''
The class Moves represents each node that is explored.
The members are the node(current board) and the depth in which the node is present in the tree
'''
class Moves:

    nodeMove=list()
    depth=0
    nextMoves= "  "
    parent=list()

    def __init__(self,nodeMove,depth,parent,nextMove):
        self.nodeMove=nodeMove
        self.depth=depth
        self.parent=parent
        if parent!=None:
            self.nextMoves= self.parent.nextMoves +" , "+ nextMove
        else:
            self.nextMoves=" "

'''
The getinput method gets the initial state of the board as input
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
The findPossibleMoves method generates the children of the each node i.e. all the possible moves from the given state
The new children are pushed into the stack(fringe list)
'''
def findPossibleMoves(interstate):
    global nodesCount
    for i in range(0, 7):
        for j in range(0, 7):
            if(interstate.nodeMove[i][j]== 'X'):
                if(j<5):
                    if(interstate.nodeMove[i][j+1]== 'X' and interstate.nodeMove[i][j+2]== '0'):
                        posstate=copy.deepcopy(interstate.nodeMove)
                        posstate[i][j]='0'
                        posstate[i][j+1]='0'
                        posstate[i][j+2]='X'
                        string=str(moveboard[i][j])+" to " +str(moveboard[i][j+2])
                        moveObj= Moves(posstate,interstate.depth+1,interstate,string)
                        fringeList.append(moveObj)

                if(i<5):
                    if(interstate.nodeMove[i+1][j]=='X' and interstate.nodeMove[i+2][j]=='0'):
                        posstate=copy.deepcopy(interstate.nodeMove)
                        posstate[i][j]='0'
                        posstate[i+1][j]='0'
                        posstate[i+2][j]='X'
                        string=str(moveboard[i][j])+" to " +str(moveboard[i+2][j])
                        moveObj= Moves(posstate,interstate.depth+1,interstate,string)
                        fringeList.append(moveObj)

                if(i>1):
                    if(interstate.nodeMove[i-1][j] == 'X' and interstate.nodeMove[i-2][j] == '0'):
                        posstate=copy.deepcopy(interstate.nodeMove)
                        posstate[i][j]='0'
                        posstate[i-1][j]='0'
                        posstate[i-2][j]='X'
                        string=str(moveboard[i][j])+" to " +str(moveboard[i-2][j])
                        moveObj= Moves(posstate,interstate.depth+1,interstate,string)
                        fringeList.append(moveObj)

                if(j>1):
                    if(interstate.nodeMove[i][j-1] == 'X' and interstate.nodeMove[i][j-2] == '0'):
                        posstate=copy.deepcopy(interstate.nodeMove)
                        posstate[i][j]='0'
                        posstate[i][j-1]='0'
                        posstate[i][j-2]='X'
                        string=str(moveboard[i][j])+" to " +str(moveboard[i][j-2])
                        moveObj= Moves(posstate,interstate.depth+1,interstate,string)
                        fringeList.append(moveObj)


'''
The method "dfs" performs a Depth First Search traversal up to a given limit of depth
It pops a node from the fringe list and checks if it a goal state. If yes, 1 is returned
If the current node is not the goal state, its children are generated.
If the limit is reached; 2 is returned
'''
def dfs(limit):
    global nodesCount
    while(len(fringeList)!=0):
        nodesCount+=1
        interstate= fringeList.pop()

        if(interstate.nodeMove == goalState):
            print "Moves made:"
            print interstate.nextMoves
            return '1'

        if(interstate.depth!=limit):
            findPossibleMoves(interstate)

    return '2'

'''
The method "idfs" does the Iterative Deepening Search
It will keep incrementing the depth of the tree for DFS
If the node is found at a particular depth; it will return else if the limit is reached, it will increment it and will
call the "dfs" function
'''
def idfs(inistate):

    for i in range(0,49):

        intstate= Moves(inistate,0,None," ") # add the initial state to the fringe list for each iteration
        fringeList.append(intstate)

        ret=dfs(i)

        if(ret== '1'):
            return ret

        elif(ret== '2'):
            while(len(fringeList)!=0):
                fringeList.pop(); # pop all remaining nodes in the fringe list

if __name__ == '__main__':

    print "------Iterative Deepening Search------"

    starttime=timeit.default_timer() # The time when the program starts its execution
    initialstate=getinput(7)

    result=idfs(initialstate)

    if(result == '1'):
        print "The goal is reached"

    else:
        print "The goal is not reached"

    endtime=timeit.default_timer() # The time when the program ends its execution
    runtime=endtime-starttime

    print "Number of Nodes Explored:",nodesCount
    print "Running time:",runtime,"seconds"
