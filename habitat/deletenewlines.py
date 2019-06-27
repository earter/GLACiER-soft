#!/usr/bin/env python

# removes blank lines in a file and creates new one

filename = "gnss_eva_1a"

f = open(f"test_data/{filename}.txt", "r")
lines = f.readlines()
f.close()

lines = filter(lambda x: not x.isspace(), lines)
f = open(f"test_data/{filename}_noempytlines.txt", "w+")
f.write("".join(lines))
f.close()
