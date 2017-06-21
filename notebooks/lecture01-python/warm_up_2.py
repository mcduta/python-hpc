import sys

years = [1989, 1955, 2011, 1943, 1975]

# save years to file

outputfile = open("years.txt", 'w')

# output total number of years

outputfile.write("{0:2d}\n".format(len(years)))
               
for i in range(len(years)):
    outputfile.write("{0:2d} {1:2d}\n".format(i, years[i]))

outputfile.close()

# Read the file into a new list

inputfile = open("years.txt", "r")

# Read the number of entries (as a string)

line = inputfile.readline()
nyear = int(line)

newyears = []

# Read in the entries (second token on each line)

for i in range(nyear):
    line = inputfile.readline()
    line = line.rstrip()
    tokens = line.split()
    newyears.append(int(tokens[1]))

inputfile.close()

print newyears

