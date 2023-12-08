from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
import session as _session

Base = declarative_base()
create_flag = False


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String(50))
    author_surname = Column(String(50))
    category = Column(String(50))
    publisher = Column(String(50))
    title = Column(String(100))


class Patron(Base):
    __tablename__ = 'patron'
    patron_id = Column(Integer, primary_key=True, autoincrement=True)
    patron_name = Column(String(50))
    patron_surname = Column(String(50))
    address = Column(String(100))
    departure = Column(Boolean)


class Checkout(Base):
    __tablename__ = 'checkout'
    checkout_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.book_id'))
    patron_id = Column(Integer, ForeignKey('patron.patron_id'))
    checkout_date = Column(DateTime)
    return_date_expected = Column(DateTime)
    return_date_actual = Column(DateTime)


if create_flag:
    Base.metadata.create_all(_session.engine)
    print("Tables created successfully.")
