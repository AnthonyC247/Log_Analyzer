# -*- coding: utf-8 -*-
"""log_analyzer

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cS3Zif9o1n16-L2xZwopArQ9llHJ0WEK

# Programming Assignment 2, CSE30-02, Winter 2023

## README

* Please follow the instructions given below (in the comments) to 
  use this Colab notebook
  * Only edit within the allowed sections as instructed by the
    comments
  * DO NOT change anything outside those sections
* Testing script is provided at the end to help you to ensure your 
  implementation is compatible with the autograder
  * If your code doesn't work with the testing script, it's not 
    compatible with the autograder; so it will fail the grading 
    for sure
  * If your code work with the testing script, it's compatible 
    with the autograder; but, this **DOES NOT** guarantee your 
    output will be correct for the inputs we provided during the 
    grading process
* To run the testing script, on menu bar, click `Runtime` -> `Run all`
* After you finished testing your code, you may download this notebook
  containing your code as **.py** file, and submit to Canvas
  * To download this notebook as .py file, on menu bar, 
    click `File` -> `Download` -> `Download .py`
"""

import json
import pandas

from typing import List
import re
import datetime
import numpy as np

def log_to_dataframe(
    src_log_filepath: str,
) -> pandas.DataFrame:
    '''
    - Parameters:
        - src_log_filepath: path to the log file
    - Returns:
        - pandas.DataFrame: a pandas.DataFrame object parsed from
          the log file
    '''
    #===== Please enter your implementation below this line ----->

    #Reading the data by accessing columns directly
    df = pandas.read_table('small_input.log', sep = '\s(?!-\\d{4})', header = None, names = ['host', 'timestamp', 'method', 'url', 'version', 'response_code', 'content_size'],
                           usecols=[0,3,4,5,6,7,8])
    
    #Cleaning the data
    df['timestamp'] = df['timestamp'].str.replace(pat=r'[\[\]]', repl=r'', regex=True)
    df['method'] = df['method'].str.replace(pat=r'[\"]', repl=r'', regex=True)
    df['version'] = df['version'].str.replace(pat=r'[\"]', repl=r'', regex=True)

    #Coverting to UTC Timezone 
    df['timestamp'] = pandas.to_datetime(df['timestamp'], format= '%d/%b/%Y:%H:%M:%S %z').apply(lambda x: x.date())

    return df
    #===== <----- Please keep your implementation above this line
    pass

def get_num_of_distinct_resp_code(data: pandas.DataFrame) -> int:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
    - Returns:
        - int: number of distinct response code
    '''
    #===== Please enter your implementation below this line ----->
    return len(data.response_code.unique())
    #===== <----- Please keep your implementation above this line
    pass


def get_median_content_size(data: pandas.DataFrame) -> int:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
    - Returns:
        - int: median content size
          - float numbers should be **type-casted** into integer numbers
    '''
   
    data['content_size'].replace('-', np.nan, inplace=True)

    return int(data['content_size'].median(skipna=True))
    
    #pass

def get_most_freq_hosts(data: pandas.DataFrame, numOfHosts: int) -> List[str]:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
        - numOfHosts: top `numOfHosts` most frequency hosts
    - Returns:
        - List[str]: list of strings containing top `numOfHosts` most
          frequency hosts; ordered from top 1 to top `numOfHosts`
    '''
   
    new_df = data.groupby(['host'])['host'].count().sort_values(ascending = False).reset_index(name = 'count')
    return new_df['host'].values[:numOfHosts].tolist()
    
    #pass

def get_most_freq_urls(data: pandas.DataFrame, numOfUrls: int) -> List[str]:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
        - numOfUrls: top `numOfUrls` most frequency URLs
    - Returns:
        - List[str]: list of strings containing top `numOfUrls` 
          most frequency URLs; ordered from top 1 to top 
          `numOfUrls`
    '''
   
    new_df = data.groupby(['url'])['url'].count().sort_values(ascending = False).reset_index(name = 'count')
    return new_df['url'].values[:numOfUrls].tolist()
    
    #pass


def get_top_urls_recv_err(data: pandas.DataFrame, numOfUrls: int) -> List[str]:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
        - numOfUrls: top `numOfUrls` URLs that received error 
          response codes
    - Returns:
        - List[str]: list of strings containing top `numOfUrls`
          URLs that received error response codes; ordered from
          top 1 to top `numOfUrls`
    '''
    
    myDict = {} #empty dict
    urls = [] #List to later store the urls
    counting = data[["url", 'response_code']].value_counts() #accessing the data from both urls and response codes
    for i,j in counting.items(): #looping through every element of data from both url and response codes
      if '200' not in i: #ignore the string of 200
       myDict[i] = j # assign index of i to equal element of j
    y = {val[0] : val[1] for val in sorted(myDict.items(), key = lambda x: (-x[1], x[0]))}
 
    for i in y: #Looping through every sorted item in new sorted dictionary 
      urls.append(i[0]) #Adding every element of index i to the list of urls 
    return urls[0:numOfUrls] #returning the urls through its indecy range from 0 until completed
    
    #pass

def get_num_of_req_recv_404(data: pandas.DataFrame) -> int:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
    - Returns:
        - int: number of requests received 404 responses
    '''
   
    return len(data[data.response_code==404])
    
    #pass

