import wandb
import os

api = wandb.Api()
run = api.run("arturo-laurenzi-istituto-italiano-di-tecnologia/mjlab/66g9wxot")

import json


e = run._attrs['rawconfig']['_wandb']['e']
e = list(e.values())[0]
git = e['git']
commit = git['commit']
remote = git['remote']
args = e['args']
codePath = e['codePath']

print(f"Commit: {commit}")
print(f"Remote: {remote}")
print(f"Args: {args}")
print(f"Code Path: {codePath}")

# Download a file with given name
filename = "kyon_mjlab.diff"  # Change this to the file you want to download
download_dir = "."  # Directory to save the file

# Create download directory if it doesn't exist
os.makedirs(download_dir, exist_ok=True)

# # List all files in the run
# print("\nAvailable files:")
# for file in run.files():
#     print(f"  - {file.name}")

# Download the specific file
try:
    file = run.file(filename)
    download_path = os.path.join(download_dir, filename)
    file.download(root=download_dir, replace=True)
    print(f"\nFile '{filename}' downloaded to: {download_path}")
except Exception as e:
    print(f"\nError downloading file '{filename}': {e}")
    print("Make sure the filename exists in the run's files.")
