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

class individual( object ):
	# a single member of the larger population

	parameters = []

	effectorPos = []

	cost = 0	#correctness of the solution. this dictates which have a higher chance of being selected and crossed over

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


class GeneticOptimization( object ):
	def calculateCost(self, testPos, targetPos):
		'''
		cost = 0
		for i in range(3):
			cost += (testPos[i] - targetPos[i])**2
		return cost
		'''
		return (testPos[2]-targetPos)**2

	def updateCosts(self, population, targetEffectorPos, travelDist, printer):
		for i in range(len(population)):
			#calculates a new effector position and then the resulting cost.
			printer.setParameters(population[i].getParameters())
			cost = 0
			for j in range(len(travelDist)):	#targetEffectorPos is a 2d Array
				printer.setParameters(travelDist[j])
				population[i].setEffectorPos(printer.getEffectorPosition())
				cost += self.calculateCost(population[i].getEffectorPos(), targetEffectorPos[j])
			population[i].setCost(cost)


	def crossover(self, newPopulation, parameters1, parameters2):
		#average a random parameter and append the new thing to the population array.
		indiv = individual()
		newParameters = []
		for i in range(len(parameters1)):
			newParameters.append( (parameters1[i]+parameters2[i]) /2)
		indiv.setParameters(newParameters)

		newPopulation.append(indiv)

	def mutateIndiv(self, indiv):
		parameters = self.mutate(indiv.getParameters(),1)
		indiv.setParameters(parameters)

	def mutate (self, parameters, scaleFactor):
		randomInt = random.randint(0,len(parameters)-1)
		randomVal = random.random() * scaleFactor - 0.5 * scaleFactor
		parameters[randomInt] = parameters[randomInt] + randomVal
		return parameters

	def createPopulation(self, startParameters, size):
		#creates an initial population that has some starting variability
		population = []
		for i in range(size):
			parameters = list(startParameters)
			indiv = individual()
			parameters = self.mutate(parameters,1)
			indiv.setParameters(parameters)
			population.append(indiv)
		return population

	def geneticSelection(self, population, targetEffectorPos, travelDist, printer):
		selectionThreshold = 0.6
		rejectionThreshold = 0.2
		mutationChance     = 0.5
		timeSinceLastExtinction = 0

		for i in range(1000):
			#print "new Iteration"
			self.updateCosts(population, targetEffectorPos, travelDist, printer)

			population = sorted(population, key=lambda individual: individual.cost)

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
			
			self.crossover(population, population[0].getParameters(), population[1].getParameters())
			self.crossover(population, population[0].getParameters(), population[1].getParameters())
			self.crossover(population, population[2].getParameters(), population[3].getParameters())

			
			#have a chance of mutating everything
			for indiv in population:
				if (random.random() < mutationChance):
					self.mutateIndiv(indiv)

			'''	
			timeSinceLastExtinction+=1
			#extinction event
			if (timeSinceLastExtinction == 100):
				population = self.createPopulation(population[0].getParameters(), 10)
				timeSinceLastExtinction = 0
			'''
			
		return population


	def run(self):
		targetParameters = 	[
								-86.6,  86,   0,		#lower x
								-50,   -50, 100,		#lower y

								-86.6,  86,   0,	    #upper x
								-50,   -50, 100,		#upper y
							]

		startParameters = 	[
								-85.6,  86,   0,	    #lower x
								-50,   -50, 100,		#lower y

								-86.6,  86,   0,	    #upper x
								-50,   -50, 100,		#upper y
							]

		#the set of carriage locations to generate the test points
		travelDist = [
			[49.999, 50, 50],
			[30, 50, 50],
			[50, 30, 50],
			[49.999, 50, 30],

			[10, 50, 50],
			[50, 10, 50],
			[49.999, 50, 10],

			[30.001, 30, 50],
			[50, 30, 30],
			[30, 50, 30],

			[10.001, 10, 50],
			[50, 10, 10],
			[10, 50, 10],



			[69.999, 70, 70],
			[30, 70, 70],
			[70, 30, 70],
			[69.999, 70, 30],

			[10, 70, 70],
			[70, 10, 70],
			[69.999, 70, 10],

			[30.001, 30, 70],
			[70, 30, 30],
			[30, 70, 30],

			[10.001, 10, 70],
			[70, 10, 10],
			[10, 70, 10],
			]

		printer = PrinterModel.PrinterModel()
		printer.setParameters(targetParameters)


		targetEffectorPos = []
		for i in travelDist:
			printer.setParameters(i)
			targetEffectorPos.append( printer.getEffectorPosition()[2] )	#only get the z value

		population = self.createPopulation(startParameters, 10)

		population = self.geneticSelection(population, targetEffectorPos, travelDist, printer)

		#for i in population:
		#	print i.getParameters()
		
		realCost = 0
		parameters = population[0].getParameters()
		for i in range(len(parameters)):
			realCost+=(parameters[i]-startParameters[i])**2
		print "realCost:", math.sqrt(realCost) 

if (__name__ == "__main__"):
	printer = PrinterModel.PrinterModel()
	ga = GeneticOptimization()
	for i in range(3):
		ga.run()
