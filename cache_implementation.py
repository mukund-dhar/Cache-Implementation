import math   
from output import print_sim, print_output
from calculations import *

def LRU_L1_create(L1_set_value, LRU_L1): 
    evict_value =  min(LRU_L1[L1_set_value].values())
    victim_tag = [s for s in LRU_L1[L1_set_value] if LRU_L1[L1_set_value][s]==evict_value]
    return victim_tag[0]

def FIFO_L1_create(L1_set_value, FIFO_L1):
    evict_value =  min(FIFO_L1[L1_set_value].values())
    victim_tag = [s for s in FIFO_L1[L1_set_value] if FIFO_L1[L1_set_value][s]==evict_value]
    return victim_tag[0]

def LRU_L2_create(L2_set_value, LRU_L2): 
    evict_value =  min(LRU_L2[L2_set_value].values())
    victim_tag = [s for s in LRU_L2[L2_set_value] if LRU_L2[L2_set_value][s]==evict_value]
    return victim_tag[0]

def FIFO_L2_create(L2_set_value, FIFO_L2):
    evict_value =  min(FIFO_L2[L2_set_value].values())
    victim_tag = [s for s in FIFO_L2[L2_set_value] if FIFO_L2[L2_set_value][s]==evict_value]
    return victim_tag[0]

def victim_tag_conversion_L1(L1_set_index, victim_tag, L1_exponent_set_size, L2_tag_info):
    intermediate=[]
    L1_set_index=bin(L1_set_index)[2:]
    if len(L1_set_index)<L1_exponent_set_size:
        L1_set_index=str(('0'*(L1_exponent_set_size-len(L1_set_index)))+str(L1_set_index))
    victim_tag=victim_tag + L1_set_index
    L2_tag_value = victim_tag[0:L2_tag_info[2]]
    L2_set_value = int(victim_tag[int(L2_tag_info[2]):int(L2_tag_info[2]+L2_tag_info[1])],2)
    intermediate.append(L2_set_value)
    intermediate.append(L2_tag_value)
    return intermediate

def victim_tag_conversion_L2(L2_set_index, victim_tag, L2_tag_info, L1_tag_limit, L1_exponent_set_size):
    intermediate=[]
    L2_set_index=bin(L2_set_index)[2:]
    if len(L2_set_index)<L2_tag_info[1]:
        L2_set_index=str(('0'*(int(L2_tag_info[1])-len(L2_set_index)))+str(L2_set_index))
    victim_tag=victim_tag + L2_set_index
    L1_tag_value = victim_tag[0:L1_tag_limit]
    L1_set_value = int(victim_tag[L1_tag_limit:L1_tag_limit+L1_exponent_set_size],2)
    intermediate.append(L1_set_value)
    intermediate.append(L1_tag_value)
    return intermediate

def L1_calling(L1_set, L1_tag, REPLACEMENT_POLICY, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1):
    if L1_tag in L1[L1_set]:
        temporary_variable = L1[L1_set].index(L1_tag)
        if L1_dirty_dict[L1_set][L1_tag]=='D':
            inclusive_bit_value[0]+=1
        L1[L1_set].pop(temporary_variable)
        if REPLACEMENT_POLICY == 0:
            del LRU_L1[L1_set][L1_tag]
        if REPLACEMENT_POLICY == 1:
            del FIFO_L1[L1_set][L1_tag]
        del L1_dirty_dict[L1_set][L1_tag]
    
