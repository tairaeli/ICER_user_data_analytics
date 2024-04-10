# ICER_user_data_analytics

## Overview


The Institute for Cyber Enabled Research (ICER) provides critical infrastructure for computational academic research, catering to various disciplines. Our project aims to delve into how users engage with ICER's systems, assessing usage efficiency and exploring avenues for optimization. By enhancing our understanding of user behaviors and system interactions, we can guide ICER in optimizing resource allocation, potentially leading to significant cost savings.

The Institute for Cyber Enabled Research (ICER) in Michigan State University provides critical infrastructure for computational academic research, catering to various disciplines. Our project aims to delve into how users engage with ICER's systems, assessing usage efficiency and exploring avenues for optimization. By enhancing our understanding of user behaviors and system interactions, we can guide ICER in optimizing resource allocation, potentially leading to significant cost savings.


## Project Description

Leveraging the SLURM job database and GPFS file metadata, this project focuses on developing classification systems to categorize user workloads and disk utilization patterns. Employing unsupervised learning methods, we aim to analyze extensive datasets, thereby refining resource usage statistics and creating tools for system improvement. Our objectives include grouping similar users, identifying underutilization of resources, and predicting job queue times, among others.

Project plan video: [Project Plan Video](https://michiganstate.sharepoint.com/:v:/s/Section_SS24-CMSE-495-001-224214134-EL-32-A26-ICER/Efp8_UgZhPlOmn8TDa3YKNEB73NHpUl5yw95KQl-N27r3A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=MrIMiT)


## Files

- For detailed installation instructions, please see our [INSTALL.md](INSTALL.md) file.

- For a step-by-step guide on how to use our software, please refer to our [demo.ipynb](demo.ipynb) file.
  
- For a step by step guide on how to produce our Waltime Prediction model, please refer to our [reproducibility](reproducibility) folder.


## Individual File Explanation

ICER_User_Dat is a melting pot of actively-used files by the team members.

Data:

  PreprocessingData-SLURM-GPFS.ipynb holds our data preprocessing code, which can be applied to future data.
  gpfs_sample_data.csv and slurm_sample_data.csv have a small subset of data with our preprocessing process applied to it.

Reproducability:
  predict_walltime.ipynb is a reproducable result we've reached with regard to our predictive research question

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
