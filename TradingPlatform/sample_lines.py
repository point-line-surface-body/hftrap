import sys

if (len(sys.argv) < 2):
    print 'USAGE: EXEC FILE 1/PROB'
    print 'If 1/PROB = 2, sampling percentage will be 0.5'
    exit(0)
    
in_file = open(sys.argv[1], 'r')
lines = in_file.readlines()
in_file.close()

prob = float(sys.argv[2])

print lines[0][:-1]

count = 0
for line in lines[1:]:
    count += 1
    if (count%prob == 0):
        print line[:-1]