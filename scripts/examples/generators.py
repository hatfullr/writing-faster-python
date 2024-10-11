r"""
Generators execute tasks on-the-fly. A generator is any function with a "yield"
statement in it. Use "yield from" to consume a different generator in-place.
"""
import os

def simple_generator():
    yield 1
    yield 2
    yield 3

def yieldfrom():
    yield 0 # 0
    yield from simple_generator() # 1, 2, 3

# Generators are extremely useful when writing recursive functions. Consider the
# following function which locates all files in all subdirectories of the given
# directory path.
def find_files(directory):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path): yield from find_files(path) 
        else: yield path
        

if __name__ == '__main__':
    # Print "1", "2", and "3"
    for item in simple_generator():
        print(item)

    input("Press enter to continue")
    
    print(list(simple_generator())) # [1, 2, 3]
    
    input("Press enter to continue")

    # Print "0", "1", "2", "3"
    for item in yieldfrom():
        print(item)

    input("Press enter to continue")

    # Print out all the files in this GitHub repository
    for f in find_files('../../'):
        print(f)

