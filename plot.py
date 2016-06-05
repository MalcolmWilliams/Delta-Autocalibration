#plot a text file for debugging
import matplotlib.pyplot as plt 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("fileName", type=str,
                    help="graph the given textfile")
args = parser.parse_args()
plt.plotfile(args.fileName, delimiter=' ', cols=(0, 1), 
             names=('col1', 'col2'), marker=',')
plt.show()
