# from dask.distributed import Client, progress
import dask.dataframe as dd
import gc
import pandas as pd
import time

# loading in data
print("Loading in data")
slurm = dd.read_csv("/mnt/research/CMSE495-SS24-ICER/slurm_usage/DID_FINAL_SLURM_OCT_2023.csv",delimiter="|", dtype={'MaxRSS': 'object'})
slurm = slurm.drop(columns=["Unnamed: 0","Unnamed: 0.1"])

# repartition data
slurm = slurm.repartition(partition_size="1 GB").persist()
print(f"Number of records: {len(slurm)}")

# finding batch data
batch_extern = slurm.loc[slurm.User=="user_258"]
batch = batch_extern[batch_extern.MaxRSS.notnull()]
batch = batch.loc[batch.Elapsed != '00:00:00']
bsub = batch.loc[:,["JobID","CPUTimeRAW","MaxRSS"]]

# creating list of jobs
joblist = bsub["JobID"].drop_duplicates()

# cleaning up 0 second jobs and batch/extern jobs
slurm_clean = slurm.loc[(slurm.Elapsed != '00:00:00') & (slurm.User!="user_258")]

start = time.time()
for i,j in enumerate(joblist):

    if i%20==0:
        gc.collect()

    print("Current Job:",str(j),"at",str(time.time()-start), flush=True)
    job = slurm_clean[slurm_clean["JobID"] == j]

    if len(job["JobID"]) == 1:
        slurm_clean["MaxRSS"] = slurm["MaxRSS"].mask(slurm_clean.JobID == j, bsub.loc[bsub["JobID"]==j,"MaxRSS"])
    else:
        for cputime in job["CPUTimeRAW"].drop_duplicates():

            # if there are multiple instances where the CPU time is the same, the memory usage is the same
            mem_used = bsub.loc[bsub["CPUTimeRAW"]==cputime,"MaxRSS"].reset_index()
            slurm_clean["MaxRSS"] = slurm["MaxRSS"].mask(cond=(slurm_clean["CPUTimeRAW"] == cputime), other=mem_used.loc[0,"MaxRSS"])

print("Saving data...")
slurm_clean.to_csv('/mnt/scratch/tairaeli/cmse_dat/part*.csv')
print("Job Complete!")

