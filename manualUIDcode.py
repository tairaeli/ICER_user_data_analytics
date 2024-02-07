import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# Initialize a Counter object to count the UID occurrences
uid_counts = Counter()

# Specify the column index for the UID in your dataset
uid_column_index = 8  # This is the correct index for the 9th column

# Open the file and read line by line
with open("/mnt/research/CMSE495-SS24-ICER/file_system_usage/gpfs-stats/inode-size-age-jan-23", "r") as file:
    reader = csv.reader(file, delimiter=' ')
    for row in reader:
        if row:  # Check if row is not empty
            uid = row[uid_column_index]  # Get the UID from the row
            uid_counts[uid] += 1  # Increment the count for this UID

print("Completed reading in data file")

# Now, uid_counts contains the number of files per UID
print("Number of users in the GPFS data:", len(uid_counts))

# Plotting
# Convert counts to a list of values for histogram
counts = list(uid_counts.values())

# Exclude outliers for this visualization
# Let's exclude any values above the 99th percentile
threshold = np.percentile(counts, 99)
filtered_counts = [count for count in counts if count <= threshold]

# Plotting with outliers removed
plt.figure(figsize=(10, 6))
plt.hist(filtered_counts, bins=50)  # Adjust the number of bins as needed
plt.title("Distribution of File Count per User (99th Percentile Cut-off)")
plt.xlabel("File Count")
plt.ylabel("Frequency")
plt.yscale('log')  # Use logarithmic scale for the y-axis to see the spread more clearly
plt.savefig('myfig_filtered.png', dpi=300)
print("UID count Dist viz without outliers is created")

# whole dataset not excluding outliers
# plt.hist(counts, bins=50)  # Adjust the number of bins as needed
# plt.title("Distribution of File Count per User")
# plt.xlabel("File Count")
# plt.ylabel("Frequency")
# plt.savefig('myfig.png', dpi=300)
# print("UID count Dist viz is created")
