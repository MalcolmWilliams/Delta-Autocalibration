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

	def getParameters(self):
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
	return cost

def updateCosts(population, targetEffectorPos):
	#maxCost = 0
	#print"costs"
	for i in range(len(population)):
		#calculates a new effector position and then the resulting cost.
		printer.setParameters(population[i].getParameters())
		#print population[i].getParameters()
		#print "printer effector position:", printer.getEffectorPosition()
		population[i].setEffectorPos(printer.getEffectorPosition())
		cost = calculateCost(population[i].getEffectorPos(), targetEffectorPos)
		population[i].setCost(cost)

		#if (maxCost < cost):
		#	maxCost = cost
		#print cost
		#print cost

	#print "maxCost\n", maxCost
	#return maxCost

def crossover(newPopulation, parameters1, parameters2):
	#average a random parameter and append the new thing to the population array.
	#for i in range(2):
	indiv = individual()
	#randomInt = random.randint(0,len(parameters1)-1)
	#print parameters1, parameters2	
	#parameters = list(parameters1)	#once this is verified as workign this should be changed to make the second child based off the first parameter set
	#parameters[randomInt] = (parameters1[randomInt] + parameters2[randomInt] ) /2
	newParameters = []
	for i in range(len(parameters1)):
		newParameters.append( (parameters1[i]+parameters2[i]) /2)
	indiv.setParameters(newParameters)

	newPopulation.append(indiv)

def mutateIndiv(indiv):
	parameters = mutate(indiv.getParameters())
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

def geneticSelection(population, targetEffectorPos):
	selectionThreshold = 0.6
	rejectionThreshold = 0.2
	mutationChance     = 0.5

	for i in range(1000):
		#print "new Iteration"
		updateCosts(population, targetEffectorPos)



		population = sorted(population, key=lambda individual: individual.cost)

		'''
		for i in range(len(population)):
			print population[i].getCost()
		print "\n"
		'''
		#print(len(population))

		
		#bottom third: deleted
		#middle third: kept
		#top third: makes children, better score = more children
		#hardcode population size for now, eventually have it able to support arbitrary population sizes

		#hardcoded values: 
		#0&1: 2 children
		#2&3: 1 child
		#4,5,6: keep
		#7,8,9 delete


		population.remove(population[9])
		population.remove(population[8])
		population.remove(population[7])

		crossover(population, population[0].getParameters(), population[1].getParameters())
		crossover(population, population[0].getParameters(), population[1].getParameters())
		crossover(population, population[2].getParameters(), population[3].getParameters())

		



		#print normalCost
		#do the genetic stuff
		'''
		if (normalCost > selectionThreshold):
			newPopulation.append(i)
			#newPopulation.append(i)
			if (readyForCrossover):
				#do crossover stuff
				crossover(newPopulation, i.getParameters(), crossoverParams)	#should add two new individuals to keep population size constant
				readyForCrossover = False
			else:
				readyForCrossover = True
				crossoverParams = i.getParameters()
		'''
		
		
		#have a chance of mutating everything
		for indiv in population:
			if (random.random() < mutationChance):
				mutateIndiv(indiv)
		
				
		#print "len: ", len(newPopulation)
	return population
		





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



population = geneticSelection(population, targetEffectorPos)





for i in population:
	print i.getParameters()
print len(population)

'''
population.remove(population[0])

for i in population:
	print i.getParameters()
print len(population)
'''