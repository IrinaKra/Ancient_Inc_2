import csv
import random

from pathlib import Path
from faker import Faker

DEPARTMENTS = ["Engineering", "Sales", "HR", "Marketing", "Finance"]
FIELDS = ["name", "department", "birthday", "hiring_date"]

fake = Faker()


def generate_row(
    *,
    min_age=21,
    max_age=65,
    h_start="-10y",
    h_end="today",
):
    return {
        "name": fake.name(),
        "department": random.choice(DEPARTMENTS),
        "birthday": fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).isoformat(),
        "hiring_date": fake.date_between(start_date=h_start, end_date=h_end).isoformat()
    }


def generate_data(num: int = 100) -> Path:
    path = Path("database.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for i in range(num):
            writer.writerow(generate_row())
    return path


if __name__ == "__main__":
    generate_data()