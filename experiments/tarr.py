#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:09:06 2026

@author: giopao

Example of calculation of i.ta[t]:

i.ta[t] = i.T_a.discrete[j] if i.T_a.discrete[j] <= i.ta[t] < i.T_a.discrete[j+1]
"""

import bisect

def ta(T_a: list[float], t: float) -> float:
    # Handle empty list or list with a single element
    if len(T_a) < 2:
        return T_a[0]
        
    # Find the insertion index using binary search
    idx = bisect.bisect_right(T_a, t)
    
    # Case 1: t is less than the first element
    if idx == 0:
        return float("-inf")
        
    # Case 2: t is greater than or equal to the last element
    if idx == len(T_a):
        return T_a[-1]
        
    # Case 3: t falls exactly between two elements
    return T_a[idx - 1]

# --- USAGE EXAMPLE ---
T_a = [1.2, 3.4, 5.8, 8.1, 10.5]
print(T_a)

print(f"ta({4.5}) = {ta(T_a, 4.5)}")   # Output: 3.4 -> Standard case
print(f"ta({12.0}) = {ta(T_a, 12.0)}")  # Output: 10.5 -> Out of bounds (right)
print(f"ta({5.8}) = {ta(T_a, 5.8)}")   # Output: 5.8 -> Edge case (t equals an element)
print(f"ta({0.5}) = {ta(T_a, 0.5)}: ValueError because {0.5} < {T_a[0]}")   # Output: ValueError -> Out of bounds (left)
