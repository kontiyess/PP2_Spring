from datetime import datetime, timedelta


# 1. Subtract five days from the current date.
current = datetime.now()
five_days = timedelta(days=5)
new_date = current - five_days

print(f"Current Date: {current}")
print(f"Date 5 days ago: {new_date}")
print()


# 2. Print yesterday, today, and tomorrow.
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(f"Yesterday: {yesterday}")
print(f"Today: {today}")
print(f"Tomorrow: {tomorrow}")
print()


# 3. Drop microseconds from the current datetime.
without_microseconds = today.replace(microsecond=0)

print(f"Current datetime without microseconds: {without_microseconds}")
print()


# 4. Calculate the difference between two dates in seconds.
difference = tomorrow - yesterday
seconds = difference.total_seconds()

print(f"Seconds between tomorrow and yesterday: {seconds}")