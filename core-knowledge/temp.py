# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
def input_name (prompt = 'blu', retries = 34, reminder = 'glu'):
    print(f'first arg: {prompt}')
    print(f'second arg: {retries}')
    print(f'third arg: {reminder}')
    return prompt
    
prompt = 'bla'
prompt = input_name(retries = 'Your name?', reminder = 5)
print(prompt)