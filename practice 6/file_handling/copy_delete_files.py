import shutil
import os

# Copy file
shutil.copy("sample.txt", "sample_copy.txt")
print("File copied.")

# Delete copied file
if os.path.exists("sample_copy.txt"):
    os.remove("sample_copy.txt")
    print("Copied file deleted.")