"""Testing Script for all methods within the Data analysis object"""

# testing packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from collections import Counter
import os

os.chdir('../')

# importing package
from DataAnalyzer import DataAnalyzer

# test initialization
def test_init():
    DataAnalyzer(None, None)

# package loading
def gpfs_load():
    dat = DataAnalyzer(gpfs_load = "./test_gpfs.csv")

def slurm_load():
    dat = DataAnalyzer(gpfs_load = "./test_gpfs.csv")

# function testing
def user_files():
    dat = DataAnalyzer(gpfs_load = "./test_gpfs.csv")

    dat.UsersWithManyFiles(file_limit = 2)

