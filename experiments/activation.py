#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:29:06 2026

@author: giopao
"""

class InteractingEntity:
    
    def __init__(self):
        self.ac = {}


e = InteractingEntity()

e.ac[1.5] = 0
print(e.ac[1.5])

e.ac[1.5] = 0.5
print(e.ac[1.5])

e.ac[2] = 0.7
print(e.ac[2])