import multiprocessing, time

def func(): time.sleep(1)

if __name__ == '__main__': # Only if we are the main process
    # Create a child process
    process = multiprocessing.Process(
        target = func,
        daemon = True, # Terminate child when main exits
    )
    process.start()
    start_time = time.time() # Starting timestamp
    process.join() # Wait until child finishes
    end_time = time.time() # Stopping timestamp
    print(end_time - start_time) # Expect: 1 (s)
