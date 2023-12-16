import json
import api as api_
import asyncio
import data as data_
from datetime import datetime, timedelta


async def invoke(async_func, *args, **kwargs):
    res = await async_func(*args, **kwargs)
    return res


def to_datetime(input_str: str):
    try:
        dt = datetime.strptime(input_str, "%Y-%m-%d_%H:%M:%S")
        return dt
    except ValueError as err:
        raise ValueError(f"Invalid date/time format: {input_str}") from err


def to_date(input_str: str):
    try:
        dt = datetime.strptime(input_str, "%Y-%m-%d_")
        return dt
    except ValueError as err:
        raise ValueError(f"Invalid date format: {input_str}") from err


def print_unknown():
    print("unknown/invalid command. try again:")


def remove_underscores(string: str):
    return string.replace("_", " ")


# book - title, category, publisher, name, surname
# book.misc_data (JSON) - published_date, language, edition, pages
# patron - name, surname, address, departure
# patron.misc_data (JSON) - join_date, expiration_date, favourite_category
# checkout - bookID, actorID, checkout_date, return_date_expected, return_date_actual
# checkout.misc_data (JSON) - checkout_fee, renewal_amount, book_condition


format_flag = True
api_.console_flag = True

method_dict = {
    "book": {"create": api_.create_book,
             "get": api_.get_book,
             "get-all": api_.get_all_books,
             "update": api_.update_book,
             "delete": api_.delete_book,
             "delete-all": api_.delete_all_books,
             "generate": api_.generate_books,
             "json-insert": api_.insert_json_data_book,
             "json-get": api_.get_json_data_book},
    "patron": {"create": api_.create_patron,
               "get": api_.get_patron,
               "get-all": api_.get_all_patrons,
               "update": api_.update_patron,
               "delete": api_.delete_patron,
               "delete-all": api_.delete_all_patrons,
               "generate": api_.generate_patrons,
               "json-insert": api_.insert_json_data_patron,
               "json-get": api_.get_json_data_patron},
    "checkout": {"create": api_.create_checkout,
                 "get": api_.get_checkout,
                 "get-all": api_.get_all_checkouts,
                 "update": api_.update_checkout,
                 "delete": api_.delete_checkout,
                 "delete-all": api_.delete_all_checkouts,
                 "generate": api_.generate_checkouts,
                 "json-insert": api_.insert_json_data_checkout,
                 "json-get": api_.get_json_data_checkout},
    "query": {"1": api_.get_books_select_where,
              "2": api_.get_books_join,
              "3": api_.update_books_category,
              "4": api_.get_books_group}}

