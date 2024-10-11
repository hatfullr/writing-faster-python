# writing-faster-python
 This repository contains resources used in the workshop "Writing Faster Python" for the GPSA 15th Annual Symposium for Graduate Physics Research at the University of Alberta on October 11th, 2024.

# Helpful Links
   - [Presentation slides](https://docs.google.com/presentation/d/1gpqly7idl1oXKRlYrjA9b4HAhZeGL0X1HxyYaBq1Iwc/edit?usp=sharing)
   - [line_profiler](https://github.com/pyutils/line_profiler)
      - A module for measuring the performance of each line in your code. Add the function decorator `@profile` to the start of any method and then at the command line, do `kernprof -l myscript.py; python3 -m line_profiler myscript.py.lprof`. See `scripts/examples/line_profiler_example.py`.
