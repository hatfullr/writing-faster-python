import timeit
import sys

a = [False, True, False, True]

# You can check the size of "a" in bytes by uncommenting this line:
#print(sys.getsizeof(a))

def append_loop():
    b = []
    for i in range(len(a)):
        b.append(a[i])
def plusequals_loop():
    b = []
    for i in range(len(a)):
        b += [a[i]]
def prealloc_loop():
    b = [None]*len(a)
    for i in range(len(a)):
        b[i] = a[i]

def plusequals_element_loop():
    b = []
    for ai in a:
        b += [ai]
def append_element_loop():
    b = []
    for ai in a:
        b.append(ai)
def prealloc_element_enumerate():
    b = [None]*len(a)
    for i, ai in enumerate(a):
        b[i] = ai

def plusequals_enumerate():
    b = []
    for i, ai in enumerate(a):
        b += [ai]
def append_enumerate():
    b = []
    for i, ai in enumerate(a):
        b.append(ai)

def comprehension(): [ai for ai in a]
def copy(): a.copy()

directory = {
    'for i in range(len(a)): b += [a[i]]' : plusequals_loop,
    'for i, ai in enumerate(a): b += [ai]' : plusequals_enumerate,
    'for i in range(len(a)): b.append(a[i])' : append_loop,
    'for i, ai in enumerate(a): b.append(ai)' : append_enumerate,
    'for ai in a: b += [ai]' : plusequals_element_loop,
    'for i in range(len(a)): b[i] = a[i]' : prealloc_loop,
    'for i, ai in enumerate(a): b[i] = ai' : prealloc_element_enumerate,
    'for ai in a: b.append(ai)' : append_element_loop,
    'b = [ai for ai in a]' : comprehension,
    'b = a.copy()' : copy,
}

# Get the timing results
results = {key : timeit.timeit(
    val.__name__ + '()',
    globals = globals()
) for key, val in directory.items()}

# Sort the results from slowest-to-fastest
order = {k : v for k,v in sorted(
    results.items(),
    key = lambda item:item[1],
    reverse=True,
)}

# Print the results
for i, (key, result) in enumerate(order.items()):
    print('{i:2d}) {result:>10f} seconds   "{key:s}"'.format(
        i = i,
        key = key,
        result = result,
    ))

