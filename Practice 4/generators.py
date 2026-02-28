# 1. Create a generator that generates the squares of numbers up to N.
def squares(n):
    for i in range(n + 1):
        yield i ** 2


# 2. Create a generator that prints even numbers between 0 and N.
def evens(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


# 3. Create a generator that yields numbers divisible by both 3 and 4 between 0 and N.
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


# 4. Create a generator that yields the square of numbers from A to B.
def squares_from_a_to_b(a, b):
    for i in range(a, b + 1):
        yield i ** 2


# 5. Create a generator that returns all numbers from N down to 0.
def countdown(n):
    for i in range(n, -1, -1):
        yield i


# 1
ans = squares(int(input("Input number: ")))
for i in ans:
    print(i, end=" ")
print()

# 2
ans = evens(int(input("Input number: ")))
for i in ans:
    print(i, end=" ")
print()

# 3
ans = divisible_by_3_and_4(int(input("Input number: ")))
for i in ans:
    print(i, end=" ")
print()

# 4
ans = squares_from_a_to_b(int(input("Input first number: ")), int(input("Input second number: ")))
for i in ans:
    print(i, end=" ")
print()

# 5
ans = countdown(int(input("Input number: ")))
for i in ans:
    print(i, end=" ")