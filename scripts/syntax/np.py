import numpy as np
import timeit

directories = []

a = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


def prealloc():
    b = np.empty(a.shape)
    for i, ai in enumerate(a):
        b[i] = ai
def npappend():
    b = np.array([])
    for ai in a:
        b = np.append(b, ai)

def npcopy(): np.copy(a)
def copy(): a.copy()

directories += [{
    'for i, ai in enumerate(a): b = np.append(b, ai)' : npappend,
    'for i, ai in enumerate(a): b[i] = ai' : prealloc,
    'np.copy(a)' : npcopy,
    'a.copy()' : copy,
}]




def sum1():
    b = 0
    for i, ai in enumerate(a):
        b += ai
def sum2(): np.sum(a)
def sum3(): a.sum()
def sum4(): sum(a)

directories += [{
    'for i, ai in enumerate(a): b += ai' : sum1,
    'np.sum(a)' : sum2,
    'a.sum()' : sum3,
    'sum(a)' : sum4,
}]


def pow1(): a**2
def pow2(): np.power(a, 2)
def pow3(): pow(a, 2)
def pow4(): a*a


directories += [{
    'a**2' : pow1,
    'np.power(a, 2)' : pow2,
    'pow(a, 2)' : pow3,
    'a*a' : pow4,
}]












for j, directory in enumerate(directories):
    # Get the timing results
    results = {key : timeit.timeit(
        val.__name__ + '()',
        globals = globals(),
        number = 100000 if j == 0 else 1000000, # np.append takes so long...
    ) for key, val in directory.items()}

    # Sort the results from slowest-to-fastest
    order = {k : v for k,v in sorted(
        results.items(),
        key = lambda item:item[1],
        reverse = True,
    )}

    # Print the results
    for i, (key, result) in enumerate(order.items()):
        print('{i:2d}) {result:>10f} seconds   "{key:s}"'.format(
            i = i,
            key = key,
            result = result,
        ))
    print()

