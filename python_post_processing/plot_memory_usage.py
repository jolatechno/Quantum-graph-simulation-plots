#!/usr/bin/python3 -W ignore

import json
import matplotlib.pyplot as plt
import numpy as np
import sys

output_base = "../plots/"
output_filename = "memory_usage.png"

filename = sys.argv[1]
if len(sys.argv) > 2:
	output_filename = sys.argv[2]

color_min_mem  = "C0"
color_avg_mem  = "C1"
color_max_mem  = "C2"
color_accuracy = "C3"

rule = ""
json_dict = {}
with open(filename, "r") as file:
	json_file = file.read()
	json_dict = json.loads(json_file)

	rule = " ".join(json_dict["command"]["rule"].split("_"))


fig, ax = plt.subplots(layout='constrained', figsize=(5, 5))

ax.set_title("Memory usage evolution")
ax.set_xlabel("iteration")
ax.set_ylabel("Memory usage/Accuracy")
ax.set_yscale("log")
ax.grid(axis='y', which="both")

ax.plot(json_dict["accuracy_evolution"][0], c=color_accuracy, linewidth=1.5, linestyle="dashed", label="Accuracy")

ax.plot(json_dict["min_memory_usage"][0], c=color_min_mem, linewidth=0.8, linestyle="solid", label="Min memory usage")
ax.plot(json_dict["avg_memory_usage"][0], c=color_avg_mem, linewidth=1.5, linestyle="solid", label="Avg memory usage")
ax.plot(json_dict["max_memory_usage"][0], c=color_max_mem, linewidth=0.8, linestyle="solid", label="Max memory usage")

fig.legend(fontsize="7", bbox_to_anchor=(0.7, 0.14, 0.29, 0.1))
fig.savefig(output_base + output_filename, dpi=200)