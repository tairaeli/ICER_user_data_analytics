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
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

class DataAnalyzer:

    
    def __init__(self, gpfspath='', slurmpath='',gpfs_nrows=1000, slurm_nrows=1000):
        # initialize data to None
        self.gpfs_data = None
        self.slurm_data = None
        # initialize paths
        self.gpfspath = gpfspath
        self.slurmpath = slurmpath
        
        
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
        # read gpfs data
        self.gpfs_data = pd.read_csv(self.gpfspath, header=None, names=column_names, delimiter=' ', nrows=nrows)
        return self.gpfs_data

    def read_slurm(self, slurmpath, nrows):
        # read data using pandas
        self.slurm_data = pd.read_csv(slurmpath, delimiter=',', nrows=nrows)
        
        # Preprocessing:
        self.slurm_data = self.slurm_data.drop(columns=['Unnamed: 0'])

        # Filter out rows where 'State' is "Cancelled" or Unknown
        self.slurm_data = self.slurm_data[self.slurm_data['State'] != 'Cancelled']
        self.slurm_data = self.slurm_data[self.slurm_data['Start']!= 'Unknown']
        
        self.slurm_data['Submit'] = pd.to_datetime(self.slurm_data['Submit'])
        self.slurm_data['Start'] = pd.to_datetime(self.slurm_data['Start'])

        # drop na used memory from MaxRSS column
        self.slurm_data = self.slurm_data.dropna(subset=['MaxRSS'])

        # Feature Engineering:

        # convert ReqMem to a uniform measurement ('M' for MB and 'G' for GB and 'K' for KB)
        def convert_memory(mem_str):
            '''
            Convert memory units to MegaBytes unit float.
            '''
            if type(mem_str) == float:
                return 0
            if mem_str.endswith('M'):
                return float(mem_str[:-1]) # remove 'M' and convert to float
            elif mem_str.endswith('K'):
                return float(mem_str[:-1]) / 1000
            elif mem_str.endswith('G'):
                return float(mem_str[:-1]) * 1e3  # convert MB to KB
            elif mem_str.endswith('T'):
                return float(mem_str[:-1]) * 1e6 # convert MB to T

        # create new columns in the dataset that have uniform memory units (ReqMem and MaxRSS)
        self.slurm_data['ReqMem_MB'] = self.slurm_data['ReqMem'].apply(convert_memory)
        self.slurm_data['MaxRSS_MB'] = self.slurm_data['MaxRSS'].apply(convert_memory)

        # Function to parse time data columns: TimeLimit and Elapsed
        def parse_time_string(time_str):
            """Convert a time string into a timedelta object."""
            days = 0
            if type(time_str) == float:
                return timedelta(days=0, hours=0, minutes=0, seconds=0)
            if '-' in time_str:
                days, time_str = time_str.split('-')
                days = int(days)
        
            parts = time_str.split(':')
            hours, minutes, seconds = map(int, parts) if len(parts) == 3 else (int(parts[0]), int(parts[1]), 0)
            return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        
        # Convert Timelimit and Elapsed to timedelta type
        self.slurm_data['Timelimit'] = self.slurm_data['Timelimit'].apply(parse_time_string)
        self.slurm_data['Elapsed'] = self.slurm_data['Elapsed'].apply(parse_time_string)

        
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
        # plt.savefig("Files_per_User_CDF.png")  # Save the plot as a PNG file
        plt.show()  # Close the plot to free up memory



    # slurm predict waltime method
    def predict_waltime(self):
        '''
        This method uses a Random Forest Model to predict Queuetime in Minutes
        params:
        returns: RMSE and r^2 scores and a scatter plot of Predicted vs. Actual Queutime
        '''
        # Calculate Queutime in minutes and create a new column for it
        self.slurm_data["QueueTime (Minutes)"] = (self.slurm_data['Start']- self.slurm_data['Submit']).dt.total_seconds()/60
        # Convert Timelimit from timedelta type to Minutes float and create a new column
        self.slurm_data['Timelimit (Minutes)'] = self.slurm_data['Timelimit'].dt.total_seconds()/60

        # Random Forest Model
        # prepare the dataset for training
        X = self.slurm_data[['ReqCPUS','ReqMem_MB','ReqNodes','Timelimit (Minutes)']]
        y = self.slurm_data['QueueTime (Minutes)']
        
        # splitting dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.2, random_state=42)
        
        # standarize features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train a random Forest Regressor 
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # predict on the test set
        y_pred = model.predict(X_test_scaled)
        
        
        # Calculate R2 score for accuracy
        r2 = r2_score(y_test, y_pred)
        print("R2 Score:", r2)
        
        # Calculate RMSE
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print("Root Mean Squared Error:", rmse)

        # Identity line for reference (where perfect predictions would lie)
        array = np.arange(0, np.max([y_test.max(), y_pred.max()])+1)  # Adjust the range based on your data
        plt.plot(array, array, 'r--', label='Perfect predictions')  # Red dashed line for reference
        
        # Scatter plot of Predicted vs. Actual values
        plt.scatter(y_pred, y_test, alpha=0.5)  # Alpha for marker opacity
        
        # Adding title and axis labels
        plt.title('Predicted vs. Actual QueueTime Random Forest Model', fontsize=20)
        plt.xlabel('Predicted QueueTime (Minutes)', fontsize=15)
        plt.ylabel('Actual QueueTime (Minutes)', fontsize=15)
        
        # Adding a legend
        plt.legend()
        
        # Show grid
        plt.grid(True)
        
        # Display the plot
        plt.show()


    # slurm Find Underutilizer method
    def find_underutilizer(self, time_threshold, cpu_threshold, nodes_threshold, memory_threshold,
                           min_time_requested, min_cpu_requested, min_nodes_requested, min_memory_requested):
        """
        Identifies users who are requesting more resources than they use based on fractional thresholds,
        including memory, and filters out jobs where the requested resources do not meet specified minimums.
        
        :param time_threshold: Fractional threshold for underutilized time.
        :param cpu_threshold: Fractional threshold for underutilized CPU.
        :param nodes_threshold: Fractional threshold for underutilized nodes.
        :param memory_threshold: Fractional threshold for underutilized memory.
        :param min_time_requested: Minimum hours requested for a job to be considered.
        :param min_cpu_requested: Minimum CPU count requested for a job to be considered.
        :param min_nodes_requested: Minimum node count requested for a job to be considered.
        :param min_memory_requested: Minimum memory (in GB or other consistent unit) requested for a job to be considered.
        :return: DataFrame of underutilizing users and their job details.
        """
        
        data = self.slurm_data  # Use the instance data

        # Calculate fractional underutilization
        data['FractionalUnderutilizedTime'] = 1 - (data['Elapsed'] / data['Timelimit'])
        data['FractionalUnderutilizedCPU'] = 1 - (data['AllocCPUS'] / data['ReqCPUS'])
        data['FractionalUnderutilizedNodes'] = 1 - (data['NNodes'] / data['ReqNodes'])
        data['FractionalUnderutilizedMemory'] = 1 - (data['MaxRSS_MB'] / data['ReqMem_MB'])

        # Filter based on the specific fractional thresholds and the minimum resource requests
        underutilized = data[
            (data['Timelimit'].dt.total_seconds() / 3600 > min_time_requested) & 
            (data['ReqCPUS'] > min_cpu_requested) &
            (data['ReqNodes'] > min_nodes_requested) &
            (data['ReqMem_MB'] > min_memory_requested) &
            ((data['FractionalUnderutilizedTime'] > time_threshold) |
             (data['FractionalUnderutilizedCPU'] > cpu_threshold) |
             (data['FractionalUnderutilizedNodes'] > nodes_threshold) |
             (data['FractionalUnderutilizedMemory'] > memory_threshold))
        ]

        return underutilized[['User', 'JobID', 'Group', 'State', 'Account', 'AllocCPUS', 'NNodes',
                              'MaxRSS_MB','Elapsed', 'FractionalUnderutilizedCPU', 'FractionalUnderutilizedNodes', 
                              'FractionalUnderutilizedMemory', 'FractionalUnderutilizedTime']]


    # slurm grouping users using KN-mean method

    # slurm plots methods:
        # cdf plot

        # Heatmap
        


