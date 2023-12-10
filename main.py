import crud as crud_
import data as data_
import asyncio
import random


async def invoke(async_func, *args, **kwargs):
    result = await async_func(*args, **kwargs)
    return result

# book - title, category, publisher, name, surname
# patron - name, surname, address, departure
# checkout - bookID, actorID, checkout_date, return_date_expected, return_date_actual

# print(asyncio.run(invoke(crud_.create_book, "fi", "1212", "fa", "fo", "rero", "boo")))
# print(asyncio.run(invoke(crud_.create_patron, "paul", "paulownia", "0988888", "AK0202", "11 koko st", False)))
# print(asyncio.run(invoke(crud_.create_checkout, random.randint(1, 9), random.randint(1, 5))))
# print(asyncio.run(invoke(crud_.get_book, 1)).to_dict())
# print([obj.to_dict() for obj in asyncio.run(invoke(crud_.get_all_books))])
# print(asyncio.run(invoke(crud_.get_patron, 1)).to_dict())
# print([obj.to_dict() for obj in asyncio.run(invoke(crud_.get_all_patrons))])
# print(asyncio.run(invoke(crud_.get_checkout, 3)).to_dict())
# print([obj.to_dict() for obj in asyncio.run(invoke(crud_.get_all_checkouts))])



