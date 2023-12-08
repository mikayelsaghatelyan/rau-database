import os
import random


def read_db_data(file_name):
    with open(os.path.join("book_db_data", file_name), "r") as file:
        return file.read().strip().split('\n')


file_names = ["categories.txt", "publishers.txt", "names.txt", "streets.txt",
              "surnames.txt", "titles.txt", "towns.txt", "us_states.txt"]
data = {file_name[:-4]: read_db_data(file_name) for file_name in file_names}

street_numbers = (str(n) for n in range(1, 300))
birth_years = (str(n) for n in range(1924, 2004))
admittance_years = (str(n) for n in range(1976, 2024))
zip_codes = (str(n) for n in range(10000, 99999))
street_names = (st + " St" for st in data["streets"])

object_number = 500

book_keys = (data["names"], data["surnames"], data["publishers"], data["categories"], data["titles"])
book_objects = (tuple(random.choice(key) for key in book_keys) for _ in range(object_number))
reader_keys = (data["names"], data["surnames"], street_numbers, street_names, ['True', 'False'])
reader_objects = (tuple(random.choice(key) for key in reader_keys) for _ in range(object_number))
