#plot a text file for debugging
import matplotlib.pyplot as plt 

plt.plotfile('test.txt', delimiter=' ', cols=(0, 1), 
             names=('col1', 'col2'), marker='o')
plt.show()
