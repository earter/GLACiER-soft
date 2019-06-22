



with open('test_data/gnss_ard_raw_ouput.txt','rw') as file:
    for line in file:
        if not line.isspace():
            file.write(line)

"""
with open("test_data/gnss_ard_raw_ouput.txt") as f:
    for line in f:
        if line.rstrip():
            print(line)
    f.close()


with open("test_data/gnss_ard_ouput_fixed.txt", 'w') as ff:
    for item in lines:
        ff.write(f"{item}")
    ff.close()
    

import fileinput
for line in fileinput.FileInput("test_data/gnss_ard_raw_ouput.txt",inplace=1):
    print(line)
    if line.rstrip():
        print(line)    
    
"""
