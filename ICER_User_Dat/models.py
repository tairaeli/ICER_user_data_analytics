"""
Contains models for each aspect of ICER userbase analyzed in 
this project
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# identify users with many files
def UsersWithManyFiles(data, file_limit):
    '''
    Function to identify users with many files using a file limit 
    as a number integer of the limit of number of files per user.

    args:
        data - dataset containing columns related to user
        file_limit - integer resembling the file limit per user
    
    returns: 
        users that are have a greater number of total files than the 
        file limit.

        *Note: left column = UID, right column = # of files*
    '''

    file_count_per_user = data.groupby("UID numeric ID for the owner of the file").size()

    return file_count_per_user[file_count_per_user.sort_values()>file_limit]
    

def FindUnterutilizerSLURM(data, thresholds):
    """
    Finds user who are requesting more resources than they use
    """

    return None

def GroupUsersSLURM(data, ngroups):
    """
    Groups users based on their utilization patterns of the HPCC
    """
    return None

def PredWalltimeSLURM(data):
    """
    Predicts how long a given job will sit in queue before running
    """
    return None
