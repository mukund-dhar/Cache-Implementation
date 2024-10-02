from sim_cache import read_file
from cache_implementation import *
from calculations import *
from aat_calc import aat
import matplotlib.pyplot as plt


trace_file = "traces/gcc_trace.txt" # Using the GCC benchmark for all experiments. 

# Graphs
def graph_1():
    plot = 1
    BLOCKSIZE = 32
    L1_ASSOC = [1, 2, 4, 8, -1]  # -1 represents fully associative
    L1_SIZE = [2 ** i for i in range(10, 21)]  # 1KB to 1MB in powers of two
    L2_SIZE = 0
    L2_ASSOC = 0
    REPLACEMENT_POLICY = 0 # Replacement policy: LRU
    INCLUSION_PROPERTY = 0 # Inclusion property: non-inclusive

    lines = read_file(trace_file)

    for assoc in L1_ASSOC:
        miss_rates = [run(lines, BLOCKSIZE, size, assoc if assoc != -1 else int(size/BLOCKSIZE), L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file, plot) for size in L1_SIZE]
        print(miss_rates)
        label = f'{assoc}-way Set Associative' if assoc != -1 else 'Fully Associative'
        plt.plot([math.log2(size) for size in L1_SIZE], miss_rates, marker='o', label=label)

    plt.title('Graph 1')
    plt.xlabel('Log(Cache Size)')
    plt.ylabel('L1 Cache Miss Rate')
    plt.legend()
    plt.grid(True)
    plt.show()

def graph_2():
    plot = 1
    BLOCKSIZE = 32
    L1_ASSOC = [1, 2, 4, 8, -1]  # -1 represents fully associative
    L1_SIZE = [2 ** i for i in range(10, 21)]  # 1KB to 1MB in powers of two
    L2_SIZE = 0
    L2_ASSOC = 0
    REPLACEMENT_POLICY = 0 # Replacement policy: LRU
    INCLUSION_PROPERTY = 0 # Inclusion property: non-inclusive
    excel_file = 'cacti_table.xls'

    lines = read_file(trace_file)

    for i, assoc in enumerate(L1_ASSOC):
        # print(i)
        miss_rates = [run(lines, BLOCKSIZE, cache_size, assoc if assoc != -1 else int(cache_size/BLOCKSIZE), L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file, plot) for cache_size in L1_SIZE]
        aat_values = [aat(miss_rate, cache_size, assoc if assoc != -1 else ' FA', BLOCKSIZE, excel_file) for miss_rate, cache_size in zip(miss_rates, L1_SIZE)]
        print(aat_values)
        aat_values = [aat_value for aat_value in aat_values if aat_value is not None] # removing None values
        # print('rem none')
        # print(aat_values)
        label = f'{assoc}-way Set Associative' if assoc != -1 else 'Fully Associative'
        plt.plot([math.log2(size) for size in L1_SIZE] if i != 3 else [math.log2(size) for size in L1_SIZE[1:]], aat_values, marker='o', label=label)

    plt.title('Graph 2')
    plt.xlabel('Log(Cache Size)')
    plt.ylabel('AAT')
    plt.legend()
    plt.grid(True)
    plt.show()

def graph_3():

    plot = 1
    BLOCKSIZE = 32
    L1_ASSOC = 4
    L1_SIZE = [2 ** i for i in range(10, 19)] # 1KB to 1MB in powers of two
    L2_SIZE = 0
    L2_ASSOC = 0
    REPLACEMENT_POLICY = [0, 1]
    INCLUSION_PROPERTY = 0 # Inclusion property: non-inclusive
    excel_file = 'cacti_table.xls'

    lines = read_file(trace_file)

    for i, rep_policy in enumerate(REPLACEMENT_POLICY):
        miss_rates = [run(lines, BLOCKSIZE, cache_size, L1_ASSOC, L2_SIZE, L2_ASSOC, rep_policy, INCLUSION_PROPERTY, trace_file, plot) for cache_size in L1_SIZE]
        aat_values = [aat(miss_rate, cache_size, L1_ASSOC, BLOCKSIZE, excel_file) for miss_rate, cache_size in zip(miss_rates, L1_SIZE)]
        print(aat_values)
        aat_values = [aat_value for aat_value in aat_values if aat_value is not None] # removing None values
        # print('rem none')
        # print(aat_values)
        label = 'LRU Replacement policy' if rep_policy == 0 else 'FIFO Replacement policy'
        plt.plot([math.log2(size) for size in L1_SIZE], aat_values, marker='o', label=label)

    plt.title('Graph 3')
    plt.xlabel('Log(Cache Size)')
    plt.ylabel('AAT')
    plt.legend()
    plt.grid(True)
    plt.show()

def graph_4():

    plot = 1
    BLOCKSIZE = 32
    L1_ASSOC = 4
    L1_SIZE = 1024
    L2_SIZE = [2 ** i for i in range(11, 16)]
    L2_ASSOC = 8
    REPLACEMENT_POLICY = 0 # Replacement policy: LRU
    INCLUSION_PROPERTY = [0, 1] 
    excel_file = 'cacti_table.xls'

    lines = read_file(trace_file)

    for i, inc_prop in enumerate(INCLUSION_PROPERTY):
        miss_rates = [run(lines, BLOCKSIZE, L1_SIZE, L1_ASSOC, cache_size, L2_ASSOC, REPLACEMENT_POLICY, inc_prop, trace_file, plot) for cache_size in L2_SIZE]
        aat_values = [aat(miss_rate, cache_size, L2_ASSOC, BLOCKSIZE, excel_file) for miss_rate, cache_size in zip(miss_rates, L2_SIZE)]
        print(aat_values)
        aat_values = [aat_value for aat_value in aat_values if aat_value is not None] # removing None values
        # print('rem none')
        # print(aat_values)
        label = 'Non-inclusive' if inc_prop == 0 else 'Inclusive'
        plt.plot([math.log2(size) for size in L2_SIZE], aat_values, marker='o', label=label)

    plt.title('AAT vs Log2(Cache Size)')
    plt.xlabel('Log2(Cache Size)')
    plt.ylabel('AAT')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # graph_1()
    # graph_2()
    graph_3()
