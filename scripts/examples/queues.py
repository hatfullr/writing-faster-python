import multiprocessing

def func(queue):
    while True: # keep going until no more tasks
        i = queue.get()
        if i is None: # end-of-queue signal
            return
        print(i)

if __name__ == '__main__':
    nprocs = 4
    queue = multiprocessing.Queue()
    
    # Put values in the queue
    for i in range(nprocs*2): queue.put(i)
    # Append end-of-queue signals
    for _ in range(nprocs): queue.put(None) 
    
    # Create nprocs processes
    processes = [multiprocessing.Process(
        target = func,
        args = [queue],
        daemon = True,
    ) for _ in range(nprocs)]
    
    # Start processes
    for process in processes: process.start()
    # Wait for processes to finish
    for process in processes: process.join()

    
