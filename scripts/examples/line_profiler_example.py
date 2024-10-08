@profile
def func(): # Some long operation
    for i in range(int(1e6)):
        i**2

func()

"""
$ kernprof -l line_profiler_example.py
Wrote profile results to line_profiler_example.py.lprof
$ python3 -m line_profiler line_profiler_example.py.lprof 
Timer unit: 1e-06 s

Total time: 0.912989 s
File: line_profiler_example.py
Function: func at line 1

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     1                                           @profile
     2                                           def func(): # Some long operation
     3   1000001     330973.0      0.3     36.3      for i in range(int(1e6)):
     4   1000000     582016.0      0.6     63.7          i**2

"""
