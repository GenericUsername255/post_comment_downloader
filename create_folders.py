import os

# Specify the names of the directories to be created
dir_name1 = "input"
dir_name2 = "saved_data"

# Check if the directories exist. If not, create them.
if not os.path.exists(dir_name1):
    os.makedirs(dir_name1)

if not os.path.exists(dir_name2):
    os.makedirs(dir_name2)