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
    def __init__(self, gpfspath='', slurmpath='',gpfs_nrows=1000, slurm_nrows=1000):
        # initialize data to None
        self.gpfs_data = None
        self.slurm_data = None
        # initialize paths
        self.gpfspath = gpfspath
        self.slurmpath = slurmpath
        
        # printing each data file path
        print('gpfs path=',gpfspath)
        print('slurm path=',slurmpath)
        
        # direct each data path to read_gpfs or read_slurm depending on path
        if gpfspath != '':
                self.read_gpfs(gpfspath,gpfs_nrows)
            
        if slurmpath != '':
            self.read_slurm(slurmpath, slurm_nrows)
        
        
    def read_gpfs(self, gpfspath , nrows):
        column_names = ["Inode (file unique ID)",
                        "KB Allocated",
                        "File Size",
                        "Creation Time in days from today",
                        "Change Time in days from today",
                        "Modification time in days from today",
                        "Acces time in days from today",
                        "GID numeric ID for the group owner of the file",
                        "UID numeric ID for the owner of the file"]
        # set gpfs_data to outputed pandas dataset;;;; 100,000 rows only 
        self.gpfs_data = pd.read_csv(self.gpfspath, header=None, names=column_names, delimiter=' ', nrows=nrows)
        return self.gpfs_data


    def read_slurm(self, slurmpath, nrows):
        # set slurm_data to outputed pandas dataset
        self.slurm_data = pd.read_csv(slurmpath, delimiter='|', nrows=nrows)
        return self.slurm_data

        
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
        else:
            raise ValueError("ERROR: gpfs data was not defined or in an unrecognized format")
    
        # Sort by 'Number of files' in descending order if DataFrame is not empty
        if not users_with_many_files_df.empty:
            users_with_many_files_df.sort_values('Number of files', ascending=False, inplace=True)
        return users_with_many_files_df

    # GPFS Files Per User log10 CDF plot
    def files_per_user_gpfs(self,full_dataset=False):
        # Explicit column names, since the data has no header
        column_names = [
            "Inode (file unique ID)",
            "KB Allocated",
            "File Size",
            "Creation Time in days from today",
            "Change Time in days from today",
            "Modification time in days from today",
            "Access time in days from today",
            "GID numeric ID for the group owner of the file",
            "UID numeric ID for the owner of the file"
        ]
        
        # Initialize a dictionary to count files per UID
        file_counts_per_user = {}
        if full_dataset==False:
            row_counter = 0  # Initialize a counter for the rows
            # Stream through the file line by line
            with open(self.gpfspath, 'r') as file:
                for line in file:
                    if row_counter < 1000:  # Process only the first 1000 lines
                        values = line.strip().split(' ')
                        
                        # Associate values with column names
                        row_data = dict(zip(column_names, values))
                        # extract the user id
                        uid = row_data["UID numeric ID for the owner of the file"]
                        file_counts_per_user[uid] = file_counts_per_user.get(uid, 0) + 1    # increase count of files for user
                        row_counter+=1
                    else:
                        break
        elif full_dataset==True:
            # Stream through the file line by line
            with open(self.gpfspath, 'r') as file:
                for line in file:
                    values = line.strip().split(' ')
                    # Associate values with column names
                    row_data = dict(zip(column_names, values))
                    # extract the user id
                    uid = row_data["UID numeric ID for the owner of the file"]
                    file_counts_per_user[uid] = file_counts_per_user.get(uid, 0) + 1    # increase count of files for user
        
        # Plot the CDF
        plt.figure(figsize=(10, 6))
        sns.ecdfplot(list(file_counts_per_user.values()))
        
        # Set the x-axis to a log scale with base 10
        plt.xscale('log', base=10)
        
        # set labels and title
        plt.xlabel('Number of Files Owned by a User')
        plt.ylabel('Fraction of Total Data')
        plt.title('Cumulative Distribution of Files per User')
        
        plt.grid(True)
        plt.savefig("Files_per_User_CDF.png")  # Save the plot as a PNG file
        plt.close()  # Close the plot to free up memory


    # slurm preprocessing method

    # slurm grouping users using KN-mean method

    # slurm identify_slurm_resource_underutilization method

    # slurm predict waltime method

    # slurm plots methods:
        


