# Remember: YOU ARE THE USER. If you ever plan to use your own code again in the
# future, you owe it to yourself to make your code useable and understandable in
# the future.

# Annotate method parameters:
def useless( # descriptive method name here!
        param1 : float,
        param2 : int,
        param3 : type(None) | str = None,
):
    """
    Describe the function. Doc strings can be used later for automatic 
    documentation (see sphinx), and for remembering how to use the function.
    
    Parameters
    ----------
    param1 : float
        Controls the adiabatic expansion of the universe. Use larger values for
        more excitement. Use smaller values if you're a wall licker. Use
        negative values if you're a maniac.
    
    param2 : int
        A flag which indicates what I ate for dinner last night, where 0 is
        Subway, 1 is chow mein, and 2 is curry. Values above 2 are never used.
    
    Other Parameters
    ----------------
    param3 : None, str, default = None
        If not None, then represents a love letter that will be sent to That 
        Game Company for making Journey, the best game ever.
    
    Returns
    -------
    stuff : float
        The stuff that this function returns.
    """

    # param1 is mostly a joke
    if param1 < 0: print('What have you done...?')

    dinner = None
    if param2 == 0: dinner = 'Subway'
    elif param2 == 1: dinner = 'chow mein'
    elif param2 == 2: dinner = 'curry'
    else: raise NotImplementedError('Unrecognized value for param2: %d' % param2)
    
    if param3 is not None: # Only if something to send
        print("I hope this arrives at That Game Company HQ...:\n" + param3)

    # Returning junk value because this function is a joke
    stuff = 1.
    return stuff

print('This script does nothing. Open the file instead of executing it.')