def L2_calling(L2_set_value, L2_tag_value, operation, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, L2_parameters, L2, LRU_L2, FIFO_L2, L2_dirty_dict, L2_tag_info, L1_tag_limit, L1_exponent_set_size, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1):
    if operation=='r':
        L2_parameters['L2_reads']+=1
        if L2_tag_value in L2[L2_set_value]:
            L2_parameters['L2_hits']+=1
            if (REPLACEMENT_POLICY==0):
                LRU_L2[L2_set_value][L2_tag_value]=max(LRU_L2[L2_set_value].values())+1
    
        else:    
            L2_parameters['L2_readmiss']+=1
            if (len(L2[L2_set_value])<L2_ASSOC):
                L2[L2_set_value].append(L2_tag_value)
                if (REPLACEMENT_POLICY==0):
                    if len(LRU_L2[L2_set_value]) != 0:
                        LRU_L2[L2_set_value][L2_tag_value]=max(LRU_L2[L2_set_value].values())+1
                    else:
                        LRU_L2[L2_set_value][L2_tag_value]=0
                
                elif (REPLACEMENT_POLICY==1):
                    if len(FIFO_L2[L2_set_value]) != 0:
                        FIFO_L2[L2_set_value][L2_tag_value]=max(FIFO_L2[L2_set_value].values())+1
                    else:
                        FIFO_L2[L2_set_value][L2_tag_value]=0

                L2_dirty_dict[L2_set_value][L2_tag_value]='NA'
            else:
                if (REPLACEMENT_POLICY==0):
                    LRU_L2[L2_set_value][L2_tag_value]=max(LRU_L2[L2_set_value].values())+1
                    victim_tag = LRU_L2_create(L2_set_value, LRU_L2)
                    if INCLUSION_PROPERTY == 1:
                        L1_victim_address = victim_tag_conversion_L2(L2_set_value, victim_tag, L2_tag_info, L1_tag_limit, L1_exponent_set_size)
                        L1_calling(L1_victim_address[0], L1_victim_address[1], REPLACEMENT_POLICY, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)
                    for i in range(len(L2[L2_set_value])):
                        if L2[L2_set_value][i] == victim_tag:
                            L2[L2_set_value][i] = L2_tag_value                     
                            break
                
                    del LRU_L2[L2_set_value][victim_tag]
                    if L2_dirty_dict[L2_set_value][victim_tag]=='D':
                        L2_parameters['L2_writebacks']+=1
                    
                    L2_dirty_dict[L2_set_value][L2_tag_value]='NA'
                    del L2_dirty_dict[L2_set_value][victim_tag]
                      
                if (REPLACEMENT_POLICY==1):
                    FIFO_L2[L2_set_value][L2_tag_value]=max(FIFO_L2[L2_set_value].values())+1
                    victim_tag = FIFO_L2_create(L2_set_value, FIFO_L2)
                    if(INCLUSION_PROPERTY==1):
                        L1_victim_address = victim_tag_conversion_L2(L2_set_value, victim_tag, L2_tag_info, L1_tag_limit, L1_exponent_set_size)
                        L1_calling(L1_victim_address[0], L1_victim_address[1], REPLACEMENT_POLICY, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)
                    for i in range(len(L2[L2_set_value])):
                        if L2[L2_set_value][i] == victim_tag:
                            L2[L2_set_value][i] = L2_tag_value                      
                            break
                    del FIFO_L2[L2_set_value][victim_tag]
                    if L2_dirty_dict[L2_set_value][victim_tag]=='D':
                        L2_parameters['L2_writebacks']+=1
                    L2_dirty_dict[L2_set_value][L2_tag_value]='NA'
                    del L2_dirty_dict[L2_set_value][victim_tag]

    else:
        L2_parameters['L2_writes']+=1
        if L2_tag_value in L2[L2_set_value]:
            L2_parameters['L2_hits']+=1
            if (REPLACEMENT_POLICY==0):
                LRU_L2[L2_set_value][L2_tag_value]=max(LRU_L2[L2_set_value].values())+1   
            L2_dirty_dict[L2_set_value][L2_tag_value]='D'   
        else:
            L2_parameters['L2_writemiss']+=1
            if (len(L2[L2_set_value])<L2_ASSOC):
                L2[L2_set_value].append(L2_tag_value)
                if (REPLACEMENT_POLICY==0):
                    if len(LRU_L2[L2_set_value]) != 0:
                        LRU_L2[L2_set_value][L2_tag_value]=max(LRU_L2[L2_set_value].values())+1
                    else:
                        LRU_L2[L2_set_value][L2_tag_value]=0
                
                elif (REPLACEMENT_POLICY==1):
                    if len(FIFO_L2[L2_set_value]) != 0:
                        FIFO_L2[L2_set_value][L2_tag_value]=max(FIFO_L2[L2_set_value].values())+1
                    else:
                        FIFO_L2[L2_set_value][L2_tag_value]=0

                L2_dirty_dict[L2_set_value][L2_tag_value]='D'
            
            else:
                if (REPLACEMENT_POLICY==0):
                    LRU_L2[L2_set_value][L2_tag_value]=max(LRU_L2[L2_set_value].values())+1
                    victim_tag = LRU_L2_create(L2_set_value, LRU_L2)
                    if(INCLUSION_PROPERTY==1):
                        L1_victim_address = victim_tag_conversion_L2(L2_set_value, victim_tag, L2_tag_info, L1_tag_limit, L1_exponent_set_size)
                        L1_calling(L1_victim_address[0], L1_victim_address[1], REPLACEMENT_POLICY, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)

                    for i in range(len(L2[L2_set_value])):
                        if L2[L2_set_value][i] == victim_tag:
                            L2[L2_set_value][i] = L2_tag_value
                            break
                    del LRU_L2[L2_set_value][victim_tag]
                    if L2_dirty_dict[L2_set_value][victim_tag]=='D':
                        L2_parameters['L2_writebacks']+=1
                    del L2_dirty_dict[L2_set_value][victim_tag]
                    L2_dirty_dict[L2_set_value][L2_tag_value] = "D"  

                if (REPLACEMENT_POLICY==1):
                    FIFO_L2[L2_set_value][L2_tag_value]=max(FIFO_L2[L2_set_value].values())+1
                    victim_tag = FIFO_L2_create(L2_set_value, FIFO_L2)
                    if(INCLUSION_PROPERTY==1):
                        L1_victim_address = victim_tag_conversion_L2(L2_set_value, victim_tag, L2_tag_info, L1_tag_limit, L1_exponent_set_size)
                        L1_calling(L1_victim_address[0], L1_victim_address[1], REPLACEMENT_POLICY, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)
                    for i in range(len(L2[L2_set_value])):
                        if L2[L2_set_value][i] == victim_tag:
                            L2[L2_set_value][i] = L2_tag_value
                            break
                    del FIFO_L2[L2_set_value][victim_tag]
                    if L2_dirty_dict[L2_set_value][victim_tag]=='D':
                        L2_parameters['L2_writebacks']+=1
                    del L2_dirty_dict[L2_set_value][victim_tag]
                    L2_dirty_dict[L2_set_value][L2_tag_value] = "D"


