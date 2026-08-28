Open the file "verification_interface.html" with Chrome to have a GUI taken from ARC-AGI 1.
Using this GUI, one can create any test grid to verify e.g. some core-knowledge code (e.g. one can draw any incomplete rectangle in any position).

The interface has two new functions:
1. You can use the key Ctrl (Cmd in Mac) to select multiple cells.
2. You can save the final grid in the file 'grid_test.json'.

The test grid can be loaded in Python with:

with open('grid_test.json', 'r', encoding='utf-8') as file:
    test_from_interface = json.load(file)
    test_grid = np.array(test_from_interface['grid'])

