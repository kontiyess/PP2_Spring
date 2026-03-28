# Create a file and write sample data

with open("sample.txt", "w") as file:
    file.write("Hello, this is a sample file.\n")
    file.write("This is the second line.\n")

print("File created and data written.")