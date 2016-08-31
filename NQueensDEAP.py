'''
@author: Chimdindu Denalex Orakwue
'''

import random
import numpy as np
from deap import algorithms, base, creator, tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

#check if current position is inbounds
def checkInBounds(chessBoard, row, col):
    if row >= len(chessBoard) or col >= len(chessBoard[0]) or col < 0 or row < 0:
            return False
    return True

#checks if two queens are in the same spot
def checkDuplicate(individual):
    dup = 0
    for i in range(0, 7):
        for j in range(i + 1, 8):
            if individual[i] == individual[j]:
                dup += 4
    return dup
    
#adds queens to chess board
def evalChessBoard(individual):
    pos = 0
    chessBoard = np.zeros((8,8))
    
    for i in range(0, 8):
        for j in range(0, 8):
            if pos in individual:
                chessBoard[i][j] = 1
            pos += 1
                
    return (chessBoard)

#fitness function
def getFitness(individual):
    chessBoard = evalChessBoard(individual)
    fitness = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if chessBoard[i, j] == 1:
                fitness += checkCollide(chessBoard, i, j)
    return ((checkDuplicate(individual) + fitness) * -1,)


#checks if queens can collide
def checkCollide(chessBoard, row, col):
    numCols = 0
    
    for position in range(1, len(chessBoard)):
        if checkInBounds(chessBoard, row + position, col):
            if chessBoard[row + position][col] == 1:
                numCols += 1
        if checkInBounds(chessBoard, row - position, col):
            if chessBoard[row - position][col] == 1:
                numCols += 1
        if checkInBounds(chessBoard, row, col + position):
            if chessBoard[row][col + position] == 1:
                numCols += 1
        if checkInBounds(chessBoard, row, col - position):
            if chessBoard[row][col - position] == 1:
                numCols += 1
        if checkInBounds(chessBoard, row + position, col + position):
            if chessBoard[row + position][col + position] == 1:
                numCols += 1
        if checkInBounds(chessBoard, row - position, col - position):
            if chessBoard[row - position][col - position] == 1:
                numCols += 1
        if checkInBounds(chessBoard, row - position, col + position):
            if chessBoard[row - position][col + position] == 1:
                numCols += 1
        if checkInBounds(chessBoard, row + position, col - position):
            if chessBoard[row + position][col - position] == 1:
                numCols += 1
       
    return numCols;
    

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(64), 8)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", getFitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low = 0, up = 63, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == "__main__":
    pop = toolbox.population(n=500)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen= 300)
    
t = tools.selBest(pop, k=1)[0]
print("\npositions: " + str(t))
print (evalChessBoard(t))
