#!/usr/bin/python3 -W ignore

from matplotlib import pyplot as plt 
import numpy as np
import random
from scipy.interpolate import interp1d

n_iter = 3000
n_graph = 2000
n_smooth = 20

"""
useful functions :
"""

# generator for a random polynomial distribution
def poly(lst, x):
	if len(lst) == 1:
		return lst[0]
	else:
		return poly(lst[1:], x)*x + lst[0]

# linear smoothing for plotting
def smooth(y):
	smoothed_y = np.zeros(len(y))

	for i in range(len(y)):
		begin = max(0, i - n_smooth//2)
		end = min(len(y), i + n_smooth//2)

		smoothed_y[i] = np.mean(y[begin:end])

	return smoothed_y

# generating an occurence list from a selecting method and a random distribution (List)
def generate(selector, List, n_select):
	occurence = np.zeros(random_list.shape)

	for i in range(n_iter):
		occurence[selector(List, n_select)] += 1

	# normalizeing occurences so they idely match the distribution
	return occurence / n_iter / n_select



"""
tested method of selection :
"""

def selector_1(List, n):
	random_selector = np.random.rand(len(List))
	random_selector = random_selector / List #-np.log(random_selector) / List

	idx = np.argpartition(random_selector, n)
	return idx[:n]



"""
generating the random distribution :
"""

# starting with an empty list
random_list = np.ndarray([])

# adding uniform distributions
for rate in [1, 1.5, 3]:
	distribution = np.random.rand(n_graph) * rate
	distribution.sort()
	random_list = np.append(random_list, distribution)

# adding exponential distribution
for rate in [1, 2, 4]:
	distribution = -np.log((np.random.rand(n_graph)*(1 - 0.05) + 0.05)) / rate
	distribution.sort()
	random_list = np.append(random_list, distribution)

# adding an inverse polynomial distribution
coefs = np.concatenate(( np.zeros(1), np.random.rand(4)), 0)
distribution = poly(coefs, np.random.rand(3*n_graph))
distribution.sort()
random_list = np.append(random_list, distribution)

# normalizeing the distribution
random_list /= np.sum(random_list)



"""
plotting the distribution and occurences for different proportions of graph selected :
"""

fig = plt.figure(figsize=(12, 5), constrained_layout=True)
plt.rc('axes', labelsize=18)
plt.rc('xtick', labelsize=18)
plt.rc('figure', titlesize=20) 
plt.rc('legend', fontsize=14)
ax = fig.add_subplot(1, 1, 1)



# plotting occurences for different proportions of graph selected
for proportion in [.2]:
	n_select = int(len(random_list) * proportion)
	ax.plot(smooth(generate(selector_1, random_list, n_select)), label=f"normalized occurences\n using probabilistic ranking\n for { proportion * 100 }% of objects selection", linewidth=5)
	#ax1.plot(smooth(generate(selector_2, random_list)), label="histograms")



# plotting the initial ditribution
ax.plot(random_list, "r--", label="objects probability distribution", linewidth=3)



# adding separators for the different distributions
ax.set_ylim(ax.get_ylim())
ax.plot([3*n_graph, 3*n_graph], [-1, 1], "k--", linewidth=4)
ax.plot([6*n_graph, 6*n_graph], [-1, 1], "k--", linewidth=4)



# adding legend
legend = fig.legend(bbox_to_anchor=(0.99, 0.90), loc='upper right', borderaxespad=0)
legend.get_frame().set_alpha(None)
legend.get_frame().set_facecolor((1, 1, 1, 1)) # R G B transparency



# setting up the frame
ax.set_ylabel("Probability/occurences")
ax.set_yticks([])

_, x_max = ax.get_xlim()
ax.set_xticks([3*n_graph/2, (3*n_graph + 6*n_graph)/2, (6*n_graph + x_max)/2], ["linear distributions", "exponential distributions", "inverse polynomial distribution"])

# adding text to name different sections
"""y_max = ax.get_ylim()[1]
args = {
	"horizontalalignment" : 'center',
	"verticalalignment" : 'center',
	"bbox" : {
		"facecolor" : 'white',
		"alpha" : 1,
	}
}
ax.text(1.5*n_graph, y_max*.75, "linear distributions", **args)
ax.text(4.5*n_graph, y_max*.75, "exponential distributions", **args)
ax.text(7.5*n_graph, y_max*.75, "inverse polynomial distribution", **args)"""



# saving the figure
fig.suptitle(f'random distribution and corresponding occurences')
fig.savefig("../../plots/validation/repartition.jpg")