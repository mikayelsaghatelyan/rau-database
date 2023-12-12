import json

import api as api_
import asyncio


async def invoke(async_func, *args, **kwargs):
    res = await async_func(*args, **kwargs)
    return res


# book - title, category, publisher, name, surname
# patron - name, surname, address, departure
# checkout - bookID, actorID, checkout_date, return_date_expected, return_date_actual

# print(asyncio.run(invoke(api_.create_book, "fi", "1212", "fa", "fo", "rero", "boo")))
# print(asyncio.run(invoke(api_.create_patron, "paul", "paulownia", "0988888", "AK0202", "11 koko st", False)))
# print(asyncio.run(invoke(api_.create_checkout, random.randint(1, 9), random.randint(1, 5))))
# print(asyncio.run(invoke(api_.get_book, 1)).to_dict())
# print([obj.to_dict() for obj in asyncio.run(invoke(api_.get_all_books))])
# print(asyncio.run(invoke(api_.get_patron, 1)).to_dict())
# print([obj.to_dict() for obj in asyncio.run(invoke(api_.get_all_patrons))])
# print(asyncio.run(invoke(api_.get_checkout, 3)).to_dict())
# print([obj.to_dict() for obj in asyncio.run(invoke(api_.get_all_checkouts))])

size = 5000
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
