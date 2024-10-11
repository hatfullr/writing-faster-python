a = [False, True, False]
b = a
print(a)
b[1] = False
print(a)

import copy
a = [False, True, False]
b = copy.deepcopy(a)
print(a)
b[1] = False
print(a)
