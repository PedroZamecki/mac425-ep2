# multiAgents.py
# --------------
# EP 2 - Inteligência Artificial
# Integrante:
#   - Pedro Zamecki Andrade 11207800


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        if successorGameState.isWin():
            return float("inf")
        if successorGameState.isLose():
            return float("-inf")
        
        foodList = newFood.asList()
        foodDistances = [manhattanDistance(newPos, food) for food in foodList]
        minFoodDistance = min(foodDistances) if len(foodDistances) > 0 else 0

        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        minGhostDistance = min(ghostDistances) if len(ghostDistances) > 0 else 0

        # Scared ghosts are not a threat
        if minGhostDistance > 0 and minGhostDistance < 3 and newScaredTimes[0] == 0:
            return float("-inf")
        
        return successorGameState.getScore() + 1 / minFoodDistance - 1 / minGhostDistance

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def maxState(state,depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = float("-inf")
            for action in state.getLegalActions(agentIndex):
                v = max(v, minState(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
            return v
        
        def minState(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = float("inf")
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:
                    v = min(v, maxState(state.generateSuccessor(agentIndex, action), depth + 1, 0))
                else:
                    v = min(v, minState(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
            return v
        
        bestAction = Directions.STOP
        bestScore = float("-inf")
        for action in gameState.getLegalActions(0):
            score = minState(gameState.generateSuccessor(0, action), 0, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def maxState(state,depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = float("-inf")
            for action in state.getLegalActions(agentIndex):
                v = max(v, minState(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v
        
        def minState(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = float("inf")
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:
                    v = min(v, maxState(state.generateSuccessor(agentIndex, action), depth + 1, 0, alpha, beta))
                else:
                    v = min(v, minState(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        
        bestAction = Directions.STOP
        bestScore = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        for action in gameState.getLegalActions(0):
            score = minState(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, bestScore)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def maxState(state,depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = float("-inf")
            for action in state.getLegalActions(agentIndex):
                v = max(v, minState(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1))
            return v
        
        def minState(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            v = 0
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:
                    v += maxState(state.generateSuccessor(agentIndex, action), depth + 1, 0)
                else:
                    v += minState(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            return v/len(state.getLegalActions(agentIndex))
        
        bestAction = Directions.STOP
        bestScore = float("-inf")
        for action in gameState.getLegalActions(0):
            score = minState(gameState.generateSuccessor(0, action), 0, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
