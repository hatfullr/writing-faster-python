
for i in range(3):
    if i == 0:
        print("Hello")
    else:
        if i == 1:
            print("What's up?")
        else:
            print("Not much")

input("Press enter to continue")

for i in range(3):
    if i == 0:
        print("Hello")
        continue
    if i == 1:
        print("What's up?")
        continue
    print("Not much")
