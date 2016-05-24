#test of new population control algoritm

class Individual:


	parent1 = None
	parent2 = None
	name = None


	def __init__ (self, p1, p2, n):
		self.parent2 = p2
		self.parent1 = p1
		self.name = n

	def getName(self):
		return self.name

	def getParents(self):
		return self.parent1, self.parent2

	def setParents(self, p1, p2):
		self.parent1 = p1
		self.parent2 = p2

population = []
for i in range(100):
	indiv = Individual(i,i,i)
	population.append(indiv)


numKill = 50
iteration = 0
childrenToMake = numKill 	#we want the population to remain at a constant size

population = population[0:len(population)-numKill]	#remove the ones we want to destroy

while not(childrenToMake == 1):	#keeps iterating until there is only one child to make
	numChild = childrenToMake/2
	childrenToMake -= numChild
	#for i in range()
	for i in range(numChild):

		population.append(Individual(i, iteration, 11))

	iteration += 1
population.append(Individual(0,1,11))
	#print numChild


for p in population:
	print p.getParents()


print len (population)