def get_num_of_unique_hosts_daily(data: pandas.DataFrame) -> List[int]:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
    - Returns:
        - List[int]: List of integers of unique hosts on each 
          day, ordered from the earliest to latest date
    '''
    
    return data.groupby(['timestamp'])['host'].nunique().tolist()
    
    #pass

def get_avg_num_of_req_per_host_daily(data: pandas.DataFrame) -> List[int]:
    '''
    - Parameters:
        - data: input dataframe, received from log_to_dataframe function call
    - Returns:
        - List[int]: List of integers of average requests per 
          host on each day, ordered from the earliest to 
          latest date
          - float numbers should be **type-casted** into integer numbers
    '''
    
    return data.groupby(['timestamp', 'host'])['host'].count().groupby('timestamp').mean().values.astype(int).tolist()
    
    #pass

def write_results_to_json(
    res1: int,
    res2: int,
    res3: List[str],
    res4: List[str],
    res5: List[str],
    res6: int,
    res7: List[int],
    res8: List[int],
    dest_json_path: str
) -> None:
    '''
    - Parameters:
        - res1: result generated by the function corresponding to question 1
        - res2: result generated by the function corresponding to question 2
        - res3: result generated by the function corresponding to question 3
        - res4: result generated by the function corresponding to question 4
        - res5: result generated by the function corresponding to question 5
        - res6: result generated by the function corresponding to question 6
        - res7: result generated by the function corresponding to question 7
        - res8: result generated by the function corresponding to question 8
        - dest_json_path: filepath to write the json file to
    '''
   
    with open(dest_json_path, 'w') as file:
      json.dump({'get_num_of_distinct_resp_code': res1,
                 'get_median_content_size': res2,
                 'get_most_freq_hosts': res3,
                 'get_most_freq_urls': res4,
                 'get_top_urls_recv_err': res5,
                 'get_num_of_req_recv_404': res6,
                 'get_num_of_unique_hosts_daily': res7,
                 'get_avg_num_of_req_per_host_daily': res8},
                file)
    
    #pass

LOG_FILE_PATH = 'small_input.log'
JSON_FILE_PATH = 'test.json'

#XXXXX DO NOT change anything below this line ----->

def assert_ret_val(res: bool, funcName: str, hint: str) -> None:
    if not res:
        print('AssertionError: {} failed; {}'.format(funcName, hint))
        return False
    print('AssertionOK: {}'.format(funcName))
    return True

def main() -> None:

    # NOTE: here we only test the input/output date types
    # to ensure your code is compatible with autograder
    # During grading process, we will be inspecting the
    # actual content of the return values

    df = log_to_dataframe(LOG_FILE_PATH)
    print('DataFrame:\n', df)
    assert_ret_val(type(df) == pandas.DataFrame, 'log_to_dataframe', 'return type is wrong')

    res1 = get_num_of_distinct_resp_code(df)
    print('get_num_of_distinct_resp_code:', res1)
    assert_ret_val(type(res1) == int, 'get_num_of_distinct_resp_code', 'return type is wrong')

    res2 = get_median_content_size(df)
    print('get_median_content_size:', res2)
    assert_ret_val(type(res2) == int, 'get_median_content_size', 'return type is wrong')

    res3 = get_most_freq_hosts(df, 10)
    print('get_most_freq_hosts:', res3)
    if assert_ret_val(type(res3) == list, 'get_most_freq_hosts', 'return type is wrong'):
        for item in res3:
            assert_ret_val(type(item) == str, 'get_most_freq_hosts', 'return type is wrong')

    res4 = get_most_freq_urls(df, 10)
    print('get_most_freq_urls:', res4)
    if assert_ret_val(type(res4) == list, 'get_most_freq_urls', 'return type is wrong'):
        for item in res4:
            assert_ret_val(type(item) == str, 'get_most_freq_urls', 'return type is wrong')

    res5 = get_top_urls_recv_err(df, 10)
    print('get_top_urls_recv_err:', res5)
    if assert_ret_val(type(res5) == list, 'get_top_urls_recv_err', 'return type is wrong'):
        for item in res5:
            assert_ret_val(type(item) == str, 'get_top_urls_recv_err', 'return type is wrong')

    res6 = get_num_of_req_recv_404(df)
    print('get_num_of_req_recv_404:', res6)
    assert_ret_val(type(res6) == int, 'get_num_of_req_recv_404', 'return type is wrong')

    res7 = get_num_of_unique_hosts_daily(df)
    print('get_num_of_unique_hosts_daily:', res7)
    if assert_ret_val(type(res7) == list, 'get_num_of_unique_hosts_daily', 'return type is wrong'):
        for item in res7:
            assert_ret_val(type(item) == int, 'get_num_of_unique_hosts_daily', 'return type is wrong')

    res8 = get_avg_num_of_req_per_host_daily(df)
    print('get_avg_num_of_req_per_host_daily:', res8)
    if assert_ret_val(type(res8) == list, 'get_avg_num_of_req_per_host_daily', 'return type is wrong'):
        for item in res8:
            assert_ret_val(type(item) == int, 'get_avg_num_of_req_per_host_daily', 'return type is wrong')

    write_results_to_json(
        res1,
        res2,
        res3,
        res4,
        res5,
        res6,
        res7,
        res8,
        JSON_FILE_PATH
    )

    try:
        with open(JSON_FILE_PATH, 'r') as f:
            file_content = f.read()
            print('write_results_to_json:', file_content)
            res_c = json.loads(file_content)
            print('write_results_to_json:', res_c)
            assert_ret_val(type(res_c) == dict, 'write_results_to_json', 'json data type is wrong')
    except FileNotFoundError:
        assert_ret_val(False, 'write_results_to_json', 'json file is not found')
    except json.JSONDecodeError:
        assert_ret_val(False, 'write_results_to_json', 'json file content is invalid')

    print('Test finished')


if __name__ == '__main__':
    main()
#XXXXX <----- DO NOT change anything above this line