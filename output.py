from calculations import *

class print_sim:
    def __init__(self, BLOCKSIZE, L1_SIZE, L1_ASSOC, L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file):
        self.BLOCKSIZE=BLOCKSIZE
        self.L1_SIZE=L1_SIZE
        self.L1_ASSOC=L1_ASSOC
        self.L2_SIZE=L2_SIZE
        self.L2_ASSOC = L2_ASSOC
        self.REPLACEMENT_POLICY=REPLACEMENT_POLICY
        self.INCLUSION_PROPERTY=INCLUSION_PROPERTY
        self.trace_file=trace_file

    def out(self):
        print("\n===== Simulator configuration =====")
        print('BLOCKSIZE:             ' + str(self.BLOCKSIZE))
        print('L1_SIZE:               '+str(self.L1_SIZE))
        print('L1_ASSOC:              '+str(self.L1_ASSOC))
        print('L2_SIZE:               '+str(self.L2_SIZE))
        print('L2_ASSOC:              '+str(self.L2_ASSOC))
        if self.REPLACEMENT_POLICY==0:
            print('REPLACEMENT POLICY:    LRU')
        if self.REPLACEMENT_POLICY==1:
            print('REPLACEMENT POLICY:    FIFO')
        if self.REPLACEMENT_POLICY==2:
            print('REPLACEMENT POLICY:    optimal')
        if self.INCLUSION_PROPERTY==1:
            print('INCLUSION PROPERTY:    inclusive')
        else:
            print('INCLUSION PROPERTY:    non-inclusive')
        print('trace_file:            '+str(self.trace_file))

def print_output(L1, L1_parameters, L1_dirty_dict, L2, L2_parameters, L2_dirty_dict, L2_SIZE, L2_ASSOC, inclusive_bit_value):

    print('===== L1 contents =====')
    for i in range(len(L1)):
        if i<=9:
            text="Set     "+str(i)+":      "
        elif i<=99:
            text="Set     "+str(i)+":     "
        else:
            text="Set     "+str(i)+":    "
        for value in L1[i]:
            text += hex(int(value,2))[2:]
            if L1_dirty_dict[i][value]=='D':
                text+=' D  '
            else:
                text+='    '
        print(text)
    if (L2_SIZE!=0 and L2_ASSOC!=0):
        print('===== L2 contents =====')
        for i in range(len(L2)):
            if i<=9:
                text="Set     "+str(i)+":      "
            elif i<=99:
                text="Set     "+str(i)+":     "
            else:
                text="Set     "+str(i)+":    "
            for value in L2[i]:
                text += hex(int(value,2))[2:]
                if L2_dirty_dict[i][value]=='D':
                    text+=' D  '
                else:
                    text+='    '
            print(text)

    L1_miss_rate = miss_rate_calc_L1(L1_parameters)
    if (L2_SIZE!=0 and L2_ASSOC!=0):
        L2_miss_rate = miss_rate_calc_L2(L2_parameters)

    Traffic_number=0
    print("===== Simulation results (raw) =====")
    print("a. number of L1 reads:        "+str(L1_parameters['L1_reads']))
    print("b. number of L1 read misses:  "+str(L1_parameters['L1_readmiss']))
    print("c. number of L1 writes:       "+str(L1_parameters['L1_writes']))
    print("d. number of L1 write misses: "+str(L1_parameters['L1_writemiss']))
    print("e. L1 miss rate:              {:.6f}".format(L1_miss_rate))
    print("f. number of L1 writebacks:   "+str(L1_parameters['L1_writebacks']))
    print("g. number of L2 reads:        "+str(L2_parameters['L2_reads']))
    print("h. number of L2 read misses:  "+str(L2_parameters['L2_readmiss']))
    print("i. number of L2 writes:       "+str(L2_parameters['L2_writes']))
    print("j. number of L2 write misses: "+str(L2_parameters['L2_writemiss']))
    if (L2_SIZE!=0 and L2_ASSOC!=0):
        print("k. L2 miss rate:              {:.6f}".format(L2_miss_rate))
    else:
        print("k. L2 miss rate:              "+str(0))
    print("l. number of L2 writebacks:   "+str(L2_parameters['L2_writebacks']))
    
    total_mem_traffic = total_mem_traffic_calc(L1_parameters, L2_parameters, inclusive_bit_value)
    print("m. total memory traffic:      "+str(total_mem_traffic))