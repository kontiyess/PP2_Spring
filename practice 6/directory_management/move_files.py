import shutil
import os

# Ensure directory exists
os.makedirs("test_dir", exist_ok=True)

# Create a file to move
with open("move_me.txt", "w") as f:
    f.write("Move this file.")

# Move file
shutil.move("move_me.txt", "test_dir/move_me.txt")
print("File moved to test_dir.")