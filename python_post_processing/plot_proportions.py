#!/usr/bin/python3 -W ignore

import json
import matplotlib.pyplot as plt
import numpy as np
import sys

files = sys.argv[1:]

ordered_keys = ["pre-symbolic-iteration", "symbolic-iteration", "collisions", "pre-object-generation", "object-generation", "communication"]

colors = ["C" + str(i) for i in range(len(ordered_keys))]

rule = ""
num_core, proportions = [], {
	key : [] for key in ordered_keys
}
min_proportion = np.inf
for filename in files:
	with open(filename, "r") as file:
		json_file = file.read()
		json_dict = json.loads(json_file)

		rule = " ".join(json_dict["command"]["rule"].split("_"))

		num_core.append([])
		for key in ordered_keys:
			proportions[key].append(json_dict["proportions"][key])
			min_proportion = min(min_proportion, np.min(proportions[key][-1]))

		for n_threads, n_jobs, n_nodes in zip(json_dict["num_threads"], json_dict["num_jobs"], json_dict["num_nodes"]):
			num_core[-1].append(n_threads*n_jobs*n_nodes)


fig, ax = plt.subplots(layout='constrained', figsize=(5, 5))

ax.set_title(f"Step execution time proportion for \"{ rule }\"")
ax.set_xlabel("Number of cores")
ax.set_ylabel("Execution time proportion")
ax.set_yscale("log")
ax.grid(axis='y', which="both")
ax.set_ylim([min_proportion/1.2, 3])


for key, color in zip(ordered_keys, colors):
	ax.plot(num_core[0], proportions[key][0], c=color, linestyle="solid", label=key + " proportion")
	for num_core_, scaling_ in zip(num_core[1:], proportions[key][1:]):
		ax.plot(num_core_, scaling_, c=color, linestyle="solid", label="_nolabel_")


fig.legend(fontsize="6", bbox_to_anchor=(0.7, 0.85, 0.29, 0.1))
fig.savefig("../plots/proportions.png", dpi=200)