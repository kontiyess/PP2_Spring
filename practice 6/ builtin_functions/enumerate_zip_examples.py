# Example data
items = ["item1", "item2", "item3"]
values = [10, 20, 30]

# enumerate()
for i, item in enumerate(items):
    print(f"{i}: {item}")

# zip()
for item, value in zip(items, values):
    print(f"{item} -> {value}")