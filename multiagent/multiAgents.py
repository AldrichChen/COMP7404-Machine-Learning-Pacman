# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        prePos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        score = 0.0
        
        ghostDistance = 0.0
        closestGhost = 100000
        for i in range(len(newGhostStates)):
            tmpGhostPos = successorGameState.getGhostPosition(i + 1)
            tmpDistance = abs(newPos[0] - tmpGhostPos[0]) + abs(newPos[1] - tmpGhostPos[1])
            ghostDistance += tmpDistance
            closestGhost = closestGhost if closestGhost < tmpDistance else tmpDistance
            
        
        closestFood = 100000
        closestFood2 = 100000
        for x in range(newFood.width):
            for y in range(newFood.height):
                if successorGameState.hasFood(x, y):
                    tmpFoodDistance = abs(newPos[0] - x) + abs(newPos[1] - y)
                    closestFood = closestFood if closestFood < tmpFoodDistance else tmpFoodDistance
                    tmpFoodDistance2 = abs(prePos[0] - x) + abs(prePos[1] - y)
                    closestFood2 = closestFood2 if closestFood < tmpFoodDistance2 else tmpFoodDistance2
                    
        if closestFood < closestFood2:
            score += 10
                    
        dist = [(abs(newPos[0] - ghost.getPosition()[0]) + abs(newPos[1] - ghost.getPosition()[1])) for ghost in newGhostStates]
        for d in dist:
            for t in newScaredTimes:
                if d <= 2 and t == 0:
                    score -= 100
            
        if successorGameState.getNumFood() == 0:
            return 1000
        score +=  -closestFood + closestGhost
        #print action, successorGameState.getScore() + isFood * 10 - closestFood + eatAround * 10
        return successorGameState.getScore() + score
        
        
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
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, self.depth)[1]
        #util.raiseNotDefined()
    
    def max_value(self, state, depth):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
            
        v = -100000
        ac = None
        legalActions = state.getLegalActions(0)
        for action in legalActions:
            successor = state.generateSuccessor(0, action)
            v_tmp = max(v, self.min_value(successor, depth, 1))
            if v_tmp > v:
                v = v_tmp
                ac = action
        return v, ac
        
    def min_value(self, state, depth, agentIndex):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        v = 100000
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            if agentIndex == state.getNumAgents() - 1:
                successor = state.generateSuccessor(agentIndex, action)
                
                tmp = self.max_value(successor, depth - 1)
                if type(tmp) != float:
                    v_tmp = min(v, tmp[0])
                    v = v if v_tmp > v else v_tmp
                else:
                    v_tmp = min(v, tmp)
                    v = v if v_tmp > v else v_tmp
                
            else:
                successor = state.generateSuccessor(agentIndex, action)
                v_tmp = min(v, self.min_value(successor, depth, agentIndex + 1))
                v = v if v_tmp > v else v_tmp
        return v
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, -100000, 100000, self.depth)[1]
        #util.raiseNotDefined()
        
    def max_value(self, state, alpha, beta, depth):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
            
        v = -100000
        ac = None
        legalActions = state.getLegalActions(0)
        for action in legalActions:
            successor = state.generateSuccessor(0, action)
            v_tmp = max(v, self.min_value(successor, alpha, beta, depth, 1))
            if v_tmp > v:
                v = v_tmp
                ac = action
            if v > beta:
                return v, action
            alpha = max(v, alpha)
        return v, ac
        
    def min_value(self, state, alpha, beta, depth, agentIndex):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        v = 100000
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            if agentIndex == state.getNumAgents() - 1:
                successor = state.generateSuccessor(agentIndex, action)
                
                tmp = self.max_value(successor, alpha, beta, depth - 1)
                if type(tmp) != float:
                    v_tmp = min(v, tmp[0])
                    v = v if v_tmp > v else v_tmp
                else:
                    v_tmp = min(v, tmp)
                    v = v if v_tmp > v else v_tmp
                
            else:
                successor = state.generateSuccessor(agentIndex, action)
                v_tmp = min(v, self.min_value(successor, alpha, beta, depth, agentIndex + 1))
                v = v if v_tmp > v else v_tmp
            
            if v < alpha: 
                return v
            beta = min(v, beta)
        return v
        

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
        return self.max_value(gameState, self.depth)[1]
        #util.raiseNotDefined()
    
    def max_value(self, state, depth):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
            
        v = -100000
        ac = None
        legalActions = state.getLegalActions(0)
        for action in legalActions:
            successor = state.generateSuccessor(0, action)
            v_tmp = max(v, self.min_value(successor, depth, 1))
            if v_tmp > v:
                v = v_tmp
                ac = action
        return v, ac
        
    def min_value(self, state, depth, agentIndex):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        legalActions = state.getLegalActions(agentIndex)
        total = 0.0
        for action in legalActions:
            v_tmp = 0.0
            if agentIndex == state.getNumAgents() - 1:
                successor = state.generateSuccessor(agentIndex, action)
                
                tmp = self.max_value(successor, depth - 1)
                if type(tmp) != float:
                    v_tmp = tmp[0]
                else:
                    v_tmp = tmp
                
            else:
                successor = state.generateSuccessor(agentIndex, action)
                v_tmp = self.min_value(successor, depth, agentIndex + 1)
                
            total += v_tmp
        return total / len(legalActions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
      
      Briefly speaking, I finish this part with the hint of the evaluation in part 2. 
      The features that could give a rise to the performance of solution are pellet, 
      food, ghost. So only consider about these features and make a reasonable 
      combination will be good enough. 
      When it comes to the weights. I just balance the features value normally, 
      for example, the count of the food will be definitely smaller than the total
      distance, so I give the total distance a larger weight to make the '1 / totaldistance'
      smaller. 
    """
    "*** YOUR CODE HERE ***"
    
    score = currentGameState.getScore()
    pacPos = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    
    closestGhost = 100000
    for i in range(len(ghosts)):
        ghostPos = currentGameState.getGhostPosition(i + 1)
        tmpDistance = abs(pacPos[0] - ghostPos[0]) + abs(pacPos[1] - ghostPos[1])
        closestGhost = tmpDistance if tmpDistance < closestGhost else closestGhost
        
    foodList = currentGameState.getFood().asList()
    foodCount = len(foodList) if foodList  else 0.01
    foodDistanceSum = sum([abs(foodPos[0] - pacPos[0]) + abs(foodPos[1] - pacPos[1]) for foodPos in foodList]) if foodList else 0.01
    
    pelletList = currentGameState.getCapsules()
    pelletCount = len(pelletList) if pelletList else 0.01
    pelletDistanceSum = sum([abs(pelletPos[0] - pacPos[0]) + abs(pelletPos[1] - pacPos[1]) for pelletPos in pelletList]) if pelletList else 0.01
    
    return score + 1 / float(closestGhost + 1) + 20 / foodCount + 5 / foodDistanceSum + 40 / pelletCount + 10 / pelletDistanceSum
    

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

