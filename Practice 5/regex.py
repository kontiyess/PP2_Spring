import re

# 1. 'a' followed by zero or more 'b'
def task1(s):
    return bool(re.fullmatch(r"ab*", s))


# 2. 'a' followed by two to three 'b'
def task2(s):
    return bool(re.fullmatch(r"ab{2,3}", s))


# 3. lowercase letters joined with underscore
def task3(s):
    return bool(re.fullmatch(r"[a-z]+_[a-z]+", s))


# 4. one uppercase letter followed by lowercase letters
def task4(s):
    return bool(re.fullmatch(r"[A-Z][a-z]+", s))


# 5. 'a' followed by anything, ending in 'b'
def task5(s):
    return bool(re.fullmatch(r"a.*b", s))


# 6. replace space, comma, or dot with colon
def task6(s):
    return re.sub(r"[ ,\.]", ":", s)


# 7. snake_case → camelCase
def task7(s):
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


# 8. split string at uppercase letters
def task8(s):
    return re.findall(r"[A-Z][^A-Z]*", s)


# 9. insert spaces before capital letters
def task9(s):
    return re.sub(r"([A-Z])", r" \1", s).strip()


# 10. camelCase → snake_case
def task10(s):
    return re.sub(r"([A-Z])", r"_\1", s).lower()


# Examples
print(task1("abbb"))
print(task2("abb"))
print(task3("hello_world"))
print(task4("Hello"))
print(task5("axyzb"))
print(task6("hello world,python.code"))
print(task7("hello_world_test"))
print(task8("HelloWorldPython"))
print(task9("HelloWorldPython"))
print(task10("helloWorldPython"))