import random
from faker import Faker
import mysql.connector

# Database connection configuration
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'flowershop',
}

# List of flower names
flower_names = [
    "Rose",
    "Carnation",
    "Tulip",
    "Lily",
    "Chrysanthemum",
    "Violet",
    "Freesia",
    "Sunflower",
    "Marigold",
    "Rosehip",
    "Hyacinth",
    "Lotus",
    "Butterfly Orchid",
    "Lily of the Valley",
    "Lilac",
    "Peony",
    "Narcissus",
    "Chrysoprase",
    "Rhododendron",
    "Jasmine"
]

# Create Faker instance to generate random data
fake = Faker()

# Connect to the database
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Number of flower records to insert
num_records = 100

# Generate random flower data and insert into the database
for _ in range(num_records):
    flower_name = random.choice(flower_names)
    origin = fake.country()
    price = round(random.uniform(1, 100), 2)
    stock = random.randint(0, 50)

    query = '''
    INSERT INTO flowers (flower_name, origin, price, stock)
    VALUES (%s, %s, %s, %s)
    '''

    cursor.execute(query, (flower_name, origin, price, stock))

# Commit the inserted data
cnx.commit()

# Close the database connection
cursor.close()
cnx.close()

print(f'Successfully inserted {num_records} flower records.')
