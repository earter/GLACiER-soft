

f = open("hab_test1.txt")
ff = [line for line in f]

def add_dots(frame):        #TODO oneliner
    frame = frame.rstrip()
    for i in range(250-len(frame)):
        frame += "."
    frame = frame + "\n"
    return frame

for line in ff:
    line = add_dots(line)
    print(line)

