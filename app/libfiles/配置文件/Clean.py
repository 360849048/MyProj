import os

path = os.getcwd()
for root, dirs, files in os.walk(path):
    for file in files:
        if root != path:
            os.remove(os.path.join(root, file))