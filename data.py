import os
import random


def read_db_data(file_name):
    with open(os.path.join("tables_data", file_name), "r") as file:
        return file.read().strip().split('\n')

def get_random_street():
    pass


file_names = ["categories.txt", "publishers.txt", "names.txt", "streets.txt",
              "surnames.txt", "titles.txt", "towns.txt", "us_states.txt"]
data = {file_name[:-4]: read_db_data(file_name) for file_name in file_names}

street_numbers_lower_bound = 1
street_number_upper_bound = 300

admittance_years = (str(n) for n in range(1976, 2024))
zip_codes = (str(n) for n in range(10000, 99999))
street_names = (st + " St" for st in data["streets"])