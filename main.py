import PrinterModel
import math


'''
basis of genetic algorithms

have a population of best solutions

Selection:
	rank each solution based on its deviation from target	
	higher ranked solutions have a better chance of being kept

Crossover: 
	avearge a random parameter between two solutions

Mutation:
	randomly vary a parameter

'''

class individual:
	# a single member of the larger population

	paramters = []

	effectorPos = []

	cost = 0	#correctness of the solution. this dictates which have a higher chance of being selected and crossed over. 
	normalCost = 0	#normalised from 0 to 1

	def setParameters(newParamters):
		self.paramters = newParamters

	def setEffectorPos(newEffectorPos):
		self.effectorPos = newEffectorPos

	def setCost(newCost):
		self.cost = newCost

	def getParamters():
		return self.paramters

	def getEffectorPos():
		return self.effectorPos

	def getCost():
		return self.cost

	def setNormalCost(maxCost):
		self.normalCost = cost/maxCost


def cost(testPos):
	cost = 0
	for i in range(3):
		cost += (testPos - targetPos)**2
	return math.sqrt(cost)

def updateCosts():
	maxCost = 0
	for i in range(len(population)):
		#calculates a new effector position and then the resulting cost.
		printer.setParameters(population[i].getParamters())
		population[i].setEffectorPos(printer.getEffectorPosition())
		cost = cost(population[i].getEffectorPos)
		population[i].setCost(cost)

		if (maxCost < cost):
			maxCost = cost

	return maxCost

def crossover(parameters1, parameters2):
	#average a random parameter and append the new thing to the population array.

	for i in range(2):
		indiv = individual()
		randomInt = random.randint(0,len(parameters1))
		parameters = parameters1	#once this is verified as workign this should be changed to make the second child based off the first parameter set
		parameters[randomInt] = (parameters1[randomInt] + parameters2[randomInt] ) /2
		indiv.setParameters(parameters)
		population.append(indiv)
	

def geneticSelection(selectionThreshold, rejectionThreshold):
	readyForCrossover = False
	crossoverParams = []
	normalCost = 0
	for i in range(100):
		maxCost = updateCosts()
		for indiv in list(population):	#iterate over a copy of the original population, so we can modify the original
			normalCost = indiv.getCost()/maxCost	#sets the normalised cost of the parameters, smaller is better, between 0 and 1

			#do the genetic stuff
			if (normalCost < selectionThreshold):
				if (readyForCrossover):
					#do crossover stuff
					crossover(indiv.getParamters(), crossoverParams)	#should add two new individuals to keep population size constant
					readyForCrossover = False
				else:
					readyForCrossover = True
					crossoverIdx = i

			else if (normalCost > rejectionThreshold):
				population.remove(indiv)	#not sure if this is legit

				#destroy the individual
			#the ones between the two thresholds dont get destroyed, but also dont get to reproduce

			#random mutation chance for each individual








printer = PrinterModel.PrinterModel()
print printer.getEffectorPosition()
printer.exportVars()
