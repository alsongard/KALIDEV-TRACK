from datetime import date
from datetime import datetime


# year_birth=input("Enter year of birth: ")
# month_birth=input("Enter month of birth:")
# day_birth = input("Enter day of birth")

# get current date
# today_dates = datetime.now()

# print(f'Todays date is :{today_dates}')

# print(f"Year of birth: {year_birth}-{month_birth}-{day_birth}")

# # work with year_brith
# birth_date =  year_birth +"-"+ month_birth +"-"+ day_birth
# print(f'birth_date: {birth_date}')
# birth_year = datetime.strptime(birth_date, '%Y-%m-%d')
# print(f'birth_year {birth_year}')

# age = today_dates.year - birth_year.year
# print(f'Age: {age}')


# trial 2 
# subtract dates on automatic
future_date = '2025-12-12'

# convert future_date to time
date_future = datetime.strptime(future_date, "%Y-%m-%d")


# perform subract
print(f'Current date using datetime: {datetime.now().date()}')

get_difference =datetime.now().date() - date_future.date() # subtraction is happening: current date to future date
print(get_difference) # this results in a negative value if the future is forward


if date_future.date() < datetime.now().date(): # if future date is less current date: means it's past
    print('IN the past')
else:
    print("IN the future")