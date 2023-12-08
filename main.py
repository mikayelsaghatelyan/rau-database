from fastapi import FastAPI, HTTPException, status
from session import session as session_
import models as models_
from sqlalchemy import DateTime
from datetime import datetime, date
from fastapi import Query

app = FastAPI()


@app.post("/create_book", tags=["book"])
async def create_book(title_: str, category_: str = "", publisher_: str = "",
                      author_name_: str = "", author_surname_: str = ""):
    obj = models_.Book(title=title_, category=category_, publisher=publisher_,
                       author_name=author_name_, author_surname=author_surname_)
    session_.add(obj)
    session_.commit()
    return f"Book created: {obj.book_id} - {obj.title}."


@app.get("/get_book/{book_id}", tags=["book"])
async def get_book(book_id_: int):
    book = session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to get book by ID: Book not found.")
    return book


@app.get("/get_all_books", tags=["book"])
async def get_all_books(skip: int = 0, limit: int = 100):
    books_query = session_.query(models_.Book).offset(skip).limit(limit)
    return books_query.all()


@app.put("/update/{book_id}", tags=["book"])
async def update_book(book_id_: int, new_title: str, new_category: str = "", new_publisher: str = "",
                      new_author_name: str = "", new_author_surname: str = ""):
    if (obj := session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to update book: No book with such ID.")
    if new_title:
        obj.title = new_title
    if new_category:
        obj.category = new_category
    if new_publisher:
        obj.publisher = new_publisher
    if new_author_name:
        obj.author_name = new_author_name
    if new_author_surname:
        obj.author_surname = new_author_surname
    session_.add(obj)
    session_.commit()
    return f"Successfully updated book with ID:{obj.book_id}."


@app.delete("/delete/{book_id}", tags=["book"])
async def delete_book(book_id_: int):
    if (obj := session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()) is not None:
        if session_.query(models_.Checkout).filter(models_.Checkout.book_id == book_id_).first() is None:
            session_.delete(obj)
            session_.commit()
            return f"Book deleted: {obj.book_id} - {obj.title}."
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f"ID: {book_id_} Book is checked out and cannot be deleted.")
