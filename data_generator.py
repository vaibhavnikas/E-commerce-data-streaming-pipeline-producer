"""Generate dummy data(categories, products, customers, locations) for e-commerce data platform"""

from dotenv import dotenv_values
from faker import Faker
import google.generativeai as genai
import json
import random
from time import sleep

config = dotenv_values(".env")

genai.configure(api_key=config['API_KEY'])
model = genai.GenerativeModel('gemini-2.0-flash')

num_categories = 0
num_products = 0
num_locations = 0
num_customers = 0


def clean_json_string(json_string):
    """Cleans json of leading ```json and trailing ```"""
    return json_string.strip()[8:-3]

def clean_string(str):
    """Cleans a string by removing invalid characters and commas from string columns so that it won't break csv file"""
    # remove invalid characters
    str = str.encode('utf-8', 'ignore').decode('utf-8')
    return str.replace(',', ' ')

def get_header(list):
    """Takes a list of dictionaries as input and returns header to be written to csv file"""
    # any index will work here
    return ','.join(list[0])

def generate_categories():
    prompt = """Generate product categories for ecommerce platform in JSON.
    Ensure the response contains only valid characters for PostgreSQL.

    Use this JSON Schema :
    Category = str
    Return: list[Category]"""

    response = model.generate_content(prompt)
    categories_json = clean_json_string(response.text)
    categories = json.loads(categories_json)

    prepared_categories = []
    global num_categories
    last_category_id = num_categories + 1
    for id, category in enumerate(categories, start=last_category_id):
        prepared_categories.append({'id': str(id), 'name': clean_string(category)})
        num_categories += 1
    return prepared_categories

def generate_products(category):
    prompt = """Generate products for the """ + category['name'] + """ category on ecommerce platform in JSON.
    Ensure the response contains only valid characters for PostgreSQL.

    Use this JSON Schema :
    Product = {'name':str, 'price': int}
    Return: list[Product]"""

    response = model.generate_content(prompt)
    products_json = clean_json_string(response.text)
    products = json.loads(products_json)
    
    prepared_products = []
    category_id = category['id']
    global num_products
    last_product_id = num_products + 1
    for id, product in enumerate(products, start=last_product_id):
        prepared_products.append({
            'id': str(id),
            'name': clean_string(product['name']),
            'category_id': clean_string(category_id),
            'price': clean_string(str(product['price']))
        })
        num_products += 1
    return prepared_products

def generate_locations():
    prompt = """Generate 100 different locations from the top 10 cities in India in JSON.
    Ensure the response contains only valid characters for PostgreSQL.
    
    Use this JSON Schema :
    Location : {'pincode':int, 'locality_name':str, 'city': str, 'state': str}
    Return: list[Location]
    """

    response = model.generate_content(prompt)
    locations_json = clean_json_string(response.text)
    locations = json.loads(locations_json)

    prepared_locations = []
    global num_locations
    last_location_id = num_locations + 1
    for id, location in enumerate(locations, start=last_location_id):
        prepared_locations.append({
            'id': str(id),
            'pincode': clean_string(str(location['pincode'])),
            'locality_name': clean_string(location['locality_name']),
            'city': clean_string(location['city']),
            'state': clean_string(location['state'])
        })
        num_locations += 1
    return prepared_locations

def generate_customers(number_of_customers=1000):
    customers = []
    global num_customers
    last_customer_id = num_customers + 1

    fake = Faker('en_IN')
    for id in range(last_customer_id, last_customer_id + number_of_customers):
        profile = fake.profile()

        firstname = profile['name'].split()[0]
        lastname = profile['name'].split()[1]
        phone = fake.phone_number()
        email = f"{firstname}.{lastname}{random.randint(1,100)}@{fake.domain_name()}"
        customers.append({
            'id': str(id),
            'firstname': clean_string(firstname),
            'lastname': clean_string(lastname),
            'phone': clean_string(phone),
            'email': clean_string(email),
            'gender': clean_string(profile['sex'])
        })
    num_customers += 1
    return customers


categories = generate_categories()
with open('data/categories.csv', 'a') as f:
    header = get_header(categories)
    f.write(header + "\n")
    for category in categories:
        f.write(','.join(category.values()) + "\n")
print('categories generated')

header_written = False
for category in categories:
    products = generate_products(category)
    with open('data/products.csv', 'a') as f:
        if not header_written:
            header = get_header(products)
            f.write(header + "\n")
            header_written = True

        for product in products:
            f.write(','.join(product.values()) + "\n")
    # Free tier allows 15 requests and a million tokens per minute for the model(gemini-2.0-flash) used (refer: https://ai.google.dev/gemini-api/docs/rate-limits)
    print("sleeping for 5 seconds to avoid hitting ratelimit")
    sleep(5)
print('products generated')

locations = generate_locations()
with open('data/locations.csv', 'a') as f:
    header = get_header(locations)
    f.write(header + "\n")
    for location in locations:
        f.write(','.join(location.values()) + "\n")
print('locations generated')

customers = generate_customers()
with open('data/customers.csv', 'a') as f:
    header = get_header(customers)
    f.write(header + "\n")
    for customer in customers:
        f.write(','.join(customer.values()) + "\n")
print('customers generated')
