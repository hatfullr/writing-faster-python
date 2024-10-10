"""
A sum computed in parallel is called a "reduce" operation. Suppose we want to
do a reduction of a list [0, 1, 2, 3, ..., n], with n = 1e9. Modify this code to
try your own solution.
"""
if __name__ == '__main__':
    # -------------- DO NOT EDIT ----------------
    result = None # Fill this using your code
    
    try: del contextlib
    except NameError: pass
    import contextlib
    @contextlib.contextmanager
    def timer():
        global result
        try: del time # No cheating :)
        except NameError: pass
        import time
        start = time.perf_counter()
        yield None
        print("That took", time.perf_counter() - start, "seconds")
        if result != 1999999999000000000:
            print("\033[0;31mIncorrect result\033[0m: %s. Try again!" % str(result))
        else: print("\033[0;32mCorrect result!\033[0m")
        quit()
    with timer():
        pass
    # -------------------------------------------
        # Write your code below:
        
        
        

    
