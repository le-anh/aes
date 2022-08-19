import os

path_result = "./result/"
path_key = "./result/key/"

# Remove all in result directory
try:
    for file_name in os.listdir(path_result):
        file = path_result + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)
except:
    print("The system cannot find the file specified")

# Remove all in result/key directory
try:
    for file_name in os.listdir(path_key):
        file = path_key + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)
except:
    print("The system cannot find the file specified")

