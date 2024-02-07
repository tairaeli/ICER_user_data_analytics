#!/bin/bash --login

#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=90G
#SBATCH --job-name UIDPlotFiltered



python /mnt/home/alkhali7/ICER-UserDataAnalytics/ICER_user_data_analytics/manualUIDcode.py
