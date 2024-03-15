"""
Contains models for each aspect of ICER userbase analyzed in 
this project
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from collections import Counter

# identify users with many files
def UsersWithManyFiles(data, file_limit):
    '''
    Function to identify users with many files using a file limit 
    as a number integer of the limit of number of files per user.

    args:
        data - dataset containing columns related to user
        file_limit - integer resembling the file limit per user
    
    returns: 
        a dataframe of users that are have a greater number of total files than the 
        file limit.

    '''

    # Group by the user ID and count the number of files for each user
    file_count_per_user = data.groupby("UID numeric ID for the owner of the file").size()
    
    # Filter users who have more files than the file_limit
    users_with_many_files = file_count_per_user[file_count_per_user > file_limit]
    
    # Convert the filtered Series object to a DataFrame
    users_with_many_files_df = users_with_many_files.reset_index()
    
    users_with_many_files_df.columns = ['UID numeric ID for the owner of the file', 'Number of files']
    
    
    # Sort by 'Number of files' in descending order
    users_with_many_files_df.sort_values('Number of files', ascending=False, inplace=True)
    
    return users_with_many_files_df
    
##
def FindUnterutilizerGPFS(data, threshold):
    """
    Identifies and returns entries for files where the actual utilization is significantly 
    lower than the allocated resources, based on a given threshold. This helps in identifying 
    inefficient resource usage in GPFS (General Parallel File System).

    The function calculates the underutilization by subtracting the kilobytes allocated 
    for each file (adjusted by a fixed overhead of 3000 KB to bytes) from the file size in bytes. 
    It then filters and returns the entries where this underutilized value exceeds a specified threshold.

    Parameters:
        data (pd.DataFrame): A pandas DataFrame containing the dataset with at least 
                             'File Size' and 'KB Allocated' columns. 'File Size' should be in bytes,
                             and 'KB Allocated' should be in kilobytes.
        threshold (int or float): A numeric threshold for the 'underutilized (Bytes)' value. Entries with
                                  underutilization greater than this threshold will be returned.

    Returns:
        pd.DataFrame: A DataFrame containing the rows from the input DataFrame where the underutilization
                      (calculated as 'File Size' in bytes minus 'KB Allocated' in bytes, including a fixed
                      overhead) exceeds the specified threshold.

    Note:
        - The function adds a fixed overhead of 3000 KB to the 'KB Allocated' before conversion and 
          calculation to account for system or operational reserves that might not be reflected 
          in the raw 'KB Allocated' values.
        - Ensure that the input DataFrame contains the necessary columns with appropriate units 
          as described.
    """
    
    # Conversion of KB Allocated to bytes and adjustment for overhead, then calculation of underutilized space
    data["underutilized (Bytes)"] = data['File Size'] - (data['KB Allocated'] * 1000 + 3000)
    
    # Filter and return rows where underutilization exceeds the threshold
    out = data[data['underutilized (Bytes)'] > threshold]
    
    return out

def FindUnterutilizerSLURM(data, thresholds):
    """
    Finds user who are requesting more resources than they use
    """

    return None
##


def convert_to_minutes(td_str):
    td = pd.Timedelta(td_str)
    return td.total_seconds() / 60



def GroupUsersSLURM(data,k):
    """
    Groups users based on their utilization patterns of the HPCC
    This done via K-Means Clustering after first running a Principal Component Analysis 
    args:
        data - dataset containing columns related to user
        k - Number of Cluster for K-Means to Use
    returns:
        plot - Plot of K-Means with 1st and 2nd Feature Space
        df_PCA - The data frame after PCA has been run, with labels added
        kmeans - The Kmeans model
        table_data - This will show you the number of of observations in each Cluster
        
        
    """
    df=data
    df['Timelimit_']=df['Timelimit'].apply(convert_to_minutes)
    df['time_column']=pd.to_timedelta(df['Elapsed'])
    df['total_minutes']=df['time_column'].dt.total_seconds() / 60
    features2=['CPUTimeRAW','ReqCPUS','AllocCPUS','ReqNodes','NNodes','Timelimit_','total_minutes','ReqMem_MB']
    df_pca=df[features2]
    scaler = StandardScaler()
    df_pca=scaler.fit_transform(df_pca)
    pca = PCA(2)
    df_pca = pca.fit_transform(df_pca)
    df_pca = pd.DataFrame(df_pca, columns=['Feature space for 1st feature', 'Feature space for 2nd feature'])
    kmeans = KMeans(n_clusters=k,algorithm='auto',init='k-means++',max_iter=300)
    kmeans.fit_predict(df_pca)
    labels = kmeans.labels_
    df_pca['Cluster'] = labels
    plot=sns.scatterplot(x=df_pca['Feature space for 1st feature'], y=df_pca['Feature space for 2nd feature'], hue='Cluster', data=df_pca, palette='viridis')
    plt.title('K-Means Clustering')

    cluster_counts = Counter(labels)
    percentages = {cluster: count / len(df) * 100 for cluster, count in cluster_counts.items()}
    
    percentages = {cluster: count / len(df) * 100 for cluster, count in cluster_counts.items()}
    
    table_data = pd.DataFrame(list(percentages.items()), columns=['Cluster Label', 'Percentage (%)'])
    
    return plot, df_pca, kmeans, table_data
    
    
    

def PredWalltimeSLURM(data):
    """
    Predicts how long a given job will sit in queue before running
    """
    return None

def AggSLURMDat(dat):
    '''
    Aggregates all submitted jobs together, removing all batch/extern 
    jobs and including said information into a single job. Excludes
    jobs that do not have a clear '.batch' and '.extern' files

    args:

        dat - the slurm dataset 
    
    returns:

        out_df - the aggregated version of the slurm dataset
    '''
    
    # initializing output dataframe
    out_df = pd.DataFrame(columns=dat.keys())

    # creating list of unique job ids
    job_list = dat["JobID"].value_counts().index

    # iterating through each unique job id
    for job in job_list:

        # filtering data for a given unique job
        jdat = dat[dat["JobID"] == job]

        # creating list of unique CPU times
        cpu_time_list = jdat["CPUTimeRAW"].value_counts()
        # doing some weird masking things to find .batch + agg job pairs
        cpu_time_list = cpu_time_list[cpu_time_list == 2].index

        # iterating through each cpu time for a given job id
        # should only run once unless the job is an array job
        for cpu_time in cpu_time_list:
            
            # masking data for a specific cpu time 
            # this SHOULD isolate a batch+agg job pair
            ajob = jdat[jdat["CPUTimeRAW"] == cpu_time]

            # if the job is user_258, should be the batch job
            batch_job = ajob[ajob["User"] == "user_258"]

            # if there is a unique id, should be the agg job
            ag_job = ajob[ajob["User"] != "user_258"]

            # some weird edge cases I found 
            if len(ag_job["User"]) == 0:
                print("Weird Job",ajob["JobID"])
                print("No aggregate job")
                continue
            
            if len(ag_job["User"]) == 2:
                print("Weird Job",ajob["JobID"])
                print("2 copies of aggregate job")
                continue
            
            # checks for any more unique edge cases in the slurm data
            assert len(ag_job["User"]) == 1, "New edge case discovered!"

            # appending MaxRSS data to agg job
            ag_job.loc[ag_job.index[0],"MaxRSS"] = batch_job["MaxRSS"].values[0]

            # appending new row to output directory
            out_df = pd.concat([out_df,ag_job])

    return out_df
