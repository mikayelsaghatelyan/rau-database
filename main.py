import json

import api as api_
import asyncio


async def invoke(async_func, *args, **kwargs):
    res = await async_func(*args, **kwargs)
    return res

# book - title, category, publisher, name, surname
# book.misc_data (JSON) - published_date, language, edition, pages
# patron - name, surname, address, departure
# patron.misc_data (JSON) - join_date, expiration_date, favourite_category
# checkout - bookID, actorID, checkout_date, return_date_expected, return_date_actual
# checkout.misc_data (JSON) - checkout_fee, renewal_amount, book_condition

format_flag = True

method_dict = {
    "book": {"create": api_.create_book,
             "get": api_.get_book,
             "get-all": api_.get_all_books,
             "update": api_.update_book,
             "delete": api_.delete_book,
             "delete-all": api_.delete_all_books,
             "generate": api_.generate_books},
    "patron": {"create": api_.create_patron,
               "get": api_.get_patron,
               "get-all": api_.get_all_patrons,
               "update": api_.update_patron,
               "delete": api_.delete_patron,
               "delete-all": api_.delete_all_patrons,
               "generate": api_.generate_patrons},
    "checkout": {"create": api_.create_checkout,
                 "get": api_.get_checkout,
                 "get-all": api_.get_all_checkouts,
                 "update": api_.update_checkout,
                 "delete": api_.delete_checkout,
                 "delete-all": api_.delete_all_checkouts,
                 "generate": api_.generate_checkouts}}

while (command := input()) != "exit":
    arguments = command.split()
    table, method = arguments[0], arguments[1]

    is_valid_table = table in method_dict
    is_valid_method = method in method_dict["book"], method_dict["patron"], method_dict["checkout"]
    if is_valid_table and is_valid_method:
        if method == "generate":
            arguments[2] = int(arguments[2])
        result = asyncio.run(invoke(method_dict[table][method], *arguments[2:]))
        if method == "get":
            if format_flag:
                print(json.dumps(result.to_dict(), indent=4))
            else:
                print(result.to_dict())
        elif method == "get-all":
            for element in result:
                if format_flag:
                    print(json.dumps(element.to_dict(), indent=4), end="\n")
                else:
                    print(element.to_dict())
        else:
            print(result)
    else:
        print("unknown/invalid command. try again:")
