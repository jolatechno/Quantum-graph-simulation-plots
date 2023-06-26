#!/usr/bin/python3 -W ignore

import json
import matplotlib.pyplot as plt
import numpy as np
import sys

output_base = "../plots/"
output_filename = "weak_scaling.png"

filename = sys.argv[1]
if len(sys.argv) > 2:
	output_filename = sys.argv[2]

color_ideal          = "red"
color_scaling        = "C0"
color_scaling_t      = "C1"
color_exec_time      = "C2"
color_scaling_symb   = "C4"
color_scaling_symb_t = "C6"

rule = ""
json_dict, num_core = {}, []
min_num_core, max_num_core = np.inf, -np.inf
with open(filename, "r") as file:
	json_file = file.read()
	json_dict = json.loads(json_file)

	rule = " ".join(json_dict["command"]["rule"].split("_"))

	for n_threads, n_jobs, n_nodes in zip(json_dict["num_threads"], json_dict["num_jobs"], json_dict["num_nodes"]):
		num_core.append(n_threads*n_jobs*n_nodes)

		min_num_core = min(min_num_core, num_core[-1])
		max_num_core = max(max_num_core, num_core[-1])

scaling, scaling_t, scaling_symbolic, scaling_symbolic_t = [], [], [], []
exec_times = []
ref_time, ref_num_objects, ref_num_symbolic = json_dict["exec_time"][0], json_dict["total_num_objects"][0], json_dict["total_num_symbolic"][0]
scaling_multiplier = float(num_core[0])/float(min_num_core)

for exec_time, num_object, num_symbolic in zip(json_dict["exec_time"], json_dict["total_num_objects"], json_dict["total_num_symbolic"]):
	exec_times.append(exec_time)

	scaling.append(num_object/ref_num_objects*scaling_multiplier)
	scaling_t.append((num_object/exec_time)/(ref_num_objects/ref_time)*scaling_multiplier)

	scaling_symbolic.append(num_symbolic/ref_num_symbolic*scaling_multiplier)
	scaling_symbolic_t.append((num_symbolic/exec_time)/(ref_num_symbolic/ref_time)*scaling_multiplier)


fig, ax1 = plt.subplots(layout='constrained', figsize=(5, 5))

ax1.set_title(f"Weak scaling results for \"{ rule }\"")
ax1.set_xlabel("Number of cores")
ax1.set_ylabel("Scaling")

ax2 = ax1.twinx()
ax2.set_ylabel("Execution time")


x = np.linspace(min_num_core, max_num_core, 10, endpoint=True)
y = np.linspace(1, max_num_core/min_num_core, 10, endpoint=True)

ax2.set_ylim([0, 1.2*np.max(exec_times)])
ax2.plot(num_core, exec_times, c=color_exec_time, linestyle="solid", label="Execution time")

ax1.plot(x, y, c=color_ideal, linestyle="dotted", label="Ideal scaling")

ax1.plot(num_core, scaling, c=color_scaling, linestyle="dashed", label="Number of objects scaling")
ax1.plot(num_core, scaling_t, c=color_scaling_t, linestyle="dashed", label="Number of objects per second scaling")

ax1.plot(num_core, scaling_symbolic, c=color_scaling_symb, linestyle="dashed", label="Number of symbolic objects scaling")
ax1.plot(num_core, scaling_symbolic_t, c=color_scaling_symb_t, linestyle="dashed", label="Number of symbolic objects per second scaling")


fig.legend(fontsize="5", bbox_to_anchor=(0.23, 0.85, 0.29, 0.1))
fig.savefig(output_base + output_filename, dpi=200)