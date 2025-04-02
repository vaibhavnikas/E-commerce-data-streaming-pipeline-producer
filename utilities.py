import datetime
import random


def get_next_date(current_date=None, days_to_add=1):
    """
    Gets the next date, or a date 'days_to_add' days in the future.
    Args:
        current_date: datetime.date object (optional). If None, uses today's date.
        days_to_add: Integer, number of days to add (default is 1).
    Returns:
        datetime.date object representing the next date.
    """
    if current_date is None:
        current_date = datetime.date(2020, 1, 1)

    next_date = current_date + datetime.timedelta(days=days_to_add)
    return next_date

def get_int(str):
    return int(str)

def get_current_date():
    """
    Returns last recorded current_date from the last ecommerce_transaction_producer.py run
    """
    current_date = datetime.date(2020, 1, 1)
    try:
        with open('last/current_date.txt', 'r') as f:
            date = f.readline().split('-')
            date = tuple(map(get_int, date))
            current_date = datetime.date(*date)
    except FileNotFoundError:
        with open('last/current_date.txt', 'w') as f:
            f.write(str(current_date))
    return current_date

def save_current_date(current_date):
    """
    Saves last recorded current_date from the current ecommerce_transaction_producer.py run.

    Saved current_date can be used in the next run.
    """
    try:
        with open('last/current_date.txt', 'w') as f:
            f.write(str(current_date))
    except Exception as e:
        print(f"An unexpected error occured: {e}")

def get_last_transaction_id():
    """
    Returns last recorded transaction_id from the last ecommerce_transaction_producer.py run
    """
    last_transaction_id = -1
    try:
        with open('last/transaction_id.txt', 'r') as f:
            last_transaction_id = f.readline()
    except FileNotFoundError:
        with open('last/transaction_id.txt', 'w') as f:
            last_transaction_id = '0'
            f.write(last_transaction_id)
    return int(last_transaction_id)
    
def save_last_transaction_id(transaction_id):
    """
    Saves last recorded transaction_id from the current ecommerce_transaction_producer.py run.

    Saved transaction_id can be used in the next run.
    """
    try:
        with open('last/transaction_id.txt', 'w') as f:
            f.write(str(transaction_id))
    except Exception as e:
        print(f"An unexpected error occured: {e}")

def remove_new_line_char(str):
    return str.replace("\n", '')

def get_csv_data(filepath:str):
    """
    Returns data in a csv file as a list of dictionaries.

    Args: filepath

    Returns: list[dict]
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
        lines = list(map(remove_new_line_char, lines))

        keys = lines[0].split(',')
        records = lines[1:]

    formatted_records = []
    for record in records:
        formatted_record = {}
        values = record.split(',')

        for key, value in zip(keys, values):
            formatted_record[key] = value
        formatted_records.append(formatted_record)
    return formatted_records

def get_random_integers(n:int, min:int, max:int):
    """Returns n unique random integers between min and max value (both inclusive)"""
    if n > (max - min + 1):
        raise ValueError("Not possible to generate n unique integers between min and max")

    random_integers = []
    while n:
        x = random.randint(min, max)
        if x not in random_integers:
            random_integers.append(x)
            n -= 1
    return random_integers
