import sys
from cache_implementation import run

def inp_arg():

    param = sys.argv
    BLOCKSIZE = int(param[1])
    L1_SIZE = int(param[2])
    L1_ASSOC = int(param[3])
    L2_SIZE = int(param[4])
    L2_ASSOC = int(param[5])
    REPLACEMENT_POLICY = int(param[6])
    INCLUSION_PROPERTY = int(param[7])
    trace_file = param[8]

    return BLOCKSIZE, L1_SIZE, L1_ASSOC, L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file

def read_file(file):
    with open(file) as file_open:
        lines = file_open.readlines()
    return lines

if __name__ == '__main__':
    plot = 0
    BLOCKSIZE, L1_SIZE, L1_ASSOC, L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file = inp_arg()
    lines = read_file(trace_file)
    run(lines, BLOCKSIZE, L1_SIZE, L1_ASSOC, L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file, plot)