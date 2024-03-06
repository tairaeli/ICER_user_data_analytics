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

def CleanSLURMDat(dat):
    '''
    Aggregates all submitted jobs together, removing all batch/extern 
    jobs and including said information into a single job. Excludes
    jobs that do not have a clear '.batch' and '.extern' files

    args:

        dat - the slurm dataset 
    
    returns:

        out_df - the aggregated version of the slurm dataset
    '''
    
    job_list = dat["JobID"].value_counts().index

    out_df = pd.DataFrame(columns=dat.keys())

    for job in job_list:

        jdat = dat[dat["JobID"] == job]

        cpu_time_list = jdat["CPUTimeRAW"].value_counts()
        cpu_time_list = cpu_time_list[cpu_time_list == 2].index

        for cpu_time in cpu_time_list:

            ajob = jdat[jdat["CPUTimeRAW"] == cpu_time]

            batch_job = ajob[ajob["User"] == "user_258"]

            ag_job = ajob[ajob["User"] != "user_258"]

            if len(ag_job["User"]) == 0:
                print("Weird Job",ajob["JobID"])
                print("No aggregate job")
                continue
            
            if len(ag_job["User"]) == 2:
                print("Weird Job",ajob["JobID"])
                print("2 copies of aggregate job")
                continue

            assert len(ag_job["User"]) == 1, "New edge case discovered!"

            ag_job.loc[ag_job.index[0],"MaxRSS"] = batch_job["MaxRSS"].values[0]

            out_df = pd.concat([out_df,ag_job])

    return out_df