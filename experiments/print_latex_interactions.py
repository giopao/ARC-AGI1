#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 13:35:35 2026

@author: giopao

Example of LaTeX representation of an interaction

Improvements:
    - use classes Interaction and InteractingEntity
    - generalize for an arbitrary number of agents (arity)
    - find a more clear way to write the code in the latex_formula below
"""

import matplotlib.pyplot as plt

# Force Matplotlib to use your system's actual LaTeX installation
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}"  # Load extra math packages if needed
})

# Substitute the following lines with the use of the attributes
i_id = "buy at"
a_1_id = "Client"
a_2_id = "Shop"
pr_id = "purchased items, receipt"
pa_id = "Client"

# find a way to write it in a more clear way
latex_formula = f"$\\texttt{{{i_id}}}: \\texttt{{{a_1_id}}}, \\texttt{{{a_2_id}}}\\xrightarrow{{\\texttt{{{pr_id}}}}}\\texttt{{{pa_id}}}$"

print(latex_formula)

# use of plt to compile with LaTeX the formula and save it
fig, ax = plt.subplots(figsize=(6, 2))
ax.axis("off")  # Hide the graph border and axis ticks

# 4. Render the LaTeX text onto the figure canvas
ax.text(
    0.5, 0.5,              # Coordinates (center of the image)
    latex_formula, 
    size=24,               # Font size of the rendered formula
    va="center",           # Vertical alignment
    ha="center"            # Horizontal alignment
)

# 5. Save the output as a cropped image file
plt.savefig(
    "interaction_" + f"{i_id}" + ".png", 
    dpi=300,               # High resolution quality
    bbox_inches="tight",   # Automatically crop whitespace around the formula
    transparent=True       # Transparent background
)
plt.close()