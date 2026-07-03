import os

# Specify the directory path
directory = "."  # Current directory

# Get the list of files and folders
contents = os.listdir(directory)

# Print the contents
print("Contents of the directory:")
for item in contents:
    print(item)