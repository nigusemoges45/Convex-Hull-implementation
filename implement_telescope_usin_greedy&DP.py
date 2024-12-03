#!/usr/bin/env python
# coding: utf-8

# #  Import Neccessary Libraries
#  * **tracemalloc**:used to Tracks memory allocations of the scheduling algorithms.
# * **time**: Measures execution time during the execution of the scheduling algorithms.

# In[8]:


import tracemalloc
import time


# ### Telescope Scheduling Using greedy method

# In[9]:


# Implementing a simple greedy algorithm for telescope scheduling

def telescope_scheduler(tasks, telescope_time):
   
    # Sort tasks by priority (descending) and visibility window (ascending)
    tasks = sorted(tasks, key=lambda x: (-x['priority'], x['visibility_end'] - x['visibility_start']))
    
    schedule = []
    remaining_time = telescope_time

    # Select tasks while there is available time
    for task in tasks:
        if task['duration'] <= remaining_time:
            schedule.append(task)
            remaining_time -= task['duration']

    return schedule


# Example tasks with their attributes
tasks = [
    {"name": "Galaxy A", "priority": 5, "duration": 2, "visibility_start": 20, "visibility_end": 24},
    {"name": "Star B", "priority": 3, "duration": 3, "visibility_start": 18, "visibility_end": 22},
    {"name": "Nebula C", "priority": 4, "duration": 1, "visibility_start": 19, "visibility_end": 21},
    {"name": "Exoplanet D", "priority": 2, "duration": 2, "visibility_start": 21, "visibility_end": 23},
    {"name": "Cluster E", "priority": 1, "duration": 4, "visibility_start": 17, "visibility_end": 20}
]

# Total telescope time available
telescope_time = 5

# Run the greedy scheduler
schedule = telescope_scheduler(tasks, telescope_time)
schedule


# ### Telescope scheduling algorithm using dynamic programming

# In[10]:


def telescope_scheduler_dp(tasks, telescope_time):
   
    n = len(tasks)

    # DP table: dp[i][w] stores the maximum priority achievable with the first i tasks and w available time
    dp = [[0] * (telescope_time + 1) for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for w in range(telescope_time + 1):
            if tasks[i - 1]['duration'] <= w:
                # Include the current task or skip it
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - tasks[i - 1]['duration']] + tasks[i - 1]['priority'])
            else:
                # Skip the current task
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find the selected tasks
    selected_tasks = []
    w = telescope_time
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_tasks.append(tasks[i - 1])
            w -= tasks[i - 1]['duration']

    # Return the maximum priority and the selected tasks
    max_priority = dp[n][telescope_time]
    return max_priority, selected_tasks


# Example tasks
tasks = [
    {"name": "Galaxy A", "priority": 5, "duration": 2, "visibility_start": 20, "visibility_end": 24},
    {"name": "Star B", "priority": 3, "duration": 3, "visibility_start": 18, "visibility_end": 22},
    {"name": "Nebula C", "priority": 4, "duration": 1, "visibility_start": 19, "visibility_end": 21},
    {"name": "Exoplanet D", "priority": 2, "duration": 2, "visibility_start": 21, "visibility_end": 23},
    {"name": "Cluster E", "priority": 1, "duration": 4, "visibility_start": 17, "visibility_end": 20}
]

# Total telescope time available
telescope_time = 5

# Run the DP scheduler
max_priority, selected_tasks = telescope_scheduler_dp(tasks, telescope_time)
max_priority, selected_tasks


# #### running time and memory consumption of greedy method and dynamic programming

# In[11]:


# Measure time and memory for the greedy algorithm
tracemalloc.start()
start_greedy = time.time()
greedy_schedule = telescope_scheduler(tasks, telescope_time)
end_greedy = time.time()
current_greedy, peak_greedy = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Measure time and memory for the dynamic programming algorithm
tracemalloc.start()
start_dp = time.time()
dp_max_priority, dp_schedule = telescope_scheduler_dp(tasks, telescope_time)
end_dp = time.time()
current_dp, peak_dp = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Results
{
    "Greedy": {
        "Time (seconds)": end_greedy - start_greedy,
        "Current Memory (bytes)": current_greedy,
        "Peak Memory (bytes)": peak_greedy,
    },
    "Dynamic Programming": {
        "Time (seconds)": end_dp - start_dp,
        "Current Memory (bytes)": current_dp,
        "Peak Memory (bytes)": peak_dp,
    }
}


# # Conclusions
# 
# - **Greedy Algorithm:**  
#   Focuses on scheduling tasks as they appear feasible, potentially missing better schedules (e.g., it may schedule lower-priority tasks early and exclude later, higher-priority ones).
# 
# - **Dynamic Programming Algorithm:**  
#   Evaluates all combinations to ensure the maximum possible tasks are scheduled. It may take longer to execute but will always produce the best schedule according to the defined criteria.
