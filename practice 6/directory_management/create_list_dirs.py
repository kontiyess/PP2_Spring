import os

# Create nested directories
base_dir = "test_dir"
sub_dir = os.path.join(base_dir, "sub_dir")

os.makedirs(sub_dir, exist_ok=True)
print("Directories created.")

# List files and folders
items = os.listdir(base_dir)

print("Contents of test_dir:")
for item in items:
    print(item)