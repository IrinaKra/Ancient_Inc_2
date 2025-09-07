import csv
import random

from faker import Faker

DEPARTMENTS = ["Engineering", "Sales", "HR", "Marketing", "Finance"]
FIELDS = ["name", "department", "birthday", "hiring_date"]

fake = Faker()

def generate_row():
    return {
        "name": fake.name(),
        "department": random.choice(DEPARTMENTS),
        "birthday": fake.date_of_birth(minimum_age = 18, maximum_age = 65).isoformat(),
        "hiring_date": fake.date_between(start_date = '-10y', end_date = 'today').isoformat()
    }

with open("database.csv", "w") as file:
    fieldnames = FIELDS
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(100):
        writer.writerow(generate_row())