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
		return (testPos[2]-targetPos)**2	#only calcuate based off the z position

	def updateCosts(self, population, targetEffectorPos, travelDist, printer):
		for i in range(len(population)):
			#calculates a new effector position and then the resulting cost.
			printer.setParameters(population[i].getParameters())
			cost = 0
			for j in range(len(travelDist)):	#targetEffectorPos is a 2d Array
				printer.setTravelDist(travelDist[j])
				population[i].setEffectorPos(printer.getEffectorPosition())
				cost += (population[i].getEffectorPos()[2] - targetEffectorPos[j])**2
			#print  "cost", cost #the percieved deviation (difference in target z end effector position and calculated)
			population[i].setCost(cost)


	def crossover(self, newPopulation, parameters1, parameters2):
		#average a random parameter and append the new thing to the population array.
		indiv = individual()
		newParameters = []
		for i in range(len(parameters1)):
			newParameters.append( (parameters1[i]+parameters2[i]) /2)
		indiv.setParameters(newParameters)

		newPopulation.append(indiv)

	def mutateIndiv(self, indiv, scaleFactor):
		parameters = self.mutate(indiv.getParameters(),scaleFactor)
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
		mutationChance     = 0.5
		scaleFactor = 1

		numKill = 30 #how many of the population to kill each time
		numIterations = 1000
		for i in range(numIterations):

			#try different muatation rates: constant, linear decay, exponential decay
			#scaleFactor = 1 - i/(numIterations)	#linear decay
			#scaleFactor = math.exp(-numIterations/10) #exponenetial decay


			#make less chance of mutation for better, or only accept mutation if beneficial
			#possible issue zeroing in on solution since all have a chance to mutate.
			for indiv in population:
				if (random.random() < mutationChance):
					self.mutateIndiv(indiv, scaleFactor)

			self.updateCosts(population, targetEffectorPos, travelDist, printer)



			population = sorted(population, key=lambda individual: individual.cost)

			iteration = 0
			childrenToMake = numKill 	#we want the population to remain at a constant size
			population = population[0:len(population)-numKill]	#remove the ones we want to destroy

			while not(childrenToMake == 1):	#keeps iterating until there is only one child to make
				numChild = childrenToMake/2
				childrenToMake -= numChild
				for i in range(numChild):
					self.crossover(population, population[i].getParameters(), population[iteration].getParameters())
					
				iteration += 1
			self.crossover(population, population[0].getParameters(), population[1].getParameters())
	
		return population


	def run(self):
		targetParameters = 	[
								-86.6,  86,   0,		#lower x
								-50,   -50, 100,		#lower y

								-86.6,  86,   0,	    #upper x
								-50,   -50, 100,		#upper y
							]

		startParameters = 	[
								-85.6,  85,   1,	    #lower x
								-51,   -51, 99,		#lower y

								-85.6,  85,   1,	    #upper x
								-51,   -51, 101,		#upper y
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
		]
		'''
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
		'''

		printer = PrinterModel.PrinterModel()
		printer.setParameters(targetParameters)


		targetEffectorPos = []
		for i in travelDist:
			printer.setTravelDist(i)
			targetEffectorPos.append( printer.getEffectorPosition()[2] )	#only get the z value

		population = self.createPopulation(startParameters, 100)

		population = self.geneticSelection(population, targetEffectorPos, travelDist, printer)

		#for i in population:
		#	print i.getParameters()
		
		print population[0].getParameters()

		realCost = 0
		parameters = population[0].getParameters()
		for i in range(len(parameters)):
			realCost+=(parameters[i]-targetParameters[i])**2
		print "realCost:", math.sqrt(realCost)

if (__name__ == "__main__"):
	printer = PrinterModel.PrinterModel()
	ga = GeneticOptimization()
	for i in range(5):
		ga.run()
