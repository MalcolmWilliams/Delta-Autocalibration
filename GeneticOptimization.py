import PrinterModel
import math
import random
import time

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
	populationSize = 100
	numKill = 30
	mutationChance = 0.5
	muationScale = 1
	numIterations = 1000
	crossoverType = 1

	def __init__(self, populationSize, numKill, mutationChance, mutationScale, numIterations, crossoverType):
		self.populationSize = populationSize
		self.numKill = numKill
		self.mutationChance = mutationChance
		self.mutationScale = mutationScale
		self.numIterations = numIterations
		self.crossoverType = crossoverType

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


	def crossoverAverage(self, newPopulation, parameters1, parameters2):
		#average a random parameter and append the new thing to the population array.
		indiv = individual()
		newParameters = []
		for i in range(len(parameters1)):
			newParameters.append( (parameters1[i]+parameters2[i]) /2)
		indiv.setParameters(newParameters)

		newPopulation.append(indiv)

	def crossoverRandomAverage(self, newPopulation, parameters1, parameters2):
		#average a random parameter and append the new thing to the population array.
		indiv = individual()
		newParameters = []
		for i in range(len(parameters1)):
			if(random.random() < 0.5):
				newParameters.append( (parameters1[i]+parameters2[i]) /2)
			else:
				newParameters.append(parameters1)	#skew towards the more favorable one.
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

	def crossover1(self, population):

		iteration = 0
		childrenToMake = self.numKill 	#we want the population to remain at a constant size
		population = population[0:len(population)-self.numKill]	#remove the ones we want to destroy

		while not(childrenToMake == 1):	#keeps iterating until there is only one child to make
			numChild = childrenToMake/2
			childrenToMake -= numChild
			for i in range(numChild):
				self.crossoverAverage(population, population[i].getParameters(), population[iteration].getParameters())
				
			iteration += 1
		self.crossoverAverage(population, population[0].getParameters(), population[1].getParameters())

	def crossover2(self, population):
		
		iteration = 0
		childrenToMake = self.numKill 	#we want the population to remain at a constant size
		population = population[0:len(population)-self.numKill]	#remove the ones we want to destroy

		while not(childrenToMake == 1):	#keeps iterating until there is only one child to make
			numChild = childrenToMake/2
			childrenToMake -= numChild
			for i in range(numChild):
				self.crossoverRandomAverage(population, population[i].getParameters(), population[iteration].getParameters())
				
			iteration += 1
		self.crossoverRandomAverage(population, population[0].getParameters(), population[1].getParameters())
	
	def crossover3(self, population):
		val = 0


	def geneticSelection(self, population, targetEffectorPos, travelDist, printer):
		#mutationChance     = 0.5
		#scaleFactor = 1

		#numKill = 30 #how many of the population to kill each time
		#numIterations = 1000
		for i in range(self.numIterations):

			#try different muatation rates: constant, linear decay, exponential decay
			#scaleFactor = 1 - i/(numIterations)	#linear decay
			#scaleFactor = math.exp(-numIterations/10) #exponenetial decay


			#make less chance of mutation for better, or only accept mutation if beneficial
			#possible issue zeroing in on solution since all have a chance to mutate.
			for indiv in population:
				if (random.random() < self.mutationChance):
					self.mutateIndiv(indiv, self.mutationScale)

			self.updateCosts(population, targetEffectorPos, travelDist, printer)



			population = sorted(population, key=lambda individual: individual.cost)
			if(self.crossoverType == 1):
				self.crossover1(population)
			elif(self.crossoverType == 2):
				self.crossover2(population)
			#else:
			#	self.crossover3(population)
	
		return population


	def run(self, targetParameters):

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

		population = self.createPopulation(startParameters, self.populationSize)

		population = self.geneticSelection(population, targetEffectorPos, travelDist, printer)

		#for i in population:
		#	print i.getParameters()
		
		return population


if (__name__ == "__main__"):
	printer = PrinterModel.PrinterModel()
	

	targetParameters = 	[
							-86.6,  86,   0,		#lower x
							-50,   -50, 100,		#lower y

							-86.6,  86,   0,	    #upper x
							-50,   -50, 100,		#upper y
						]

	populationSize = [100, 1000, 10000]
	numKillRatio = [10, 3, 2]  # = [10, 30, 50, 100, 300, 500, 1000, 3000, 5000]
	mutationChance = [0.3, 0.5, 0.8]
	mutationScale = [0.5,1,2]
	numIterations = [100, 1000]#, 10000]
	crossoverType = [1, 2]

	f = open("log.txt", "w")


	f.write("populationSize, numKillRatio, mutationChance, mutationScale, numIterations, crossoverType, realCost1, realCost2, realCost3, averageCost\n")

	for p in populationSize:
		for nKR in numKillRatio:
			for mC in mutationChance:
				for mS in mutationScale:
					for nI in numIterations:
						for cT in crossoverType:
							f.write(str(p) +", "+ str(nKR) +", "+ str(mC) +", "+ str(mS) +", "+ str(nI) +", "+ str(cT) + ", ")
							print (str(p) +", "+ str(nKR) +", "+ str(mC) +", "+ str(mS) +", "+ str(nI) +", "+ str(cT) + ", "),
							ga = GeneticOptimization(p, (p/nKR), mC, mS, nI, cT)
							averageCost = 0
							for i in range(3):
								realCost = 0
								population = ga.run(targetParameters)
								parameters = population[0].getParameters()
								for i in range(len(parameters)):
									realCost+=(parameters[i] - targetParameters[i])**2
								realCost = math.sqrt(realCost)
								averageCost+= realCost
								f.write(str(realCost) + ", ")
								print (str(realCost) + ", "),
							f.write(str(averageCost) + "\n")
							print (str(averageCost) + "\n"),
	f.close()



'''
		print population[0].getParameters()

		realCost = 0
		parameters = population[0].getParameters()
		for i in range(len(parameters)):
			realCost+=(parameters[i]-targetParameters[i])**2
		print "realCost:", math.sqrt(realCost)




	ga = GeneticOptimization(100, 30, 0.5, 1, 1000, 1)
	for i in range(5):
	 	ga.run()
'''
