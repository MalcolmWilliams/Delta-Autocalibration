#tthuis usime profile
import GeneticOptimization
import cProfile

targetParameters = 	[
						-86.6,  86,   0,		#lower x
						-50,   -50, 100,		#lower y

						-86.6,  86,   0,	    #upper x
						-50,   -50, 100,		#upper y
					]

gOpt = GeneticOptimization.GeneticOptimization(100, 30, 0.5, 1, 100, 1)
cProfile.run('gOpt.run(targetParameters)')