while (command := input()) != "exit":
    arguments = command.split()
    first, second = arguments[0], arguments[1]
    is_valid_table = first in method_dict
    is_valid_method = second in method_dict["book"], method_dict["patron"], method_dict["checkout"]
    if is_valid_table and is_valid_method:
        if second in ["generate", "delete"]:
            if len(arguments) <= 3:
                result = asyncio.run(invoke(method_dict[first][second], int(arguments[2])))
                print(result)
            else:
                print_unknown()
                continue
        elif second == "get":
            if len(arguments) <= 3:
                result = asyncio.run(invoke(method_dict[first][second], int(arguments[2])))
                if format_flag:
                    print(json.dumps(result.to_dict(), indent=4))
                else:
                    print(result.to_dict())
            else:
                print_unknown()
                continue
        elif second == "get-all":
            if len(arguments) == 4:
                result = asyncio.run(invoke(method_dict[first][second], int(arguments[2]), int(arguments[3])))
                if len(result) > 0:
                    for element in result:
                        if format_flag:
                            print(json.dumps(element.to_dict(), indent=4), end="\n")
                        else:
                            print(element.to_dict())
                else:
                    print("Database is empty. Nothing to return.")
            else:
                print_unknown()
                continue
        elif second == "delete-all":
            if len(arguments) <= 2:
                result = asyncio.run(invoke(method_dict[first][second]))
                print(result)
            else:
                print_unknown()
                continue
        elif second in ["create", "update"]:
            if first == "book":
                if len(arguments) <= 7:
                    result = asyncio.run(invoke(method_dict[first][second], *arguments[2:]))
                    print(result)
                else:
                    print_unknown()
                    continue
            elif first == "patron":
                if len(arguments) <= 7:
                    departure = bool(arguments[6])
                    result = asyncio.run(invoke(method_dict[first][second], *arguments[2:-1], departure))
                    print(result)
                else:
                    print_unknown()
                    continue
            elif first == "checkout":
                if len(arguments) <= 7:
                    book_id, checkout_id = int(arguments[2]), int(arguments[3])
                    checkout_date = to_datetime(arguments[4])
                    return_date_exp = to_datetime(arguments[5])
                    return_date_act = to_datetime(arguments[6])
                    result = asyncio.run(invoke(method_dict[first][second],
                                                book_id,
                                                checkout_id,
                                                checkout_date,
                                                return_date_exp,
                                                return_date_act))
                    print(result)
                else:
                    print_unknown()
                    continue
            else:
                print_unknown()
        elif second == "json-insert":
            if first == "book":
                if len(arguments) == 7:
                    book_misc_data = {"published_date": to_date(arguments[3]),
                                      "language": arguments[4],
                                      "edition": arguments[5],
                                      "pages": int(arguments[6])}
                    result = asyncio.run(invoke(method_dict[first][second], int(arguments[2]), book_misc_data))
                    print(result)
                elif len(arguments) == 4 and arguments[3] == "random":
                    book_misc_data = {"published_date": data_.get_random_publish_date(),
                                      "language": data_.get_random_language(),
                                      "edition": data_.get_random_edition(),
                                      "pages": data_.get_random_pages()}
                    result = asyncio.run(invoke(method_dict[first][second], int(arguments[2]), book_misc_data))
                    print(result)
                else:
                    print_unknown()
                    continue
            if first == "patron":
                if len(arguments) == 6:
                    patron_misc_data = {"join_date": to_date(arguments[3]),
                                        "expiration_date": to_date(arguments[4]),
                                        "favourite_category": arguments[5]}
                    result = asyncio.run(invoke(method_dict[first][second], int(arguments[2]), patron_misc_data))
                    print(result)
                if len(arguments) == 4 and arguments[3] == "random":
                    patron_misc_data = {"join_date": (join_date := data_.get_random_join_date()),
                                        "expiration_date": join_date + timedelta(weeks=20),
                                        "favourite_category": data_.get_random_category()}
                    result = asyncio.run(invoke(method_dict[first][second], int(arguments[2]), patron_misc_data))
                    print(result)
                else:
                    print_unknown()
                    continue
            if first == "checkout":
                if len(arguments) == 6:
                    checkout_misc_data = {"checkout-fee": int(arguments[3]),
                                          "renewal-amount": int(arguments[4]),
                                          "book-condition": arguments[5]}
                    result = asyncio.run(invoke(method_dict[first][second], int(arguments[2]), checkout_misc_data))
                    print(result)
                if len(arguments) == 4 and arguments[3] == "random":
                    checkout_misc_data = {"checkout-fee": data_.get_random_fee(),
                                          "renewal-amount": data_.get_random_renewal_amount(),
                                          "book-condition": data_.get_random_condition()}
                    result = asyncio.run(invoke(method_dict[first][second], int(arguments[2]), checkout_misc_data))
                    print(result)
        elif second == "json-get":
            if len(arguments) == 3:
                result = asyncio.run(invoke(method_dict[first][second], int(arguments[2])))
                if format_flag:
                    print(json.dumps(result, indent=4))
                else:
                    print(result.to_dict())
            else:
                print_unknown()
        elif first == "query":
            if ((second == "1" and len(arguments) == 5) or (second == "2" and len(arguments) == 3) or
               (second == "3" and len(arguments) == 7) or (second == "4" and len(arguments) == 2)):
                result = asyncio.run(invoke(method_dict[first][second], *arguments[2:]))
                if second in ["1", "2", "4"]:
                    for element in result:
                        if format_flag:
                            print(json.dumps(element, indent=4))
                        else:
                            print(element)
                else:
                    print(result)
            else:
                print_unknown()
        else:
            print_unknown()
    else:
        print_unknown()
