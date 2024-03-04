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
    df["underutilizerCPUS"] = df['ReqCPUS']-df['AllocCPUS'] 
    df["underutilizerNodes"] = df['ReqNodes']-df['NNodes']
    df['time_column']=pd.to_timedelta(df['Elapsed'])
    df['total_minutes']=df['time_column'].dt.total_seconds() / 60
    features2=['CPUTimeRAW','ReqCPUS','AllocCPUS','ReqNodes','NNodes','underutilizerCPUS','underutilizerNodes','total_minutes']
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
    percentages = {cluster: count / 1000000 * 100 for cluster, count in cluster_counts.items()}
    
    percentages = {cluster: count / 1000000 * 100 for cluster, count in cluster_counts.items()}
    
    table_data = pd.DataFrame(list(percentages.items()), columns=['Cluster Label', 'Percentage (%)'])
    
    return plot, df_pca, kmeans, table_data
    
    
    

def PredWalltimeSLURM(data):
    """
    Predicts how long a given job will sit in queue before running
    """
    return None
