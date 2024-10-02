def miss_rate_calc_L1(L1_parameters):

    L1_miss_rate = float((L1_parameters['L1_readmiss']+L1_parameters['L1_writemiss'])/(L1_parameters['L1_reads']+L1_parameters['L1_writes']))
    return L1_miss_rate

def miss_rate_calc_L2(L2_parameters):            
           
    L2_miss_rate = float((L2_parameters['L2_readmiss'])/(L2_parameters['L2_reads']))
    return L2_miss_rate

def total_mem_traffic_calc(L1_parameters, L2_parameters, inclusive_bit_value):

    if L2_parameters['L2_reads']==0:
        total_mem_traffic = L1_parameters['L1_readmiss']+L1_parameters['L1_writemiss']+L1_parameters['L1_writebacks']
    else:
        total_mem_traffic = L2_parameters['L2_readmiss']+L2_parameters['L2_writemiss']+L2_parameters['L2_writebacks'] + inclusive_bit_value[0]

    return total_mem_traffic