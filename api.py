from fastapi import FastAPI, HTTPException, Request, Query
from starlette import status
from session import session as session_
from datetime import datetime, timedelta
import models as models_
import data as data_
import random
import asyncio
import json

app = FastAPI()


# book CRUD
@app.post("/create_book", tags=["book"])
async def create_book(title_: str = "",
                      isbn_: str = "",
                      category_: str = "",
                      publisher_: str = "",
                      author_name_: str = "",
                      author_surname_: str = "",
                      quantity_: int = 1):
    book = models_.Book(title=title_,
                        isbn=isbn_,
                        category=category_,
                        publisher=publisher_,
                        author_name=author_name_,
                        author_surname=author_surname_,
                        quantity=quantity_)
    session_.add(book)
    session_.commit()
    return f"Book successfully created. BookID: {book.book_id}, Title: {book.title}."


@app.get("/get_book/{book_id}", tags=["book"])
async def get_book(book_id_: int):
    book = session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to get book by ID. Book not found.")
    return book


@app.get("/get_all_books", tags=["book"])
async def get_all_books(skip: int = 0, limit: int = 100):
    books = session_.query(models_.Book).offset(skip).limit(limit)
    return books.all()


@app.put("/update/{book_id}", tags=["book"])
async def update_book(book_id_: int,
                      new_title: str = "",
                      new_isbn: str = "",
                      new_category: str = "",
                      new_publisher: str = "",
                      new_author_name: str = "",
                      new_author_surname: str = "",
                      new_quantity: str = None):
    if (book := session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to update book. No book with such ID.")
    if new_title:
        book.title = new_title
    if new_isbn:
        book.isbn = new_isbn
    if new_category:
        book.category = new_category
    if new_publisher:
        book.publisher = new_publisher
    if new_author_name:
        book.author_name = new_author_name
    if new_author_surname:
        book.author_surname = new_author_surname
    if new_quantity:
        book.quantity = new_quantity
    session_.add(book)
    session_.commit()
    return f"Successfully updated book. BookID: {book.book_id}."


@app.delete("/delete/{book_id}", tags=["book"])
async def delete_book(book_id_: int):
    if session_.query(models_.Book).count() != 0:
        if (book := session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()) is not None:
            if session_.query(models_.Checkout).filter(models_.Checkout.book_id == book_id_).first() is None:
                session_.delete(book)
                session_.commit()
                return f"Book successfully deleted: BookID: {book.book_id}, Title: {book.title}."
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"ID: {book_id_} Book is checked out and cannot be deleted.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"ID: {book_id_} Failed to delete book. No book with such ID.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Failed to delete book. No books in database.")


@app.delete("/delete_all_books", tags=["book"])
async def delete_all_books():
    if session_.query(models_.Book).count() > 0:
        if session_.query(models_.Checkout).count() == 0:
            deleted_count = session_.query(models_.Book).count()
            session_.query(models_.Book).delete()
            session_.commit()
            return f"All books successfully deleted. Deleted books count: {deleted_count}."
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to delete all books. Some books "
                                       "are checked out and cannot be deleted.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No books found. Nothing to delete.")


# patron CRUD
@app.post("/create_patron", tags=["patron"])
async def create_patron(patron_name_: str = "",
                        patron_surname_: str = "",
                        phone_number_: str = "",
                        passport_: str = "",
                        address_: str = "",
                        departure_: bool = False):
    patron = models_.Patron(patron_name=patron_name_,
                            patron_surname=patron_surname_,
                            phone_number=phone_number_,
                            passport=passport_,
                            address=address_,
                            departure=departure_)
    session_.add(patron)
    session_.commit()
    return (f"Patron successfully created: PatronID: {patron.patron_id}, "
            f"Name, Surname: {patron.patron_name} {patron.patron_surname}.")


@app.get("/get_patron/{patron_id}", tags=["patron"])
async def get_patron(patron_id_: int):
    patron = session_.query(models_.Patron).filter(models_.Patron.patron_id == patron_id_).first()
    if patron is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to get patron by ID: Patron not found.")
    return patron


@app.get("/get_all_patrons", tags=["patron"])
async def get_all_patrons(skip: int = 0, limit: int = 100):
    patrons = session_.query(models_.Patron).offset(skip).limit(limit)
    return patrons.all()


@app.put("/update/{patron_id}", tags=["patron"])
async def update_patron(patron_id_: int,
                        new_patron_name: str = "",
                        new_patron_surname: str = "",
                        new_phone_number: str = "",
                        new_passport: str = "",
                        new_address: str = "",
                        new_departure: bool = False):
    if (patron := session_.query(models_.Patron).filter(models_.Patron.patron_id == patron_id_).first()) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to update patron. No patron with such ID.")
    if new_patron_name:
        patron.patron_name = new_patron_name
    if new_patron_surname:
        patron.patron_surname = new_patron_surname
    if new_phone_number:
        patron.phone_number = new_phone_number
    if new_passport:
        patron.passport = new_passport
    if new_address:
        patron.address = new_address
    if new_departure is not None:
        patron.departure = new_departure
    session_.add(patron)
    session_.commit()
    return f"Patron successfully updated. PatronID: {patron.patron_id}."


