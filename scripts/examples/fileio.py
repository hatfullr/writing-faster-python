r"""
In this file, we simulate a long-running calculation that is applied to each 
line of a file containing random data. When you execute this script, it will
create a file called "data.txt". Then it will read that file and run the
calculations in serial and report a time. Then it will do the same process but
in parallel.
"""
import multiprocessing, queue, time, os, traceback, contextlib
import numpy as np

@contextlib.contextmanager
def timer(name): # A simple performance timer
    start = time.perf_counter()
    yield None
    print(name, "took", time.perf_counter() - start, "seconds")

def create_file(path): # Make a file filled with random data.
    with open(path, 'w') as f:
        for row in np.random.rand(1000, 3):
            f.write(('%22.14E'*len(row) + '\n') % tuple(row))
def read(path):
    # Read the file located at path. This is called a "generator".
    # Use it in a loop to iteratively read the file:
    # for line in read(path):
    #     print(line)
    with open(path, 'r') as f:
        for line in f:
            yield np.asarray(line.split(), dtype = object).astype(float)


def calculation(data_row): # some long calculation
    time.sleep(1.e-3)
    return 0

def func(input_queue, output_queue, error_queue):
    try:
        while True:
            if input_queue.empty(): continue
            try: inputs = input_queue.get()
            except Exception as e:
                if isinstance(e, queue.Empty): break
                else: raise e
            if inputs is None: break
            output_queue.put(calculation(inputs))
        output_queue.put(None)
    except:
        error_queue.put(traceback.format_exc())

def process_errors(processes, error_queue): # Check if a process raised error
    if error_queue.empty(): return
    print(error_queue.get())
    for process in processes: process.terminate()
    quit(1)



# Main program
if __name__ == '__main__':
    filename = 'data.txt'
    create_file(filename)


    
    # ------------- SERIAL -------------
    with timer('serial'):
        for line in read(filename): calculation(line)
    # ----------------------------------


    
    # ------------ PARALLEL ------------
    manager = multiprocessing.Manager() # Provides cleaner error handling
    input_queue = manager.Queue()
    output_queue = manager.Queue()
    error_queue = manager.Queue()

    # Create a process for each CPU
    processes = [multiprocessing.Process(
        target = func,
        args = (input_queue, output_queue, error_queue),
        daemon = True,
    ) for _ in range(multiprocessing.cpu_count())]

    try: # Catch exceptions so we can terminate processes for safe exit
        for process in processes: process.start()
        
        with timer('parallel'):
            # Fill the input queue
            for line in read(filename): input_queue.put(line)
            for _ in processes: input_queue.put(None) # end-of-queue signal

            # Get the results from the output queue
            ndone = 0
            while ndone < len(processes):
                process_errors(processes, error_queue) # Check for errors
                if output_queue.empty(): continue
                if output_queue.get() is None: ndone += 1
    
    except: # Catch exceptions for safe exit
        print('Terminating processes. Please wait.')
        for process in processes: process.terminate()
        print('Processes terminated')
        raise
    # ----------------------------------
