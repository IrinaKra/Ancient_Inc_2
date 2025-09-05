import csv
import random

from faker import Faker

DEPARTMENTS = ["Engineering", "Sales", "HR", "Marketing", "Finance"]

fake = Faker()

def generate_row():
    return {
        "name": fake.name(),
        "hiring_date": fake.date_between(start_date = '-10y', end_date = 'today').isoformat(),
        "department": random.choice(DEPARTMENTS),
        "birthday": fake.date_of_birth(minimum_age = 18, maximum_age = 65).isoformat()
    }

with open("/Users/iryna.kravchenko/Documents/study/Ancient_Inc_2/database.csv", "w") as file:
    fieldnames = ["name", "hiring_date", "department", "birthday"]
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(100):
        writer.writerow(generate_row())