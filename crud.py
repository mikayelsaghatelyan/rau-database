from fastapi import FastAPI, HTTPException, status
from session import session as session_
import models as models_
from sqlalchemy import DateTime
from datetime import datetime, date
from fastapi import Query

app = FastAPI()


# book CRUD
@app.post("/create_book", tags=["book"])
async def create_book(title_: str,
                      category_: str = "",
                      publisher_: str = "",
                      author_name_: str = "",
                      author_surname_: str = ""):
    obj = models_.Book(title=title_,
                       category=category_,
                       publisher=publisher_,
                       author_name=author_name_,
                       author_surname=author_surname_)
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
async def update_book(book_id_: int,
                      new_title: str,
                      new_category: str = "",
                      new_publisher: str = "",
                      new_author_name: str = "",
                      new_author_surname: str = ""):
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


# patron CRUD
@app.post("/create_patron", tags=["patron"])
async def create_patron(patron_name_: str = "",
                        patron_surname_: str = "",
                        address_: str = "",
                        departure_: bool = "False"):
    check_patron_id_first = session_.query(models_.actor).filter(models_.actor.id == patron_id).first()
    if check_patron_id_first is not None:
        check_patron_id_second = session_.query(models_.patron).filter(models_.patron.id == patron_id).first()
        if check_patron_id_second is None:
            object = models_.patron(id=patron_id, name=name, ampula=ampula, piesa=piesa, gender=gender)
            session_.add(object)
            session_.commit()
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID IN USE, CHANGE THE ID")
        if name:
            return f"patron added: {object.name}"
        else:
            return f"patron added: ID = {object.id}"
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID IN USE, CHANGE THE ID")


@app.get("/get_patron", tags=["patron"])
async def get_all_patrons(skip: int = Query(0, ge=0), limit: int = Query(100)):
    patron_query = session_.query(models_.patron).offset(skip).limit(limit)
    return patron_query.all()


@app.put("/update_patron/{patron_id}", tags=["patron"])
async def patron_update(
        patron_id: int,
        new_name: str = "",
        new_ampula: str = "",
        new_piesa: str = "",
        new_gender: str = ""
):
    patron_object = session_.query(models_.patron).filter(models_.patron.id == patron_id).first()
    if patron_object is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")

    if new_name:
        patron_object.name = new_name
    if new_ampula:
        patron_object.ampula = new_ampula
    if new_piesa != 0:
        patron_object.piesa = new_piesa
    if new_gender:
        patron_object.gender = new_gender
    session_.add(patron_object)
    session_.commit()
    return "patron successfully updated"


@app.delete("/delete_patron/{patron_id}", tags=["patron"])
async def patron_delete(patron_id: int):
    patron_object = session_.query(models_.patron).filter(models_.patron.id == patron_id).first()
    if patron_object is not None:
        session_.delete(patron_object)
        session_.commit()
        return f"patron deleted: {patron_object.id}"
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")




# checkout methods
@app.post("/create_checkout", tags=["checkout"])
async def create_checkout(start_patron: date = datetime.now().strftime("%Y-%m-%d"),
                          stop_patron: date = datetime.now().strftime("%Y-%m-%d"),
                          date_of: date = datetime.now().strftime("%Y-%m-%d"),
                          group_number: int = 0, patron_type: str = "",
                          director: str = ""):
    if session_.query(models_.Book).filter(
            models_.Book.id == checkout_id).first() is not None:  # if found id in actor.id
        if session_.query(models_.Checkout).filter(
                models_.Checkout.id == checkout_id).first() is None:  # if not found id in checkout.id
            object = models_.Checkout(id=checkout_id, start_patron=start_patron, stop_patron=stop_patron,
                                      patron_type=patron_type, group_number=group_number,
                                      director=director, date_of=date_of)
            session_.add(object)
            session_.commit()
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID IN USE, CHANGE THE ID")
        if patron_type:
            return f"checkout added: {object.patron_type}"
        else:
            return f"checkout added: ID = {object.id}"
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID in actor")


@app.get("/get_checkout", tags=["checkout"])
async def get_all_checkout(skip: int = Query(0, ge=0), limit: int = Query(100)):
    checkout_query = session_.query(models_.Checkout).offset(skip).limit(limit)
    return checkout_query.all()


@app.put("/update_checkout/{checkout_id}", tags=["checkout"])
async def checkout_update(
        checkout_id: int,
        new_group_number: int = 0,
        new_start_patron: date = datetime.now().strftime("%Y-%m-%d"),
        new_stop_patron: date = datetime.now().strftime("%Y-%m-%d"),
        new_patron_type: str = "",
        new_director: str = "",
        new_date_of: date = datetime.now().strftime("%Y-%m-%d")
):
    checkout_object = session_.query(models_.Checkout).filter(models_.Checkout.id == checkout_id).first()
    if checkout_object is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")

    if new_group_number:
        checkout_object.group_number = new_group_number
    if new_start_patron:
        checkout_object.stop_patron = new_start_patron
    if new_stop_patron != 0:
        checkout_object.stop_patron = new_stop_patron
    if new_patron_type:
        checkout_object.patron_type = new_patron_type
    if new_director:
        checkout_object.director = new_director
    if new_date_of:
        checkout_object.date_of = new_date_of
    session_.add(checkout_object)
    session_.commit()
    return "checkout successfully updated"


@app.delete("/delete_checkout/{checkout_id}", tags=["checkout"])
async def checkout_delete(checkout_id: int):
    checkout_object = session_.query(models_.Checkout).filter(models_.Checkout.id == checkout_id).first()
    if checkout_object is not None:
        session_.delete(checkout_object)
        session_.commit()
        return f"checkout deleted: {checkout_object.id}"
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")
