import crud
import asyncio


async def invoke(async_func, *args, **kwargs):
    result = await async_func(*args, **kwargs)
    return result


asyncio.run(invoke(crud.create_book, "fi", "fa", "fo", "rero", "ragu"))