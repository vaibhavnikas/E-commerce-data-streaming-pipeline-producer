"""Generates synthetic ecommerce transaction records and sends them to a Kafka topic, facilitating real-time data ingestion into a data warehouse."""

import datetime
from dotenv import dotenv_values
import json
from kafka_producer import create_kafka_producer, send_message, close_producer
import random
from utilities import get_csv_data, get_current_date, get_next_date, get_last_transaction_id, get_random_integers, save_current_date, save_last_transaction_id


config = dotenv_values('.env')

def get_customers():
    filepath = 'data/customers.csv'
    customers = get_csv_data(filepath)
    return customers

def get_locations():
    filepath = 'data/locations.csv'
    locations = get_csv_data(filepath)
    return locations

def get_products():
    filepath = 'data/products.csv'
    products = get_csv_data(filepath)
    return products

def get_n_products(n:int):
    """Returns n random products from products.csv"""
    products = get_products()
    last_product_id = len(products)
    product_ids = get_random_integers(n, 1, last_product_id)

    n_products = []
    for product_id in product_ids:
        # product_id 1 is at 0th index in products list
        n_products.append(products[product_id-1])
    return n_products

def get_random_customer():
    """Returns a random customer from customer.csv"""
    customers = get_customers()
    index = random.randint(0, len(customers)-1)
    return customers[index]

def get_random_location():
    """Returns a random location from locations.csv"""
    locations = get_locations()
    index = random.randint(0, len(locations)-1)
    return locations[index]

def generate_transaction_data(transaction_id:int, date:datetime.date):
    """Generates synthetic transaction data for a ecommerce transaction"""
    # should generate a random customer_id or location_id by getting max customer or location id. No need to get the data as its not being used.
    customer = get_random_customer()
    location = get_random_location()
    
    num_products_in_transaction = random.randint(1, 10)
    products = get_n_products(num_products_in_transaction)
    transaction_data = []
    for product in products:
        product_quantity = random.randint(1, 5)
        billed_amount = int(product['price']) * product_quantity
        # data can be optimised by reducing redundancy
        transaction_data.append({
            'transaction_id': transaction_id,
            'customer_id': int(customer['id']),
            'product_id': int(product['id']),
            'quantity': product_quantity,
            'billed_amount': billed_amount,
            'location_id': int(location['id']),
            'date_id': str(date)
        })
    return transaction_data

def produce_transactions():
    """Produces transaction data to a kafka topic (e-commerce-transactions)"""
    current_date = get_current_date()
    last_date = datetime.date.today()
    last_transaction_id = get_last_transaction_id()
    current_transaction_id = last_transaction_id + 1

    bootstrap_servers = json.loads(config['BOOTSTRAP_SERVERS'])
    producer = create_kafka_producer(bootstrap_servers=bootstrap_servers)
    
    while True:
        send_message(producer, 'e-commerce-transactions', {'date': str(current_date), 'type':'date'})
        num_of_transactions_on_current_date = random.randint(10, 100)

        for transaction_id in range(current_transaction_id, current_transaction_id + num_of_transactions_on_current_date):
            transaction_data = generate_transaction_data(transaction_id, current_date)
            send_message(producer, 'e-commerce-transactions', {'transaction_data': transaction_data, 'type':'transaction'})
            save_last_transaction_id(transaction_id)
        
        current_transaction_id += num_of_transactions_on_current_date
        if current_date == last_date:
            break
        current_date = get_next_date(current_date)
        save_current_date(current_date)

    close_producer(producer)

produce_transactions()
