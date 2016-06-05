import PrinterModel
import math
import random
import time
import datetime
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

	def __init__(self, populationSize, numKill, mutationChance, mutationScale, numIterations, crossoverType):
		self.populationSize = populationSize
		self.numKill = numKill
		self.mutationChance = mutationChance
		self.mutationScale = mutationScale
		self.numIterations = numIterations
		self.crossoverType = crossoverType

		self.traveldist = []
		self.printer = PrinterModel.PrinterModel()
		self.targetEffectorPos = []
		#self.population = []
		
		startParameters = 	[
								-76.6,  86,   0,		#lower x
								-50,   -50, 100,		#lower y

								-86.6,  86,   0,	    #upper x
								-50,   -50, 100,		#upper y
							]
		
		self.population = []
		self.createPopulation(startParameters, self.populationSize)

	def createPopulation(self, startParameters, size):
		#creates an initial population that has some starting variability
		self.population = []
		for i in range(size):
			parameters = list(startParameters)
			indiv = individual()
			parameters = self.mutate(parameters,1)
			indiv.setParameters(parameters)
			self.population.append(indiv)
	
	def calculateCost(self, testPos, targetPos):
		return (testPos[2]-targetPos)**2	#only calcuate based off the z position

	def updateCosts(self):
		#updates the costs for the entire population
		for i in range(len(self.population)):
			#calculates a new effector position and then the resulting cost.
			self.printer.setParameters(self.population[i].getParameters())
			cost = 0
			for j in range(len(self.travelDist)):	#targetEffectorPos is a 2d Array
				self.printer.setTravelDist(self.travelDist[j])
				self.population[i].setEffectorPos(self.printer.getEffectorPosition())
				cost += (self.population[i].getEffectorPos()[2] - self.targetEffectorPos[j])**2
			self.population[i].setCost(cost)

	def updateCost(self, indiv):
		#set the cost for an individual of the population
		self.printer.setParameters(indiv.getParameters())
		cost = 0
		for j in range(len(self.travelDist)):	#targetEffectorPos is a 2d Array
			self.printer.setTravelDist(self.travelDist[j])
			indiv.setEffectorPos(self.printer.getEffectorPosition())
			cost += (indiv.getEffectorPos()[2] - self.targetEffectorPos[j])**2
		#print str(cost) + " " 
		indiv.setCost(cost)

	def makeChild(self, parameters1, parameters2, idx):
		#make a new child and insert it at the given index
		newParameters = []
		for i in range(len(parameters1)):
			newParameters.append( (parameters1[i]+parameters2[i]) /2)
		self.population[idx].setParameters(newParameters)		
		if (random.random() < self.mutationChance):
			self.mutateIndiv(self.population[idx], self.mutationScale)
		self.updateCost(self.population[idx])

	def crossover(self):
		#randomly select 3 individuals. kill worst and make child with 2 best
		#each individual should always know their cost. 
		rand = []
		for i in range(3):
			temp = random.randint(0, len(self.population)-1)
			rand.append([temp, self.population[temp].getCost()])
			#rand.append( [0,1] )


		rand = sorted(rand, key=lambda rand: rand[0])
		#population.remove(population[rand[0][2]])
		self.makeChild( self.population[rand[0][0]].getParameters(), self.population[rand[1][0]].getParameters(), rand[2][0])
		#have a chance of mutating the child

	#crossover of all population
	def crossoverAverage(self, parameters1, parameters2):
		#average a random parameter and append the new thing to the population array.
		indiv = individual()
		newParameters = []
		for i in range(len(parameters1)):
			newParameters.append( (parameters1[i]+parameters2[i]) /2)
		indiv.setParameters(newParameters)

		self.population.append(indiv)

	def crossoverAll(self):
		for indiv in self.population:
			if (random.random() < self.mutationChance):
				self.mutateIndiv(indiv, self.mutationScale)
		
		self.updateCosts()
		
		self.population = sorted(self.population, key=lambda individual: individual.cost)
		print str(self.population[0].getCost()) + " "

		iteration = 0
		childrenToMake = self.numKill 	#we want the population to remain at a constant size
		self.population = self.population[0:len(self.population)-self.numKill]	#remove the ones we want to destroy

		while not(childrenToMake == 1):	#keeps iterating until there is only one child to make
			numChild = childrenToMake/2
			childrenToMake -= numChild
			for i in range(numChild):
				self.crossoverAverage(self.population[i].getParameters(), self.population[iteration].getParameters())
				
			iteration += 1
		self.crossoverAverage(self.population[0].getParameters(), self.population[1].getParameters())

	def mutateIndiv(self, indiv, scaleFactor):
		parameters = self.mutate(indiv.getParameters(),scaleFactor)
		indiv.setParameters(parameters)

	def mutate (self, parameters, scaleFactor):
		randomInt = random.randint(0,len(parameters)-1)
		randomVal = random.random() * scaleFactor - 0.5 * scaleFactor
		parameters[randomInt] = parameters[randomInt] + randomVal
		return parameters

	def geneticSelection(self):
		for i in range(self.numIterations):
		
			#try different muatation rates: constant, linear decay, exponential decay
			#scaleFactor = 1 - i/(numIterations)	#linear decay
			#scaleFactor = math.exp(-numIterations/10) #exponenetial decay


			#make less chance of mutation for better, or only accept mutation if beneficial
			#possible issue zeroing in on solution since all have a chance to mutate.
			
			
			print i,
			#self.crossover()
			self.crossoverAll()
		
	
	def run(self, targetParameters):
		#the set of carriage locations to generate the test points
		self.travelDist = [
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
		

		self.printer.setParameters(targetParameters)


		for i in self.travelDist:
			self.printer.setTravelDist(i)
			self.targetEffectorPos.append( self.printer.getEffectorPosition()[2] )	#only get the z value


		self.geneticSelection()


		return sorted(self.population, key=lambda individual: individual.cost)


if (__name__ == "__main__"):
	printer = PrinterModel.PrinterModel()
	

	targetParameters = 	[
							-86.6,  86,   0,		#lower x
							-50,   -50, 100,		#lower y

							-86.6,  86,   0,	    #upper x
							-50,   -50, 100,		#upper y
						]
	'''
	populationSize = [100, 1000]#, 10000]
	numKillRatio = [10, 3, 2]  # = [10, 30, 50, 100, 300, 500, 1000, 3000, 5000]
	mutationChance = [0.3, 0.5, 0.8]
	mutationScale = [0.5,1,2]
	numIterations = [10]#[100, 1000]#, 10000]
	crossoverType = [1, 2]
	'''
	populationSize = [100]
	numKillRatio = [2]  # = [10, 30, 50, 100, 300, 500, 1000, 3000, 5000]
	mutationChance = [0.1]
	mutationScale = [0.5]
	numIterations = [10000]#, 10000]
	crossoverType = [1]
	'''	
	ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	f = open("logs/log_" +str(ts)+ "_.txt", "w")


	f.write("populationSize, numKillRatio, mutationChance, mutationScale, numIterations, crossoverType, realCost1, realCost2, realCost3, averageCost, runTime\n")

	for p in populationSize:
		for nKR in numKillRatio:
			for mC in mutationChance:
				for mS in mutationScale:
					for nI in numIterations:
						for cT in crossoverType:
							start = time.clock()
							f.write(str(p) +", "+ str(nKR) +", "+ str(mC) +", "+ str(mS) +", "+ str(nI) +", "+ str(cT) + ", ")
							print (str(p) +", "+ str(nKR) +", "+ str(mC) +", "+ str(mS) +", "+ str(nI) +", "+ str(cT) + ", "),
							averageCost = 0
							for i in range(1):
								ga = GeneticOptimization(p, (p/nKR), mC, mS, nI, cT)
								realCost = 0
								population = ga.run(targetParameters)
								parameters = population[0].getParameters()
								for i in range(len(parameters)):
									realCost+=(parameters[i] - targetParameters[i])**2
								realCost = math.sqrt(realCost)
								averageCost+= realCost
								f.write(str(realCost) + ", ")
								print (str(realCost) + ", "),
								print ("fakeCost: " + str(population[0].getCost()) + ", ")
							averageCost = averageCost/3
							f.write(str(averageCost) + ", ")
							print (str(averageCost) + ", "),
							end = time.clock()
							f.write(str((end-start)/3)+"\n")
							print (str((end-start)/3)+"\n"),
	f.close()
	'''
	ga = GeneticOptimization(100, 2, 0.1, 0.5, 1000, 1)
	ga.run(targetParameters)	

