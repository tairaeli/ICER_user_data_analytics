#!/bin/bash --login
 
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=50G

pip install --user seaborn==0.11.0

python /mnt/home/alkhali7/ICER-UserDataAnalytics/ICER_user_data_analytics/FilePerUserCDF-job.py