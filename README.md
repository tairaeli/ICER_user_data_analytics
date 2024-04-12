# ICER_user_data_analytics

## Overview


The Institute for Cyber Enabled Research (ICER) provides critical infrastructure for computational academic research, catering to various disciplines. Our project aims to delve into how users engage with ICER's systems, assessing usage efficiency and exploring avenues for optimization. By enhancing our understanding of user behaviors and system interactions, we can guide ICER in optimizing resource allocation, potentially leading to significant cost savings.

The Institute for Cyber Enabled Research (ICER) in Michigan State University provides critical infrastructure for computational academic research, catering to various disciplines. Our project aims to delve into how users engage with ICER's systems, assessing usage efficiency and exploring avenues for optimization. By enhancing our understanding of user behaviors and system interactions, we can guide ICER in optimizing resource allocation, potentially leading to significant cost savings.


## Project Description

Leveraging the SLURM job database and GPFS file metadata, this project focuses on developing classification systems to categorize user workloads and disk utilization patterns. Employing unsupervised learning methods, we aim to analyze extensive datasets, thereby refining resource usage statistics and creating tools for system improvement. Our objectives include grouping similar users, identifying underutilization of resources, and predicting job queue times, among others.

Project plan video: [Project Plan Video](https://michiganstate.sharepoint.com/:v:/s/Section_SS24-CMSE-495-001-224214134-EL-32-A26-ICER/Efp8_UgZhPlOmn8TDa3YKNEB73NHpUl5yw95KQl-N27r3A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=MrIMiT)

### Research Questions
1. **Resource Utilization Patterns**: Can we identify which users are underutilizing or overutilizing system resources? 

2. **User Categorization and Prediction**: Can we classify users based on their system usage, including computing and disk usage, and monitor their resource utilization? 

3. **Queue Time Analysis**: Can we forecast the queue time for submitted jobs and identify key factors influencing this time? 

## Files

- For detailed installation instructions, please see our [INSTALL.md](INSTALL.md) file.

- For a step-by-step guide on how to use our software, please refer to our [demo.ipynb](demo.ipynb) file.
  
- For a step by step guide on how to produce our Waltime Prediction model, please refer to our [reproducibility](reproducibility) folder.


## Individual File Explanation

ICER_User_Dat:

  - DataAnalyzer.py is a class that houses all of our analysis functions.
  - models.py has the models for clusering users, identifying users with many files, and others.

Data:

  - PreprocessingData-SLURM-GPFS.ipynb holds our data preprocessing code, which can be applied to future data.
  - gpfs_sample_data.csv and slurm_sample_data.csv have a small subset of data with our preprocessing process applied to it.

Reproducability:

  - predict_walltime.ipynb is a reproducable result we've reached with regard to our predictive research question.

.gitignore:

  - Specifies things for github to not track, in our case is just jupyter notebook checkpoints and the data preprocessing directory.

ICER_package_demo.ipynb:

  - A demo of our analysis package in action, aggregating the data and identifying users with many files.

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

Acknowledgments

ICER for providing the infrastructure and datasets for this research.
All team members and contributors who have dedicated their time and expertise to this project.

Team Members & Contact Info:
- Shams Al khalidy        alkhali7@msu.edu
- Richard Arbury          arburyri@msu.edu
- Wesley Casaletto        casalet3@msu.edu
- Luke Kozlowski          kozlow86@msu.edu
- Elias Taira             tairaeli@msu.edu
