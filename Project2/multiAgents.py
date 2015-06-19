# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import math
import timeit
from game import Agent

minMaxNodes=0
alphaBetaNodes=0
"""
The 'getDistance' function is used to get the distance between the ghost and the Pacman
"""
def getDistance(x1,y1,x2,y2):
    dis=math.pow((x1-x2),2)+math.pow((y1-y2),2)
    dist=math.sqrt(dis)

    return dist

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions() # a list of legal actions : Stop/North/South/East/West

        if "Stop" in legalMoves:
            legalMoves.remove("Stop")


        # Choose one of the best actions
        for action in legalMoves:
            scores = [self.evaluationFunction(gameState, action) for action in legalMoves]

        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        evalScore=0

        successorGameState = currentGameState.generatePacmanSuccessor(action) # for a corresponding action, what is the next state

        newPos = successorGameState.getPacmanPosition()
        # The food positions in the current state
        oldFood = currentGameState.getFood().asList()

        # The food positions in the successor state
        newFood = successorGameState.getFood().asList()

        iniScore=successorGameState.getScore()

        lenOldFood=len(oldFood) # Number of food positions in the current state
        lenNewFood=len(newFood) # Number of food positions in the successor state

        foodDistances=list() # List of distances of food from the Pacman

        for i in newFood:
            d=manhattanDistance(i,newPos)
            foodDistances.append(d)

        minFood=float("inf")

        for i in range(0,len(foodDistances)): #To get the food which is close to the Pacman
            if(foodDistances[i]<minFood):
                minFood=float(foodDistances[i])

        """
        If the number of food in successor state is less than the current state, then the current position is food.
        More score should be added to it
        """
        if((lenNewFood) < (lenOldFood)):
            x= iniScore+2000
        else:
            x=iniScore

        """
        If the minimum distance from the food is not zero, then reciprocal of the distance is added so that the food
        that is close is given more value
        """
        if(minFood!=0):
            evalScore=iniScore+x+100/minFood
        else:
            evalScore=iniScore+x+1000



        newGhostStates = successorGameState.getGhostStates()
        ghostPos=successorGameState.getGhostPosition(1)

        """
        Distance from the ghost is calculated. If the ghost is far, the distance is more than 1 and more value is added
        """
        ghostDist=getDistance(ghostPos[0],ghostPos[1],newPos[0],newPos[1])


        if(ghostDist>1):
            evalScore+=1200
        elif(ghostDist==1):
            evalScore+=0
        elif(ghostDist==0):
            evalScore-=100

        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        """
        The total evaluation score from the distance between the Pacman and food ; Pacman and ghost
        """
        return evalScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):

          #Returns the minimax action from the current gameState using self.depth
          #and self.evaluationFunction.

          #Here are some method calls that might be useful when implementing minimax.

        numAgents=gameState.getNumAgents() # total number of agents; Used to keep a track of current agent

        agentIndex=0 #Pacman

        legalMoves=gameState.getLegalActions(agentIndex)

        if "Stop" in legalMoves: #Stop is removed from the legalMoves
            legalMoves.remove("Stop")

        """
        The initial move in the game is made my MAX agent i.e. the Pacman whose agentIndex is 0
        The next move is the MIN agent or the ghost at agentIndex 1
        The MINMAX tree is generated to its entirety. Pacman will pick that move whose score is more.

        The scores list will have all the values corresponding to each the Pacman will make.
        The move that has maximum will be picked. If there are more than one moves with same max value, then one of it
        will be chosen randomly.
        """

        scores=[self.minMove((agentIndex+1)%numAgents,gameState.generateSuccessor(agentIndex,action),numAgents,self.depth,self.evaluationFunction) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        #print "Number of Nodes expanded:",minMaxNodes
        return legalMoves[chosenIndex]


    def maxMove(self,agentIndex,state,numAgents,depth,evalFunc):

        """
        This function corresponds to the move Pacman makes.
        """
        global minMaxNodes;
        minMaxNodes=minMaxNodes+1
        """
        If the given depth is reached or the game is over(Pacman lost or won), evaluation function is applied on the current
        state and the value is returned.
        """


        if(depth==0 or state.isWin() or state.isLose()):
            return evalFunc(state)


        temp=float("-inf")

        """
        The minMove function is called with next ghost.
        If the value returned is greater than the current value, then it is updated.
        """
        legalMoves=state.getLegalActions(agentIndex)
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")

        for action in legalMoves:
            successor=state.generateSuccessor(agentIndex,action)
            retval=self.minMove((agentIndex+1)%numAgents,successor,numAgents,depth,evalFunc)

            if(retval>temp):
                temp=retval

        return temp


    def minMove(self,agentIndex,state,numAgents,depth,evalFunc):

        global minMaxNodes;
        minMaxNodes=minMaxNodes+1

        if(depth==0 or state.isWin() or state.isLose()):
            return evalFunc(state)

        temp=float("inf")
        legalMoves=state.getLegalActions(agentIndex)
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")

        """
        If the next agent is Pacman at agentIndex:0, then maxMove function is called with the depth decreased by 1.
        Else, minMove is called with no change in depth.

        If the value returned is less than the current value, then it is updated.
        """
        for action in legalMoves:
            successor=state.generateSuccessor(agentIndex,action)

            if(((agentIndex+1)%numAgents)==0):
                retval=self.maxMove((agentIndex+1)%numAgents,successor,numAgents,depth-1,evalFunc)

            else:
                retval=self.minMove((agentIndex+1)%numAgents,successor,numAgents,depth,evalFunc)



            if(retval<temp):
                temp=retval

        return temp

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):

          #Returns the minimax action from the current gameState using self.depth
          #and self.evaluationFunction.

          #Here are some method calls that might be useful when implementing minimax.

        numAgents=gameState.getNumAgents() # total number of agents

        agentIndex=0 # Pacman

        alpha=float("-inf")
        beta=float("inf")

        legalMoves=gameState.getLegalActions(agentIndex)
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")

        bestAction=""
        retval=float("-inf")

        for action in legalMoves:
            successor=gameState.generateSuccessor(agentIndex,action)
            retval=max(retval,self.alphaBetaMinMove((agentIndex+1)%numAgents,successor,numAgents,alpha,beta,self.depth,self.evaluationFunction))
            """
            If the value is greater than beta; then return
            """
            if(retval>=beta):
                return bestAction

            if(retval>alpha): #update alpha value accordingly
                alpha=retval
                bestAction=action


        return bestAction


    def alphaBetaMaxMove(self,agentIndex,state,numAgents,alpha,beta,depth,evalFunc):

        global alphaBetaNodes;
        alphaBetaNodes=alphaBetaNodes+1
        """
        If the given depth is reached or the game is over(Pacman lost or won), evaluation function is applied on the current
        state and the value is returned.
        """

        if(depth==0 or state.isWin() or state.isLose()):
            return evalFunc(state)

        retval=float("-inf")


        legalMoves=state.getLegalActions(agentIndex)
        """
        The alphaBetaMinMove function without decreasing the depth, but increasing the agentIndex which will consider the first ghost
        """
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")


        for action in legalMoves:
            successor=state.generateSuccessor(agentIndex,action)
            retval=max(retval,self.alphaBetaMinMove((agentIndex+1)%numAgents,successor,numAgents,alpha,beta,depth,evalFunc))

            if(retval>=beta):  #If the value of alpha is greater than or equal to beta, return the value; This does pruning
                return retval

            if(retval>alpha): #update alpha value
                alpha=retval


        return alpha


    def alphaBetaMinMove(self,agentIndex,state,numAgents,alpha,beta,depth,evalFunc):

        global alphaBetaNodes;
        alphaBetaNodes=alphaBetaNodes+1
        """
        If the given depth is reached or the game is over(Pacman lost or won), evaluation function is applied on the current
        state and the value is returned.
        """

        if(depth==0 or state.isWin() or state.isLose()):
            return evalFunc(state)

        retval=float("inf")
        legalMoves=state.getLegalActions(agentIndex)

        if "Stop" in legalMoves:
            legalMoves.remove("Stop")

        """
        If the next agent is Pacman at agentIndex:0, then maxMove function is called with the depth decreased by 1.
        Else, minMove is called with no change in depth.
        """

        for action in legalMoves:
            successor=state.generateSuccessor(agentIndex,action)

            if(((agentIndex+1)%numAgents)==0):
                retval=min(retval,self.alphaBetaMaxMove((agentIndex+1)%numAgents,successor,numAgents,alpha,beta,depth-1,evalFunc))

            else:
                retval=min(retval,self.alphaBetaMinMove((agentIndex+1)%numAgents,successor,numAgents,alpha,beta,depth,evalFunc))



            if(retval<=alpha): # if beta is less than or equal to alpha, return
                return retval

            if(retval<beta): # update beta accordingly
                beta=retval



        return beta

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

