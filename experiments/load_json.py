import json
import numpy as np

# example of json file from training
with open('0a938d79.json', 'r', encoding='utf-8') as file:
    grids = json.load(file)

# grids is a dict 
# print(f"type of grids: {type(grids)}")

# with keys 'train' and 'test'
# print(f"keys of grids: {grids.keys()}")

# and with list as values
# print(f"type of grids['train']: {type(grids['train'])}")

number_of_input_grids = len(grids['train'])
cal_I: list[np.ndarray] = []
cal_S: list[np.ndarray] = []

for k in range(number_of_input_grids - 1):

    # grids['train'][k] is a dict with keys 'input' and 'output'
    
    # grids['train'][k]['input'] is the k-th input grid: \mathcal{I}_k
    cal_I.append(np.array(grids['train'][k]['input']))
    
    # grids['train'][k]['output'] is the k-th output grid: \mathcal{S}_k
    cal_S.append(np.array(grids['train'][k]['output']))

# We can also have more than 1 test to solve (and we must solve all of them)
number_of_tests = len(grids['test']) 

for k in range(number_of_input_grids - 1, number_of_input_grids + number_of_tests - 1):
    cal_I.append(np.array(grids['test'][k - number_of_input_grids + 1]['input']))
    
    # in the correspondin 'output' there is the solution
    cal_S.append(np.array(grids['test'][k - number_of_input_grids + 1]['output']))
    

with open('grid_test.json', 'r', encoding='utf-8') as file:
    test_from_interface = json.load(file)
    test_grid = np.array(test_from_interface['grid'])

