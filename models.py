from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
import session as _session
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()
create_flag = False


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), index=True)
    isbn = Column(String(50))
    category = Column(String(50))
    publisher = Column(String(50))
    author_name = Column(String(50))
    author_surname = Column(String(50))
    misc_data = Column(JSONB)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Patron(Base):
    __tablename__ = 'patron'
    patron_id = Column(Integer, primary_key=True, autoincrement=True)
    patron_name = Column(String(50))
    patron_surname = Column(String(50))
    phone_number = Column(String(50))
    passport = Column(String(50), index=True)
    address = Column(String(100))
    departure = Column(Boolean)
    misc_data = Column(JSONB)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Checkout(Base):
    __tablename__ = 'checkout'
    checkout_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    book_id = Column(Integer, ForeignKey('book.book_id'))
    patron_id = Column(Integer, ForeignKey('patron.patron_id'))
    checkout_date = Column(DateTime)
    return_date_expected = Column(DateTime)
    return_date_actual = Column(DateTime)
    misc_data = Column(JSONB)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


if create_flag:
    Base.metadata.create_all(_session.engine)
    print("Tables created successfully.")
