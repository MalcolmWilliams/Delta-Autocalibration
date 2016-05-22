#time profile
import main
import cProfile

ga = main.GeneticOptimization()
cProfile.run('ga.run()')