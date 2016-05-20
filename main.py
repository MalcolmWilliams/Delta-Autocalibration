import PrinterModel
import math
import random


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

	parameters = []

	effectorPos = []

	cost = 0	#correctness of the solution. this dictates which have a higher chance of being selected and crossed over. 


	def setParameters(self, newparameters):
		self.parameters = newparameters

	def setEffectorPos(self, newEffectorPos):
		self.effectorPos = newEffectorPos

	def setCost(self, newCost):
		self.cost = newCost

	def getparameters(self):
		return self.parameters

	def getEffectorPos(self):
		return self.effectorPos

	def getCost(self):
		return self.cost



def calculateCost(testPos, targetPos):
	cost = 0
	for i in range(3):
		cost += (testPos[i] - targetPos[i])**2
	#print cost
	#print testPos, targetPos
	return math.sqrt(cost)

def updateCosts(targetEffectorPos):
	maxCost = 0.0001
	print"costs"
	for i in range(len(population)):
		#calculates a new effector position and then the resulting cost.
		printer.setParameters(population[i].getparameters())
		#print population[i].getparameters()
		#print "printer effector position:", printer.getEffectorPosition()
		population[i].setEffectorPos(printer.getEffectorPosition())
		cost = calculateCost(population[i].getEffectorPos(), targetEffectorPos)
		population[i].setCost(cost)

		if (maxCost < cost):
			maxCost = cost
		#print cost
		print cost

	print "maxCost\n", maxCost
	return maxCost

def crossover(newPopulation, parameters1, parameters2):
	#average a random parameter and append the new thing to the population array.
	#for i in range(2):
	indiv = individual()
	randomInt = random.randint(0,len(parameters1)-1)
	#print parameters1, parameters2	
	parameters = list(parameters1)	#once this is verified as workign this should be changed to make the second child based off the first parameter set
	parameters[randomInt] = (parameters1[randomInt] + parameters2[randomInt] ) /2
	indiv.setParameters(parameters)
	newPopulation.append(indiv)

def mutateIndiv(indiv):
	parameters = mutate(indiv.getparameters())
	indiv.setParameters(parameters)

def mutate (parameters):
	scaleFactor = 1
	randomInt = random.randint(0,len(parameters)-1)
	randomVal = random.random() * scaleFactor - 0.5 * scaleFactor
	parameters[randomInt] = parameters[randomInt] + randomVal
	return parameters

def createPopulation(startParameters, size):
	#creates an initial population that has some starting variability
	population = []
	for i in range(size):
		parameters = list(startParameters)
		indiv = individual()
		parameters = mutate(parameters)
		#print parameters
		indiv.setParameters(parameters)
		population.append(indiv)
	return population

def geneticSelection(population, targetEffectorPos, selectionThreshold, rejectionThreshold, mutationChance):
	readyForCrossover = False
	crossoverParams = []
	normalCost = 0
	for i in range(4):
		print "new Iteration"
		maxCost = updateCosts(targetEffectorPos)
		
		newPopulation = []
		tempPopulation = population[:]
		print "normalCost1"
		for i in list(tempPopulation):	#iterate over a copy of the original population, so we can modify the original
			
			normalCost = i.getCost()/maxCost	#sets the normalised cost of the parameters, smaller is better, between 0 and 1
			print normalCost
			#do the genetic stuff
			
			if (normalCost > selectionThreshold):
				newPopulation.append(i)
				if (readyForCrossover):
					#do crossover stuff
					crossover(newPopulation, i.getparameters(), crossoverParams)	#should add two new individuals to keep population size constant
					readyForCrossover = False
				else:
					readyForCrossover = True
					crossoverParams = i.getparameters()
			
			if (normalCost > rejectionThreshold):	#is mediocre and we want to keep it
				newPopulation.append(i)
			

				#destroy the individual
			#the ones between the two thresholds dont get destroyed, but also dont get to reproduce
		
		#random mutation chance for each individual in population:
		population = newPopulation[:]
		'''
		for indiv in population:
			if (random.random() < mutationChance):
				mutateIndiv(indiv)
		'''
		
		print "normalCosts"
		for i in population:
			print i.getCost()/maxCost
		print "len: ", len(population)
		





targetParameters = 	[
						-86.6,  86,   0,		#lower x
						-50,   -50, 100,		#lower y

						-86.6,  86,   0,	    #upper x
						-50,   -50, 100,		#upper y
					]



StartParameters = 	[
						-85.6,  86,   0,	    #lower x
						-50,   -50, 100,		#lower y

						-86.6,  86,   0,	    #upper x
						-50,   -50, 100,		#upper y
					]



printer = PrinterModel.PrinterModel()

printer.setParameters(targetParameters)
targetEffectorPos = printer.getEffectorPosition()

population = createPopulation(StartParameters, 10)


selectionThreshold = 0.8
rejectionThreshold = 0.2
mutationChance     = 0.5
geneticSelection(population, targetEffectorPos, selectionThreshold, rejectionThreshold, mutationChance)





for i in population:
	print i.getparameters()
print len(population)

'''
population.remove(population[0])

for i in population:
	print i.getparameters()
print len(population)
'''