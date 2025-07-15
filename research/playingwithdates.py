from datetime import date, datetime

print(date.today())
today = date.today()
# in the example below: subtracting dates
graduation_day = date(2026,11,11)
print(graduation_day)
days_left = abs(graduation_day - today)
print(days_left)


project_start_date = "2025-07-15"
projtect_end_date =  "2025-07-22"

# converting strings to dates
# work with the datetime class
# the datetime.strptime method takes 2 arguments: string for the date and the format string|format code

project_start_date = datetime.strptime(project_start_date, "%Y-%m-%d")
project_end_date = datetime.strptime(projtect_end_date, "%Y-%m-%d")

print(f"type of project_start_date : {type(project_start_date)} and project_start_date: {project_start_date}")



project_1_start_date="2025-07-15"
project_2_start_date="2025-08-15"
date_format="%Y-%m-%d"
project_2_start_date=datetime.strptime(project_2_start_date, date_format)

todays_date = date.today()
print(f"project_2_start_date.date: {project_2_start_date.date()}")
todays_date.month
todays_date.day

future_project_date = project_2_start_date.date() - todays_date
print(future_project_date)
print(future_project_date.days)
print(type(future_project_date.days))
# print(type(future_project_days_left))
# future_project_days_left = str(future_project_days_left)
# print(type(future_project_days_left))

# future_project_days_left = int(future_project_days_left)
if future_project_date.days > 0:
    print("project is in the future")
else:
    print("Project in the future")













"""
when working with date we use ``datetime`` module
``from datetime import *``
In the example below will show you how to perform subtraction
```py
from datetime import date
# get todays date
today = date.today() # today is a method of the class date
grad_day = date(2025, 07, 29) # date(yy,mm,hh)
time_left = abs(grad_day - today)
print(time_left)
```

### **Converting strings to datetime object**
To convert a string to a `datetime` object in Python, you can use the `strptime()` method from the `datetime` module. This method takes two arguments: the date string (`date_string`) and the format string (`format_code`) that specifies how the date is structured 

For example:

```python
from datetime import datetime

date_string = "2025-06-15 14:30:00"
format_code = "%Y-%m-%d %H:%M:%S"

parsed_date = datetime.strptime(date_string, format_code)
print(parsed_date)  # Outputs: 2025-06-15 14:30:00
```

In this example:
- `%Y` matches a four-digit year,
- `%m` matches a two-digit month,
- `%d` matches a two-digit day of the month,
- `%H` matches the hour (in 24-hour format),
- `%M` matches the minute,
- `%S` matches the second 

If the string doesn't match the format exactly, a `ValueError` will be raised. Therefore, it's a good idea to ensure that the format string precisely matches the input string's structure 

For more complex date strings, such as `"Jun 1 2005 1:33PM"`, the format string would be:

```python
date_string = "Jun 1 2005 1:33PM"
format_code = "%b %d %Y %I:%M%p"

parsed_date = datetime.strptime(date_string, format_code)
print(parsed_date)  # Outputs: 2005-06-01 13:33:00
```

Here:
- `%b` matches the abbreviated month name,
- `%d` matches the day of the month,
- `%Y` matches the four-digit year,
- `%I` matches the hour (in 12-hour format),
- `%M` matches the minute,
- `%p` matches the AM/PM indicator 

You can extract just the date part using `.date()` or the time part using `.time()` from the resulting `datetime` object if needed 
"""