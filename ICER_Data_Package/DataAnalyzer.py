import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class DataAnalyzer:

    # add preprocessing=false parameter to specify if user want preprocessing then call preprocessing method
    def __init__(self, gpfspath='', slurmpath='', full_dataset=False):
        # initialize data to None
        self.gpfs_data = None
        self.slurm_data = None
        self.slurm_agg = None
        
        # printing each data file path
        print('gpfs path=',gpfspath)
        print('slurm path=',slurmpath)
        
        # direct each data path to read_gpfs or read_slurm depending on path
        if gpfspath != '':
            # either read in portion of dataset using read_gpfs or whole dataset through lazy_loading_gpfs
            if not full_dataset:
                self.read_gpfs(gpfspath)
            else:
                self.lazy_loading_gpfs(gpfspath)
            
        if slurmpath != '':
            self.read_slurm(slurmpath)
        
        
    def read_gpfs(self, gpfspath):
        column_names = ["Inode (file unique ID)",
                        "KB Allocated",
                        "File Size",
                        "Creation Time in days from today",
                        "Change Time in days from today",
                        "Modification time in days from today",
                        "Acces time in days from today",
                        "GID numeric ID for the group owner of the file",
                        "UID numeric ID for the owner of the file"]
        # set gpfs_data to outputed pandas dataset
        self.gpfs_data = pd.read_csv(gpfspath, header=None, names=column_names, delimiter=' ', nrows=1e5)
        return self.gpfs_data

    def lazy_loading_gpfs(self, gpfspath):
        self.gpfs_data = []  # List to store each row's data
        max_rows = 1000  # or set to None for full data
        row_counter = 0
        
        column_names = [
            "Inode (file unique ID)", "KB Allocated", "File Size", 
            "Creation Time in days from today", "Change Time in days from today", 
            "Modification time in days from today", "Access time in days from today", 
            "GID numeric ID for the group owner of the file", "UID numeric ID for the owner of the file"
        ]
        
        with open(gpfspath, 'r') as file:
            for line in file:
                if max_rows and row_counter >= max_rows:
                    break
                values = line.strip().split(' ')
                self.gpfs_data.append(dict(zip(column_names, values)))
                row_counter += 1

    def files_per_user_gpfs(self):
        # THIS ONLY STREAMS 1,000 rows!!! change later!
        # Ensure self.gpfs_data is populated
        if not self.gpfs_data:
            print("No GPFS data to aggregate.")
            return
        
        # Aggregate file counts per user
        file_counts_per_user = {}
        for row in self.gpfs_data:
            uid = row.get("UID numeric ID for the owner of the file")
            if uid:
                file_counts_per_user[uid] = file_counts_per_user.get(uid, 0) + 1
                
        # # Sort and prepare for CDF plot
        # file_counts = list(file_counts_per_user.values())
        # file_counts.sort()
        # cumulative_counts = np.cumsum(file_counts)
        # cumulative_distribution = cumulative_counts / cumulative_counts[-1]
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.ecdf(file_counts_per_user.values(), drawstyle='steps-post')
        plt.xlabel('Number of Files Owned by a User')
        plt.ylabel('Fraction of Total Data')
        plt.title('Cumulative Distribution of Files per User')
        plt.grid(True)
        plt.show()

    def read_slurm(self, slurmpath):
        # set slurm_data to outputed pandas dataset
        self.slurm_data = pd.read_csv(slurmpath, delimiter='|', nrows=1e3)
        return self.slurm_data

    def AggSLURMDat(self, dat):
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
    
            # iterating through each cpu time for a given job id should only run once unless the job is an 
            for cpu_time in cpu_time_list:
                # masking data for a specific cpu time 
                # this SHOULD isolate a batch+agg job pair
                ajob = jdat[jdat["CPUTimeRAW"] == cpu_time]
    
                # if the job is user_258, should be the batch job
                batch_job = ajob[ajob["User"] == "user_258"]
    
                # if there is a unique id, should be the agg job
                ag_job = ajob[ajob["User"] != "user_258"]
    
                # # some weird edge cases I found 
                if len(ag_job["User"]) == 0:
                #     print("Weird Job",ajob["JobID"])
                #     print("No aggregate job")
                    continue
                if len(ag_job["User"]) == 2:
                #     print("Weird Job",ajob["JobID"])
                #     print("2 copies of aggregate job")
                    continue
                # # checks for any more unique edge cases in the slurm data
                assert len(ag_job["User"]) == 1, "New edge case discovered!"
    
                # appending MaxRSS data to agg job
                ag_job.loc[ag_job.index[0],"MaxRSS"] = batch_job["MaxRSS"].values[0]
                # appending new row to output directory
                out_df = pd.concat([out_df,ag_job])
                
            # set slurm_agg to outputed pandas aggregated slurm data
            self.slurm_agg = out_df
            return out_df
        
    # GPFS find users with many files method
    def UsersWithManyFiles(self, file_limit):
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
        users_with_many_files_df = pd.DataFrame()  # Ensure the DataFrame is always initialized

        # If gpfs_data is a DataFrame, use pandas functionality to aggregate
        if isinstance(self.gpfs_data, pd.DataFrame):
            file_count_per_user = self.gpfs_data.groupby("UID numeric ID for the owner of the file").size()
            users_with_many_files = file_count_per_user[file_count_per_user > file_limit]
            users_with_many_files_df = users_with_many_files.reset_index(name='Number of files')
            users_with_many_files_df.columns = ['UID numeric ID for the owner of the file', 'Number of files']
    
        # If gpfs_data is a list from streamed data, aggregate manually
        elif isinstance(self.gpfs_data, list):
            file_count_per_user = {}
            for row in self.gpfs_data:
                uid = row["UID numeric ID for the owner of the file"]
                file_count_per_user[uid] = file_count_per_user.get(uid, 0) + 1
    
            # Filter and create DataFrame for users exceeding file_limit
            users_with_many_files = {uid: count for uid, count in file_count_per_user.items() if count > file_limit}
            users_with_many_files_df = pd.DataFrame(list(users_with_many_files.items()), columns=['UID numeric ID for the owner of the file', 'Number of files'])
    
        else:
            print("ERROR: gpfs data was not defined or in an unrecognized format")
            return None
    
        # Sort by 'Number of files' in descending order if DataFrame is not empty
        if not users_with_many_files_df.empty:
            users_with_many_files_df.sort_values('Number of files', ascending=False, inplace=True)
    
        return users_with_many_files_df
    
        # # Sort by 'Number of files' in descending order
        # users_with_many_files_df.sort_values('Number of files', ascending=False, inplace=True)
        # return users_with_many_files_df
        
        # if isinstance(self.gpfs_data, pd.DataFrame):
             
        #     # Group by the user ID and count the number of files for each user
        #     file_count_per_user = self.gpfs_data.groupby("UID numeric ID for the owner of the file").size()
            
        #     # Filter users who have more files than the file_limit
        #     users_with_many_files = file_count_per_user[file_count_per_user > file_limit]
            
        #     # Convert the filtered Series object to a DataFrame
        #     users_with_many_files_df = users_with_many_files.reset_index()
        #     users_with_many_files_df.columns = ['UID numeric ID for the owner of the file', 'Number of files']
            
        #     # Sort by 'Number of files' in descending order
        #     users_with_many_files_df.sort_values('Number of files', ascending=False, inplace=True)
        #     return users_with_many_files_df
            
        # print("ERROR: gpfs data was not defined")
        # return None
        
    # slurm preprocessing method

    # slurm grouping users using KN-mean method

    # slurm identify_slurm_resource_underutilization method

    # slurm predict waltime method

    # slurm plots methods:
        


