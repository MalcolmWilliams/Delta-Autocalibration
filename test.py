#for running quick tests
import random

var = [0,1,2,3,4,5]
maxLen = 0

for i in range(100):
	rand =  random.randint(0, len(var))
	if rand > maxLen:
		maxLen = rand
print maxLen