def run(lines, BLOCKSIZE, L1_SIZE, L1_ASSOC, L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file, plot):

    inclusive_bit_value=[0]

    # print(BLOCKSIZE, L1_SIZE, L1_ASSOC, L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file, plot)

    #calculations for L1
    L1_set_size = (L1_SIZE)//(BLOCKSIZE*L1_ASSOC)
    L1_exponent_set_size = int(math.log2(L1_set_size))
    L1_tag_limit = 32-L1_exponent_set_size-int(math.log2(BLOCKSIZE))
    L1_parameters={'L1_reads':0,'L1_writes':0,'L1_readmiss':0,'L1_writemiss':0,'L1_hits':0,'L1_writebacks':0}

    L1={}
    for i in range(L1_set_size):
        L1[i]=[]

    LRU_L1={}
    for i in range(L1_set_size):
        LRU_L1[i]={}

    FIFO_L1={}
    for i in range(L1_set_size):
        FIFO_L1[i]={}

    L1_dirty_dict={}
    for i in range(L1_set_size):
        L1_dirty_dict[i]={}

    temp=[]
    L2_parameters={'L2_reads':0,'L2_writes':0,'L2_readmiss':0,'L2_writemiss':0,'L2_hits':0,'L2_writebacks':0}
    L2_tag_info=[]

    #calculations for L2
    L2={}
    LRU_L2={}
    FIFO_L2={}
    L2_dirty_dict={}

    if (L2_SIZE !=0 and L2_ASSOC!=0):
        L2_set_size = (L2_SIZE)//(BLOCKSIZE*L2_ASSOC)
        L2_exponent_set_size = int(math.log2(L2_set_size))
        L2_tag_limit = 32-L2_exponent_set_size-int(math.log2(BLOCKSIZE))
        L2_tag_info.append(L2_set_size)
        L2_tag_info.append(L2_exponent_set_size)
        L2_tag_info.append(L2_tag_limit)
       
        for i in range(L2_set_size):
            L2[i]=[]
       
        for i in range(L2_set_size):
            LRU_L2[i]={}
       
        for i in range(L2_set_size):
            FIFO_L2[i]={}
       
        for i in range(L2_set_size):
            L2_dirty_dict[i]={}


    for i in range(len(lines)):
        temp.append(lines[i].strip('\n').split(' '))
        if len(temp[i][1])<8:
            number_of_zeroes=8-len(temp[i][1])
            temp[i][1]=str(('0'*number_of_zeroes)+str(temp[i][1]))
            #binary conversion -> 32
        temp[i][1]=bin(int(temp[i][1],16))[2:].zfill(32)
        L1_tag_value = temp[i][1][0:L1_tag_limit]
        if len(temp[i][1][L1_tag_limit:L1_tag_limit+L1_exponent_set_size])==0:
            L1_set_value=0
        else:
            L1_set_value = int(temp[i][1][L1_tag_limit:L1_tag_limit+L1_exponent_set_size],2)
        if (L2_SIZE !=0 and L2_ASSOC!=0):
            L2_tag_value = temp[i][1][0:L2_tag_limit]
            L2_set_value = int(temp[i][1][L2_tag_limit:L2_tag_limit+L2_exponent_set_size],2)

        if temp[i][0]=='r':
            L1_parameters['L1_reads']+=1
            if L1_tag_value in L1[L1_set_value]:
                L1_parameters['L1_hits']+=1
                if (REPLACEMENT_POLICY==0):
                    LRU_L1[L1_set_value][L1_tag_value]=max(LRU_L1[L1_set_value].values())+1
                
            else:    
                L1_parameters['L1_readmiss']+=1
                if (len(L1[L1_set_value])<L1_ASSOC):
                    L1[L1_set_value].append(L1_tag_value)
                    if (REPLACEMENT_POLICY==0):
                        if len(LRU_L1[L1_set_value]) != 0:
                            LRU_L1[L1_set_value][L1_tag_value]=max(LRU_L1[L1_set_value].values())+1
                        else:
                            LRU_L1[L1_set_value][L1_tag_value]=0
                    
                    elif (REPLACEMENT_POLICY==1):
                        if len(FIFO_L1[L1_set_value]) != 0:
                            FIFO_L1[L1_set_value][L1_tag_value]=max(FIFO_L1[L1_set_value].values())+1
                        else:
                            FIFO_L1[L1_set_value][L1_tag_value]=0

                    L1_dirty_dict[L1_set_value][L1_tag_value]='NA'

                else:
                    if (REPLACEMENT_POLICY==0):
                        LRU_L1[L1_set_value][L1_tag_value]=max(LRU_L1[L1_set_value].values())+1
                        victim_tag = LRU_L1_create(L1_set_value, LRU_L1)
                        for i in range(len(L1[L1_set_value])):
                            if L1[L1_set_value][i] == victim_tag:
                                L1[L1_set_value][i] = L1_tag_value                  
                                break
                        del LRU_L1[L1_set_value][victim_tag]
                        if L1_dirty_dict[L1_set_value][victim_tag]=='D':
                            L1_parameters['L1_writebacks']+=1
                            if (L2_SIZE!=0 and L2_ASSOC!=0):
                                L2_victim_address = victim_tag_conversion_L1(L1_set_value, victim_tag, L1_exponent_set_size, L2_tag_info)
                                L2_calling(L2_victim_address[0], L2_victim_address[1],'w', L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, L2_parameters, L2, LRU_L2, FIFO_L2, L2_dirty_dict, L2_tag_info, L1_tag_limit, L1_exponent_set_size, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)

                        L1_dirty_dict[L1_set_value][L1_tag_value]='NA'
                        del L1_dirty_dict[L1_set_value][victim_tag]
                        
                    if (REPLACEMENT_POLICY==1):
                        FIFO_L1[L1_set_value][L1_tag_value]=max(FIFO_L1[L1_set_value].values())+1
                        victim_tag = FIFO_L1_create(L1_set_value, FIFO_L1)
                        for i in range(len(L1[L1_set_value])):
                            if L1[L1_set_value][i] == victim_tag:
                                L1[L1_set_value][i] = L1_tag_value                      
                                break
                        del FIFO_L1[L1_set_value][victim_tag]
                        if L1_dirty_dict[L1_set_value][victim_tag]=='D':
                            L1_parameters['L1_writebacks']+=1
                            if (L2_SIZE!=0 and L2_ASSOC!=0):
                                L2_victim_address = victim_tag_conversion_L1(L1_set_value, victim_tag, L1_exponent_set_size, L2_tag_info)
                                L2_calling(L2_victim_address[0], L2_victim_address[1],'w', L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, L2_parameters, L2, LRU_L2, FIFO_L2, L2_dirty_dict, L2_tag_info, L1_tag_limit, L1_exponent_set_size, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)
                        L1_dirty_dict[L1_set_value][L1_tag_value]='NA'
                        del L1_dirty_dict[L1_set_value][victim_tag]
                    
                if (L2_SIZE!=0 and L2_ASSOC!=0):
                    L2_calling(L2_set_value,L2_tag_value,'r', L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, L2_parameters, L2, LRU_L2, FIFO_L2, L2_dirty_dict, L2_tag_info, L1_tag_limit, L1_exponent_set_size, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)               


        else:
            L1_parameters['L1_writes']+=1
            if L1_tag_value in L1[L1_set_value]:
                L1_parameters['L1_hits']+=1
                if (REPLACEMENT_POLICY==0):
                    LRU_L1[L1_set_value][L1_tag_value]=max(LRU_L1[L1_set_value].values())+1   
                L1_dirty_dict[L1_set_value][L1_tag_value]='D'   
            else:
                L1_parameters['L1_writemiss']+=1
                if (len(L1[L1_set_value])<L1_ASSOC):
                    L1[L1_set_value].append(L1_tag_value)
                    if (REPLACEMENT_POLICY==0):
                        if len(LRU_L1[L1_set_value]) != 0:
                            LRU_L1[L1_set_value][L1_tag_value]=max(LRU_L1[L1_set_value].values())+1
                        else:
                            LRU_L1[L1_set_value][L1_tag_value]=0
                    
                    elif (REPLACEMENT_POLICY==1):
                        if len(FIFO_L1[L1_set_value]) != 0:
                            FIFO_L1[L1_set_value][L1_tag_value]=max(FIFO_L1[L1_set_value].values())+1
                        else:
                            FIFO_L1[L1_set_value][L1_tag_value]=0
                    
                    L1_dirty_dict[L1_set_value][L1_tag_value]='D'
                
                else:
                    if (REPLACEMENT_POLICY==0):
                        LRU_L1[L1_set_value][L1_tag_value]=max(LRU_L1[L1_set_value].values())+1
                        victim_tag = LRU_L1_create(L1_set_value, LRU_L1)
                        for i in range(len(L1[L1_set_value])):
                            if L1[L1_set_value][i] == victim_tag:
                                L1[L1_set_value][i] = L1_tag_value
                                break
                        del LRU_L1[L1_set_value][victim_tag]
                        if L1_dirty_dict[L1_set_value][victim_tag]=='D':
                            L1_parameters['L1_writebacks']+=1
                            if (L2_SIZE!=0 and L2_ASSOC!=0):
                                L2_victim_address = victim_tag_conversion_L1(L1_set_value, victim_tag, L1_exponent_set_size, L2_tag_info)
                                L2_calling(L2_victim_address[0], L2_victim_address[1],'w', L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, L2_parameters, L2, LRU_L2, FIFO_L2, L2_dirty_dict, L2_tag_info, L1_tag_limit, L1_exponent_set_size, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)
                        del L1_dirty_dict[L1_set_value][victim_tag]
                        L1_dirty_dict[L1_set_value][L1_tag_value] = "D"  

                    if (REPLACEMENT_POLICY==1):
                        FIFO_L1[L1_set_value][L1_tag_value]=max(FIFO_L1[L1_set_value].values())+1
                        victim_tag = FIFO_L1_create(L1_set_value, FIFO_L1)
                        for i in range(len(L1[L1_set_value])):
                            if L1[L1_set_value][i] == victim_tag:
                                L1[L1_set_value][i] = L1_tag_value
                                break
                        del FIFO_L1[L1_set_value][victim_tag]
                        if L1_dirty_dict[L1_set_value][victim_tag]=='D':
                            L1_parameters['L1_writebacks']+=1
                            if (L2_SIZE!=0 and L2_ASSOC!=0):
                                L2_victim_address = victim_tag_conversion_L1(L1_set_value, victim_tag, L1_exponent_set_size, L2_tag_info)
                                L2_calling(L2_victim_address[0], L2_victim_address[1],'w', L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, L2_parameters, L2, LRU_L2, FIFO_L2, L2_dirty_dict, L2_tag_info, L1_tag_limit, L1_exponent_set_size, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)
                        del L1_dirty_dict[L1_set_value][victim_tag]
                        L1_dirty_dict[L1_set_value][L1_tag_value] = "D"

                if (L2_SIZE!=0 and L2_ASSOC!=0):
                    L2_calling(L2_set_value,L2_tag_value,'r', L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, L2_parameters, L2, LRU_L2, FIFO_L2, L2_dirty_dict, L2_tag_info, L1_tag_limit, L1_exponent_set_size, L1, L1_dirty_dict, inclusive_bit_value, LRU_L1, FIFO_L1)

    if plot == 0:
        obj=print_sim(BLOCKSIZE, L1_SIZE, L1_ASSOC, L2_SIZE, L2_ASSOC, REPLACEMENT_POLICY, INCLUSION_PROPERTY, trace_file)
        obj.out()
        print_output(L1, L1_parameters, L1_dirty_dict, L2, L2_parameters, L2_dirty_dict, L2_SIZE, L2_ASSOC, inclusive_bit_value)

    elif plot == 1:
        return miss_rate_calc_L1(L1_parameters)

