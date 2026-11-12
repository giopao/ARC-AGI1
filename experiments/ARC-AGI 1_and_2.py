#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:55:39 2026

@author: giopao
"""
with open('training1.txt', 'r', encoding='utf-8') as f1:
    # .read().splitlines() deletes new lines (\n)
    puzzles1 = f1.read().splitlines()  
    set1 = set(puzzles1)
    
with open('training2.txt', 'r', encoding='utf-8') as f2:
    puzzles2 = f2.read().splitlines()
    set2 = set(puzzles2)

intersection = set1.intersection(set2)
exclusive_puzzles = set1 - set2

print(f"Unique codes in ARC-AGI 1: {len(puzzles1)}")
print(f"Unique codes in ARC-AGI 2: {len(puzzles2)}")
print(f"Codes in both: {len(intersection)}")
print("Puzzles of ARC-AGI 1 that are not included in ARC-AGI 2:")
for puzzle in exclusive_puzzles:
    print(puzzle)

