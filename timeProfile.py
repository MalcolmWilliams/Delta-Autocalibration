#tthuis usime profile
import GeneticOptimization
import cProfile

gOpt = GeneticOptimization.GeneticOptimization()
cProfile.run('gOpt.run()')
