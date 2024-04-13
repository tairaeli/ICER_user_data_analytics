import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
print(sns.__version__)

print('reading file start',flush=True)
file_path = "/mnt/research/CMSE495-SS24-ICER/file_system_usage/gpfs-stats/inode-size-age-jan-23"

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


print("Streaming START",flush=True)
# Stream through the file line by line
with open(file_path, 'r') as file:
    for line in file:
        values = line.strip().split(' ')
        
        # Associate values with column names
        row_data = dict(zip(column_names, values))
        
        uid = row_data["UID numeric ID for the owner of the file"]
        file_counts_per_user[uid] = file_counts_per_user.get(uid, 0) + 1

print('streaming COMPLETE',flush=True)

print('Plotting START')
# Plot the CDF
plt.figure(figsize=(10, 6))

sns.ecdfplot(list(file_counts_per_user.values()))

# Set the x-axis to a log scale with base 10
# plt.xscale('log', base=10)

# set labels and title
plt.xlabel('Number of Files Owned by a User')
plt.ylabel('Fraction of Total Data')
plt.title('Cumulative Distribution of Files per User')

plt.grid(True)
plt.savefig("Files_per_User_CDF.png")  # Save the plot as a PNG file
plt.close()  # Close the plot to free up memory


print('PLOT COMPLETE!!!!!',flush=True)
