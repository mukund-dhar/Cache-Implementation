import pandas as pd
from calculations import *

def cacti_table_file_processing(cache_size, assoc, block_size, data):
    filtered_data = data[(data['Cache Size(bytes)'] == cache_size) & 
                         (data['Associativity'] == assoc) & 
                         (data['Block Size(bytes)'] == block_size)]

    if not filtered_data.empty:
        # If there are matching records, return the access time
        return filtered_data['Access Time(ns)'].values[0]
    else:
        # If no matching records found, return None
        return None
    

def read_excel_file(excel_file_path):
    df = pd.read_excel(excel_file_path)
    return df

def aat(miss_rate, cache_size, assoc, block_size, file):
    # print(miss_rate, cache_size, assoc, block_size, file)
    miss_penalty = 100 # given 100 ns
    hit_time = cacti_table_file_processing(cache_size, assoc, block_size, read_excel_file(file))

    aat = hit_time + miss_penalty * miss_rate if hit_time != None else None

    return aat

if __name__ == '__main__':
    # Example usage:
    cache_size = 16384  
    assoc = 4         
    block_size = 32  
    file = 'cacti_table.xls' 

    access_time = cacti_table_file_processing(cache_size, assoc, block_size, read_excel_file(file))
    print(f"Access Time for Cache Size {cache_size}, Associativity {assoc}, Block Size {block_size}: {access_time}")