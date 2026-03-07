import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 1. найти цены
prices = re.findall(r"\d+,\d+", text)

# 2. найти названия товаров
products = re.findall(r"\d+\.\n(.+)", text)

# 3. найти итог
total = re.search(r"ИТОГО:\n(\d+ \d+,\d+)", text)

# 4. найти дату
date = re.search(r"\d{2}\.\d{2}\.\d{4}", text)

# 5. найти время
time = re.search(r"\d{2}:\d{2}:\d{2}", text)

# 6. способ оплаты
if "Банковская карта" in text:
    payment = "Card"
else:
    payment = "Unknown"

# вывод
print("Products:", products)
print("Prices:", prices)

if total:
    print("Total:", total.group(1))

if date:
    print("Date:", date.group())

if time:
    print("Time:", time.group())

print("Payment method:", payment)