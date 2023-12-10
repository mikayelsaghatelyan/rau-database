import os
import random


def read_data(file_name):
    with open(os.path.join("tables_data", file_name), "r") as file:
        return file.read().strip().split('\n')


def get_random_isbn():
    prefix = random.choice(['978', '979'])
    middle_digits = ''.join(random.choice('0123456789') for _ in range(9))
    check_digit = calculate_isbn_check_digit(prefix + middle_digits)
    return prefix + middle_digits + check_digit


def calculate_isbn_check_digit(isbn_prefix):
    total = sum(int(digit) * (index % 2 * 2 + 1) for index, digit in enumerate(isbn_prefix))
    check_digit = (11 - (total % 11)) % 11
    return str(check_digit) if check_digit < 10 else 'X'


def get_random_phone_number():
    return f"+374({random.randint(10, 99)}){random.randint(100000, 999999)}"


def get_random_name():
    return random.choice(data["names"])


def get_random_surname():
    return random.choice(data["surnames"])


def get_random_category():
    return random.choice(data["categories"])


def get_random_publisher():
    return random.choice(data["publishers"])


def get_random_address():
    address = (f"{random.randint(1, 300)} {random.choice(data['streets'])} St, "
               f"Apt. {random.randint(1, 200)}, {random.randint(100000, 999999)}")
    return address


def get_random_departure():
    return bool(random.randint(0, 1))


def get_random_title():
    return random.choice(data["titles"])


def get_random_passport():
    letters = random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2)
    numbers = ''.join(random.choices('0123456789', k=8))
    passport_code = ''.join(letters) + numbers
    return passport_code


file_names = ["categories.txt", "publishers.txt", "names.txt", "streets.txt",
              "surnames.txt", "titles.txt", "towns.txt", "us_states.txt"]

data = {file_name[:-4]: read_data(file_name) for file_name in file_names}