@app.delete("/delete_patron/{patron_id}", tags=["patron"])
async def delete_patron(patron_id_: int):
    if session_.query(models_.Patron).count() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Failed to delete patron. No patrons in database.")
    if (patron := session_.query(models_.Patron).filter(models_.Patron.patron_id == patron_id_).first()) is not None:
        if session_.query(models_.Checkout).filter(models_.Checkout.patron_id == patron_id_).first() is None:
            session_.delete(patron)
            session_.commit()
            return f"Patron successfully deleted: {patron.book_id} - {patron.title}."
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"ID: {patron_id_} Patron checked out book(s) and cannot be deleted.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID: {patron_id_} Failed to delete patron. No patron with such ID.")


@app.delete("/delete_all_patrons", tags=["patron"])
async def delete_all_patrons():
    if session_.query(models_.Patron).count() > 0:
        if session_.query(models_.Checkout).count() == 0:
            deleted_count = session_.query(models_.Patron).count()
            session_.query(models_.Patron).delete()
            session_.commit()
            return f"All patrons successfully deleted. Deleted patrons count: {deleted_count}."
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to delete all patrons. Some patrons "
                                       "checked out books and cannot be deleted.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No patrons found. Nothing to delete.")


# checkout methods
@app.post("/create_checkout", tags=["checkout"])
async def create_checkout(book_id_: int,
                          patron_id_: int,
                          checkout_date_: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          return_date_expected_:
                          datetime = (datetime.now() + timedelta(weeks=3)).strftime("%Y-%m-%d %H:%M:%S"),
                          return_date_actual_:
                          datetime = (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d% H:%M:%S")):
    if session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first() is not None:
        if session_.query(models_.Patron).filter(models_.Patron.patron_id == patron_id_).first() is not None:
            checkout = models_.Checkout(book_id=book_id_,
                                        patron_id=patron_id_,
                                        checkout_date=checkout_date_,
                                        return_date_expected=return_date_expected_,
                                        return_date_actual=return_date_actual_)
            session_.add(checkout)
            session_.commit()
            return (f"Checkout successfully created. CheckoutID:{checkout.checkout_id} - "
                    f"PatronID:{checkout.patron_id} checked out BookID:{checkout.book_id}.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Failed to create checkout. No patron with such ID.")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to create checkout. No book with such ID.")


@app.get("/get_checkout/{checkout_id}", tags=["checkout"])
async def get_checkout(checkout_id_: int):
    checkout = session_.query(models_.Checkout).filter(models_.Checkout.checkout_id == checkout_id_).first()
    if checkout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to get checkout by ID: Checkout not found.")
    return checkout


@app.get("/get_all_checkouts", tags=["checkout"])
async def get_all_checkouts(skip: int = 0, limit: int = 100):
    checkouts = session_.query(models_.Checkout).offset(skip).limit(limit)
    return checkouts.all()


@app.put("/update/{checkout_id}", tags=["checkout"])
async def update_checkout(checkout_id_: int,
                          new_book_id: int = 0,
                          new_patron_id: int = 0,
                          new_checkout_date: datetime = None,
                          new_return_date_expected: datetime = None,
                          new_return_date_actual: datetime = None):
    if (checkout := session_.query(models_.Checkout).filter(
            models_.Checkout.checkout_id == checkout_id_).first()) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Failed to update checkout. No checkout with such ID.")
    if new_book_id:
        checkout.book_id = new_book_id
    if new_patron_id:
        checkout.patron_id = new_patron_id
    if new_checkout_date:
        checkout.checkout_date = new_checkout_date
    if new_return_date_expected:
        checkout.return_date_expected = new_return_date_expected
    if new_return_date_actual:
        checkout.return_date_actual = new_return_date_actual
    session_.add(checkout)
    session_.commit()
    return f"Checkout successfully updated. CheckoutID: {checkout.checkout_id}."


@app.delete("/delete_checkout/{checkout_id}", tags=["checkout"])
async def delete_checkout(checkout_id_: int):
    if session_.query(models_.Checkout).count() != 0:
        if (checkout := session_.query(models_.Checkout).filter(
                models_.Checkout.checkout_id == checkout_id_).first()) is not None:
            session_.delete(checkout)
            session_.commit()
            return (f"Checkout successfully deleted. CheckoutID:{checkout.checkout_id}: "
                    f"PatronID:{checkout.book_id} checked out BookID:{checkout.title}.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"ID: {checkout.checkout_id} "
                                       f"Failed to delete checkout. No checkout with such ID.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Failed to delete checkout. No checkouts in database.")


@app.delete("/delete_all_checkouts", tags=["checkout"])
async def delete_all_checkouts():
    if session_.query(models_.Checkout).count() > 0:
        deleted_count = session_.query(models_.Checkout).count()
        session_.query(models_.Checkout).delete()
        session_.commit()
        return f"All checkouts successfully deleted. Deleted checkouts count: {deleted_count}."
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No checkouts found. Nothing to delete.")


# Methods for creating lines with random pre-generated values
@app.post("/generate_books", tags=["book"])
async def generate_books(number: int):
    for _ in range(number):
        book = models_.Book(title=data_.get_random_title(),
                            isbn=data_.get_random_isbn(),
                            category=data_.get_random_category(),
                            publisher=data_.get_random_publisher(),
                            author_name=data_.get_random_name(),
                            author_surname=data_.get_random_surname(),
                            quantity=data_.get_random_quantity())
        session_.add(book)
        session_.commit()
    return f"Books successfully generated. Generated books count: {number}"


@app.post("/generate_patrons", tags=["patron"])
async def generate_patrons(number: int):
    for _ in range(number):
        patron = models_.Patron(patron_name=data_.get_random_name(),
                                patron_surname=data_.get_random_surname(),
                                phone_number=data_.get_random_phone_number(),
                                passport=data_.get_random_passport(),
                                address=data_.get_random_address(),
                                departure=data_.get_random_departure())
        session_.add(patron)
        session_.commit()
    return f"Patrons successfully generated. Generated patrons count: {number}"


@app.post("/generate_checkouts", tags=["checkout"])
async def generate_checkouts(number: int):
    book_ids = [book.book_id for book in session_.query(models_.Book).all()]
    patron_ids = [patron.patron_id for patron in session_.query(models_.Patron).all()]
    for _ in range(number):
        patron = models_.Checkout(book_id=random.choice(book_ids),
                                  patron_id=random.choice(patron_ids),
                                  checkout_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  return_date_expected=(datetime.now() + timedelta(weeks=3)).strftime("%Y-%m-%d"),
                                  return_date_actual=(datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d"))
        session_.add(patron)
        session_.commit()
    return f"Checkouts successfully generated. Generated checkouts count: {number}"


# Methods for inserting and reading JSON column (misc_data) values of the tables
@app.post("/insert_json_book", tags=["book"])
async def insert_json_data_book(book_id_: int, json_data: dict):
    book = session_.query(models_.Book).filter(models_.Book.book_id_ == book_id_).first()
    if book is not None:
        book.misc_data = json_data
        session_.add(book)
        session_.commit()
        return f"Book miscellaneous data successfully inserted. BookID: {book.book_id}, Title: {book.title}."
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to insert miscellaneous data into book. No book with such ID.")


@app.get("/get_json_book/{book_id}", tags=["book"])
async def get_json_data_book(book_id_: int):
    book = session_.query(models_.Book).filter(models_.Book.book_id_ == book_id_).first()
    if book is not None:
        return book.misc_data
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to get miscellaneous data into book. No book with such ID.")


@app.post("/insert_json_patron", tags=["patron"])
async def insert_json_data_patron(patron_id_: int, json_data: dict):
    patron = session_.query(models_.Patron).filter(models_.Patron.patron_id_ == patron_id_).first()
    if patron is not None:
        patron.misc_data = json_data
        session_.add(patron)
        session_.commit()
        return f"patron miscellaneous data successfully inserted. patronID: {patron.patron_id}, Title: {patron.title}."
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to insert miscellaneous data into patron. No patron with such ID.")


@app.get("/get_json_patron/{patron_id}", tags=["patron"])
async def get_json_data_patron(patron_id_: int):
    patron = session_.query(models_.Patron).filter(models_.Patron.patron_id_ == patron_id_).first()
    if patron is not None:
        return patron.misc_data
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to get miscellaneous data into patron. No patron with such ID.")


@app.post("/insert_json_checkout", tags=["checkout"])
async def insert_json_data_checkout(checkout_id_: int, json_data: dict):
    checkout = session_.query(models_.Checkout).filter(models_.Checkout.checkout_id_ == checkout_id_).first()
    if checkout is not None:
        checkout.misc_data = json_data
        session_.add(checkout)
        session_.commit()
        return f"checkout miscellaneous data successfully inserted. checkoutID: {checkout.checkout_id}, Title: {checkout.title}."
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to insert miscellaneous data into checkout. No checkout with such ID.")


@app.get("/get_json_checkout/{checkout_id}", tags=["checkout"])
async def get_json_data_checkout(checkout_id_: int):
    checkout = session_.query(models_.Checkout).filter(models_.Checkout.checkout_id_ == checkout_id_).first()
    if checkout is not None:
        return checkout.misc_data
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to get miscellaneous data into checkout. No checkout with such ID.")
