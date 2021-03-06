# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    s = util.Stack()
    visited = []
    
    s.push((problem.getStartState(), []))
    
    while not s.isEmpty():
        curState, curPath = s.pop()
        
        if problem.isGoalState(curState):
            return curPath
        
        visited.append(curState)
        for nextState, action, cost in problem.getSuccessors(curState):
            if nextState not in visited:
                s.push((nextState, curPath + [action]))
        
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    q = util.Queue()
    visited = []
    
    q.push((problem.getStartState(), []))
    
    while not q.isEmpty():
        curState, curPath = q.pop()
        
        if problem.isGoalState(curState):
            return curPath
            
        if curState not in visited:
            visited.append(curState)
            for nextState, action, cost in problem.getSuccessors(curState):
                q.push((nextState, curPath + [action]))
            
    return []

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    # note in this method, it adds node to explored set at the same time when pushing it 
    # to the queue, which is not the same as the pseudo code given by teacher
    '''
    q = util.PriorityQueue()
    visited = {}
    
    q.push((problem.getStartState(), []), 0)
    visited[problem.getStartState()] = 0
    
    while not q.isEmpty():
        curState, curPath = q.pop()
        
        if problem.isGoalState(curState):
            return curPath
    
        for nextState, action, cost in problem.getSuccessors(curState):
            if nextState not in visited.keys(): 
                visited[nextState] =  cost + visited[curState]
                q.push((nextState, curPath + [action]), visited[nextState])     
            elif visited[curState] + cost < visited[nextState]:
                visited[nextState] = visited[curState] + cost
                q.push((nextState, curPath + [action]), visited[nextState])
    
    return []
    '''
    q = util.PriorityQueue()
    visited = []
    
    q.push((problem.getStartState(), [], 0), 0)
    
    while not q.isEmpty():
        curState, curPath, curCost = q.pop()
        
        if problem.isGoalState(curState):
            return curPath
            
        if curState not in visited:
            visited.append(curState)
            for nextState, action, cost in problem.getSuccessors(curState):
                q.push((nextState, curPath + [action], curCost + cost), curCost + cost)
    
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    # note in this method, it adds node to explored set at the same time when pushing it 
    # to the queue, which is not the same as the pseudo code given by teacher
    '''
    # Use dictionary to implement the visited
    q = util.PriorityQueue()
    visited = {}
    
    q.push((problem.getStartState(), []), 0)
    
    visited[problem.getStartState()] = 0 + heuristic(problem.getStartState(), problem)
    
    while not q.isEmpty():
        curState, curPath = q.pop()
        
        if problem.isGoalState(curState):
            return curPath
        
        for nextState, action, cost in problem.getSuccessors(curState):
            h = heuristic(nextState, problem)
            if nextState not in visited.keys():
                visited[nextState] = visited[curState] + cost
                q.push((nextState, curPath + [action]), visited[nextState] + h)
            elif visited[curState] + cost < visited[nextState]:
                visited[nextState] = visited[curState] + cost + h
                q.push((nextState, curPath + [action]), visited[nextState] + h)
                
    return []
    '''
    
    # Use set to implement the visited
    q = util.PriorityQueue()
    visited = []
    
    initHVal = heuristic(problem.getStartState(), problem)
    q.push((problem.getStartState(), [], 0), initHVal)
    #visited.add(problem.getStartState())
    
    while not q.isEmpty():
        curState, curPath, curCost = q.pop()
        
        if problem.isGoalState(curState):
            return curPath
        
        if curState not in visited:
            visited.append(curState)
            for nextState, action, cost in problem.getSuccessors(curState):
                hVal = heuristic(nextState, problem)
                q.push((nextState, curPath + [action], curCost + cost), curCost + cost + hVal)
    return []
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
