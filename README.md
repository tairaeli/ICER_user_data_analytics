# ICER_user_data_analytics

## Overview


The Institute for Cyber Enabled Research (ICER) provides critical infrastructure for computational academic research, catering to various disciplines. Our project aims to delve into how users engage with ICER's systems, assessing usage efficiency and exploring avenues for optimization. By enhancing our understanding of user behaviors and system interactions, we can guide ICER in optimizing resource allocation, potentially leading to significant cost savings.

## Project Description

Leveraging the SLURM job database and GPFS file metadata, this project focuses on developing classification systems to categorize user workloads and disk utilization patterns. Employing unsupervised learning methods, we aim to analyze extensive datasets, thereby refining resource usage statistics and creating tools for system improvement. Our objectives include grouping similar users, identifying underutilization of resources, and predicting job queue times, among others.

- Project plan video: [Project Plan Video](https://michiganstate.sharepoint.com/:v:/s/Section_SS24-CMSE-495-001-224214134-EL-32-A26-ICER/Efp8_UgZhPlOmn8TDa3YKNEB73NHpUl5yw95KQl-N27r3A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=MrIMiT)

- Final Project MVP: [Final Project Video](https://michiganstate.sharepoint.com/:v:/r/sites/Section_SS24-CMSE-495-001-224214134-EL-32-A26-ICER/Shared%20Documents/ICER/project_deliverables/Video_Final_Project.mp4?csf=1&web=1&e=e3NKGu&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)

### Research Questions
1. **Resource Utilization Patterns**: Can we identify which users are underutilizing or overutilizing system resources? 

2. **User Categorization and Prediction**: Can we classify users based on their system usage, including computing and disk usage, and monitor their resource utilization? 

3. **Queue Time Analysis**: Can we forecast the queue time for submitted jobs and identify key factors influencing this time? 

## Files

- For detailed installation instructions, please see our [INSTALL.md](INSTALL.md) file.

- For a step-by-step guide on how to use our software, please refer to our [ICER_package_demo.ipynb](ICER_package_demo.ipynb) file.
  
- For a step by step guide on how to produce our Waltime Prediction model, please refer to our [reproducibility](reproducibility) folder.


## Individual File Explanation

ICER_package:
  - [DataAnalyzer.py](ICER_package/DataAnalyzer.py) is the file that includes the class that houses all of our analysis functions.
  - [tests](ICER_package/tests) directory includes 3 files for testing ICER_package and are the following:
    1. [test_gpfs.csv](ICER_package/tests/test_gpfs.csv) file includes 3 rows of fake GPFS data
    2. [test_slurm.csv](ICER_package/tests/test_slurm.csv) file includes 3 rows of fake slurm data
    3. [test_pytest.py](ICER_package/tests/test_pytest.py) file is a python script that can be ran to test ICER_pacakge directly.
    
ICER_package_demo.ipynb:

  - [ICER_package_demo](ICER_package_demo.ipynb) : a demo of our methods in the analysis package in action.

Reproducability:
  - [data_exploration](ICER_User_Dat/data_exploration) directory includes the notebooks, python, and sh files used used to explore, test and load the full slurm data file through different packages and methods.
  1. **RQ1**: How are users using resources inefficiently? 
  - [RQ1/FilesPerUser](reproducibility/RQ1/FilesPerUser) directory includes the job script file, python script file, log scaled Files Per User CDF plot, regular scaled Files Per User CDF plot, and a python notebook on a subset of the data for reproducibility with regard to plotting File Distribution in the GPFS system.
  - [RQ1/UsersWithManyFIlesGPFS.ipynb](reproducibility/RQ1/UsersWithManyFIlesGPFS.ipynb) is a reproducible function we've created to identify users in the GPFS system with many files based on a given threshold.
  2. **RQ2**: Are there any groups users fall into based on usage patterns? 
  - [RQ2/K-MeansClusterFinal](reproducibility/RQ2/K-MeansClusterFinal.ipynb)
Notebook takes data after preprocessing and isolates numeric features of the data set. It then using various Python packages, namely Skicit-Learn, it perform Principal Component analysis to reduce the dimensions of the SLURM data to dimensions of 2 and 3 and, performs and graphs KMeans clusters each respective dimension. Also performs a Decision Classification Tree to classify newly found Cluster labels. This helps show feature impact on each clusters label classification.
  - [RQ2/BIRCHCluster](reproducibility/RQ2/BIRCHCluster.ipynb)
Notebook takes data after preprocessing and isolates numeric features of the data set. It then using various Python packages, namely Skicit-Learn, it perform Principal Component analysis to reduce the dimensions of the SLURM data to dimensions of 2 and 3, performs and graphs BIRCH clusters to each respective dimension 
  - [RQ2/PCA_ElbowCurve Final](reproducibility/RQ2/PCA_ElbowCurve_Final.ipynb) 
Notebook takes data after preprocessing and isolates numeric features of the data set. It then using various Python packages, namely Skicit-Learn, it perform Principal Component analysis to reduce the dimensions of the SLURM data to dimensions. It then shows the explained variance of each Principle Component, the effect each of the original features had on each principle component and their normalized values. The notebook then uses the 3-dimensional data and initializes 14 k-means models. Each model has a different cluster value, each models inertia metric found. A plot of inertia vs. clusters is shown, which is used to pick final k-means cluster
  - [RQ2/Sample Statistics](reproducibility/RQ2/Sample_Statitics_Final.ipynb) 
Notebook takes data after preprocessing and isolates numeric features of the data set. It then finds and plots the CDFs of each numeric data feature. Also contains charts using “Group” feature of the data to show distribution of resources among unique groups in the SLURM data frame, as well as the the amount of time each group shows up in the data frame
  3. **RQ3**: Can we predict how long a job will remain in queue? 
  - [RQ3/RQ3-Predicting_Queutime.ipynb]([reproducibility/RQ3/RQ3-Predicting_Queutime.ipynb]) is a reproducable result we've reached with regard to our predictive research question.


.gitignore:
  - Specifies things for github to not track, in our case is just jupyter notebook checkpoints and the data preprocessing directory.

INSTALL.md:

  - Installation instructions for running our project.

LICENSE.txt:

  - Legal terms for using the work we did in the project.

environment.yml:

  - A file you can run to automatically install all the prerequisite packages for our project's code.

makefile:

  - the makefile for our project gives the command line instructions for setup.

## License

MIT License

Copyright (c) 2024 Shams Alkhalidy,Luke Kozlowski, Wesley Casaletto, Elias Taira, Richard Arbury

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

 - see the LICENSE.md file for details.

**Acknowledgments**

ICER for providing the infrastructure and datasets for this research.
All team members and contributors who have dedicated their time and expertise to this project.

**Team Members & Contact Info:**
- Shams Al khalidy        alkhali7@msu.edu
- Richard Arbury          arburyri@msu.edu
- Wesley Casaletto        casalet3@msu.edu
- Luke Kozlowski          kozlow86@msu.edu
- Elias Taira             tairaeli@msu.edu
