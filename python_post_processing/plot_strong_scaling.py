#!/usr/bin/python3 -W ignore

import json
import matplotlib.pyplot as plt
import numpy as np
import sys

files = sys.argv[1:]

color_ideal = "red"
color_data  = "C0"

rule = ""
datas, num_core = [], []
min_num_core, max_num_core = np.inf, -np.inf
for filename in files:
	with open(filename, "r") as file:
		json_file = file.read()
		json_dict = json.loads(json_file)

		rule = " ".join(json_dict["command"]["rule"].split("_"))

		datas.append(json_dict)

		num_core.append([])
		for n_threads, n_jobs, n_nodes in zip(json_dict["num_threads"], json_dict["num_jobs"], json_dict["num_nodes"]):
			num_core[-1].append(n_threads*n_jobs*n_nodes)

			min_num_core = min(min_num_core, num_core[-1][-1])
			max_num_core = max(max_num_core, num_core[-1][-1])

scaling = []
for i, data in enumerate(datas):
	ref_time = data["exec_time"][0]
	scaling_multiplier = float(num_core[i][0])/float(min_num_core)

	scaling.append([])
	for exec_time in data["exec_time"]:
		scaling[-1].append(ref_time/exec_time*scaling_multiplier)

rule = " ".join(datas[0]["command"]["rule"].split("_"))

fig, ax = plt.subplots(layout='constrained', figsize=(5, 5))

ax.set_title(f"Strong scaling results for \"{ rule }\"")
ax.set_xlabel("Number of cores")
ax.set_ylabel("Relative execution time scaling")


x = np.linspace(min_num_core, max_num_core, 10, endpoint=True)
y = np.linspace(1, max_num_core/min_num_core, 10, endpoint=True)

plt.plot(x, y, c=color_ideal, linestyle="dashed", label="Ideal scaling")

plt.plot(num_core[0], scaling[0], c=color_data, linestyle="solid", label="Execution time scaling")
plt.plot(num_core[0][0:1], scaling[0][0:1], c=color_data, marker="x", label="Reference point for scaling")
for num_core_, scaling_ in zip(num_core[1:], scaling[1:]):
	plt.plot(num_core_, scaling_, c=color_data, linestyle="solid", label="_nolabel_")
	plt.plot(num_core_[0:1], scaling_[0:1], c=color_data, marker="x", label="_nolabel_")


fig.legend(fontsize="9", bbox_to_anchor=(0.7, 0.15, 0.29, 0.1))
fig.savefig("../plots/strong_scaling.png", dpi=200)