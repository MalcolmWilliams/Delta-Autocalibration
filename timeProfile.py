#tthuis usime profile
import GeneticOptimization
import cProfile

gOpt = GeneticOptimization.GeneticOptimization(100, 30, 0.5, 1, 100, 1)
cProfile.run('gOpt.run()')
