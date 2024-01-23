# Research questions

1. User data questions
  - What amount/fraction of ICER's data has not been used as a function of time?  (I.e., what fraction of data hasn't been used in any way in a month, a year, etc.)
  - Are there common patterns in terms of users' data utilization?  (Considering file size, creation time, change/modification time, and access times.)
  - Are there any users or groups who are outliers in terms of their data utilization patterns?

  
2. User computing utilization - data analysis questions
  - What are the common types of workloads run on the HPC (ex. Computational jobs needing large memory, GPUs, shared network jobs, etc.)? 
  -  Are there particular resources that are over-subscribed or under-subscribed, as measured by queue time or other metrics? 
  - How much system resources (memory, number of course, wall-clock time) are used for each type of job?  (I'm looking for job categorization here - are there patterns?)
  - How many jobs fit on a single node vs. require multiple nodes? 
  - Are their jobs that request significantly more resources than are used?  (In other words, are there jobs that are significantly underutilizing resources?)
  - (related to previous question) Are there users who are outliers in terms of underutilizing resources compared to their requests?



3. User computing utilization - prediction questions
  - Can we predict which users are underutilizing/overutilizing system resources?
  - Can we predict roughly how long a submitted job will sit in the queue?  (And what the most important characteristics of a job are that make it sit in the queue?) 
  - Can we predict how much over-estimating resource needs (compared to utilization) will impact queue time?
  - Do users have predictable utilization patterns?  i.e., can we reliably predict which users are consistently running jobs vs. those who have more bursty patterns?  How does it correlate to time of year/academic calendar?

4. User modeling
  - Can we categorize users into types based on their system usage, including both computing resources and disk usage?  Can we predict who will underutilize resources, or consume lots of resources?
 
