#!/usr/bin/python3 -W ignore

import json
import matplotlib.pyplot as plt
import numpy as np
import sys

filename = sys.argv[1]

color_num_object   = "C0"
color_num_symbolic = "C1"
color_accuracy     = "C2"

rule = ""
json_dict, num_core = {}, []
with open(filename, "r") as file:
	json_file = file.read()
	json_dict = json.loads(json_file)

	rule = " ".join(json_dict["command"]["rule"].split("_"))

	for n_threads, n_jobs, n_nodes in zip(json_dict["num_threads"], json_dict["num_jobs"], json_dict["num_nodes"]):
		num_core.append(n_threads*n_jobs*n_nodes)


fig, ax1 = plt.subplots(layout='constrained', figsize=(5, 5))

ax1.set_title(f"Accuracy scaling for \"{ rule }\"")
ax1.set_xlabel("Number of cores")
ax1.set_ylabel("Accuracy")

ax2 = ax1.twinx()
ax2.set_ylabel("Number of objects")

ax2.set_ylim([0, 1.2*np.max(json_dict["total_num_symbolic"])])
ax2.plot(num_core, json_dict["total_num_objects"], c=color_num_object, linestyle="dashed", label="Number of objects")
ax2.plot(num_core, json_dict["total_num_symbolic"], c=color_num_symbolic, linestyle="dashed", label="Number of symbolic objects")

ax1.set_ylim([np.min(json_dict["accuracy"]) - 0.1, np.max(json_dict["accuracy"]) + 0.1])
ax1.plot(num_core, json_dict["accuracy"], c=color_accuracy, linestyle="solid", label="Accuracy")

fig.legend(fontsize="7", bbox_to_anchor=(0.23, 0.8, 0.29, 0.1))
fig.savefig("../plots/accuracy.png", dpi=200)