import pandas as pd
import random
from datetime import datetime, timedelta, date
import numpy as np
import openpyxl

"""
This set of functions allows to quickly generate test datasets 
"""

def dataset_generator(columns, column_types, num_rows):
    dataset = {}
    for col, col_type in zip(columns, column_types):
        dataset[col] = randomizer(col_type, num_rows)
    return pd.DataFrame(dataset)


def create_dataframe(columns):
    dataset = pd.DataFrame(columns=columns)
    return dataset


def randomizer(column_type, num_rows, *args):
    if column_type == 'int64':
        if len(args) >= 2:
            minimum_value = args[0]
            maximum_value = args[1]
        else:
            minimum_value = 1
            maximum_value = 15

        if len(args) == 3:
            step = args[2]
        else:
            step = 1

        return _generate_integer(num_rows, minimum_value, maximum_value, step)

    elif column_type == 'object':
        if len(args) < 1:
            raise ValueError("At least one string value should be provided.")
        elif len(args) == 1:
            return _generate_string(num_rows, args[0])
        else:
            return _generate_string(num_rows, random.choice(args))

    elif column_type == 'datetime64[ns]':
        if len(args) >= 2:
            start_date = args[0]
            end_date = args[1]
        else:
            start_date = '2023-06-14'
            end_date = '2023-06-26'

        return _generate_date(num_rows, start_date, end_date)

    else:
        raise ValueError("Invalid column type provided.")


def _generate_integer(num_rows, minimum_value=1, maximum_value=15, step=1):
    return [random.randrange(minimum_value, maximum_value + 1, step) for _ in range(num_rows)]


def _generate_string(num_rows, *values):
    return [random.choice(values) for _ in range(num_rows)]


def _generate_date(num_rows, start_date, end_date):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    delta = (end_datetime - start_datetime).days

    if num_rows <= delta:
        dates = [start_datetime + timedelta(days=i) for i in range(num_rows)]
    else:
        dates = [start_datetime + timedelta(days=i) for i in range(delta)]
        dates.extend([np.nan] * (num_rows - delta))

    return dates


# Use case
# Set up prerequisites
columns = ['category', 'amount', 'sale_date']
column_types = ['object', 'int64', 'datetime64[ns]']

# Generate an empty dataset with 1000 rows
# dataset = dataset_generator(columns, column_types, 1000)

# Create empty dataset
dataset = create_dataframe(columns=columns)

# Day count
days = 700

min_date = date(year=2021, month=6, day=1)
min_date_format = min_date.strftime("%Y-%m-%d")
max_date = min_date + timedelta(days=days)
max_date_format = max_date.strftime("%Y-%m-%d")
print(f'The max date is {max_date}')

# min_date = '2023-01-01'
# max_date = '2023-06-26'

# Fill the dataset with values using the randomizer function
dataset['category'] = randomizer('object', days, 'milk')
dataset['amount'] = randomizer('int64', days, 11, 29, 1)
dataset['sale_date'] = randomizer('datetime64[ns]', days, min_date_format, max_date_format)
dataset['id'] = dataset.index

# Check our dataset and save it in appropriate format
print(dataset.info())
dataset.to_excel('categories.xlsx', index=False)
