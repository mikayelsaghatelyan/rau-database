from fastapi import FastAPI, HTTPException, status
from session import session as session_
import models as models_
from datetime import datetime, timedelta
from fastapi import Query
import data as data_

app = FastAPI()


# book CRUD
@app.post("/create_book", tags=["book"])
async def create_book(title_: str = "",
                      isbn_: str = "",
                      category_: str = "",
                      publisher_: str = "",
                      author_name_: str = "",
                      author_surname_: str = ""):
    book = models_.Book(title=title_,
                        isbn=isbn_,
                        category=category_,
                        publisher=publisher_,
                        author_name=author_name_,
                        author_surname=author_surname_)
    session_.add(book)
    session_.commit()
    return f"Book successfully created. BookID: {book.book_id}, Title: {book.title}."


@app.get("/get_book/{book_id}", tags=["book"])
async def get_book(book_id_: int):
    book = session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()
    if book is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
                      new_author_surname: str = ""):
    if (book := session_.query(models_.Book).filter(models_.Book.book_id == book_id_).first()) is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                     detail=f"ID: {book_id_} Book is checked out and cannot be deleted.")
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail=f"ID: {book_id_} Failed to delete book. No book with such ID.")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Failed to delete all books. Some books "
                                        "are checked out and cannot be deleted.")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to get patron by ID: Patron not found.")
    return patron


@app.get("/get_all_patrons", tags=["patron"])
async def get_all_patrons(skip: int = 0, limit: int = 100):
    patrons = session_.query(models_.Patron).offset(skip).limit(limit)
    return patrons.all()


@app.put("/update/{patron_id}", tags=["patron"])
async def update_book(patron_id_: int,
                      new_patron_name: str = "",
                      new_patron_surname: str = "",
                      new_phone_number: str = "",
                      new_passport: str = "",
                      new_address: str = "",
                      new_departure: bool = False):
    if (patron := session_.query(models_.Patron).filter(models_.Patron.patron_id == patron_id_).first()) is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Failed to delete patron. No patrons in database.")
    if (patron := session_.query(models_.Patron).filter(models_.Patron.patron_id == patron_id_).first()) is not None:
        if session_.query(models_.Checkout).filter(models_.Checkout.patron_id == patron_id_).first() is None:
            session_.delete(patron)
            session_.commit()
            return f"Patron successfully deleted: {patron.book_id} - {patron.title}."
        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail=f"ID: {patron_id_} Patron checked out book(s) and cannot be deleted.")
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Failed to delete all patrons. Some patrons "
                                        "checked out books and cannot be deleted.")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="No patrons found. Nothing to delete.")


# checkout methods
@app.post("/create_checkout", tags=["checkout"])
async def create_checkout(book_id_: int,
                          patron_id_: int,
                          checkout_date_: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          return_date_expected_: datetime = (datetime.now() + timedelta(weeks=3)).strftime("%Y-%m-%d"),
                          return_date_actual_: datetime = (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d")):
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
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Failed to create checkout. No patron with such ID.")
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Failed to create checkout. No book with such ID.")


@app.get("/get_checkout/{checkout_id}", tags=["checkout"])
async def get_checkout(checkout_id_: int):
    checkout = session_.query(models_.Checkout).filter(models_.Checkout.checkout_id == checkout_id_).first()
    if checkout is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
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
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail=f"ID: {checkout.checkout_id} "
                                        f"Failed to delete checkout. No checkout with such ID.")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Failed to delete checkout. No checkouts in database.")


@app.delete("/delete_all_checkouts", tags=["checkout"])
async def delete_all_checkouts():
    if session_.query(models_.Checkout).count() > 0:
        deleted_count = session_.query(models_.Checkout).count()
        session_.query(models_.Checkout).delete()
        session_.commit()
        return f"All checkouts successfully deleted. Deleted checkouts count: {deleted_count}."
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="No checkouts found. Nothing to delete.")


@app.post("/generate_books", tags=["book"])
async def generate_books(number: int):
    for _ in range(number):
        create_book()
