import uuid
from typing import cast

from sqlalchemy import Table, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = Column(String(30), primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))

    def __repr__(self):
        return "<User(username='%s', first_name='%s', last_name='%s')>" % (
            self.username,
            self.first_name,
            self.last_name,
        )

    def user_info(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True)
    account_type = Column(String(30))
    account_name = Column(String(30))
    account_balance = Column(Float)
    username = Column(String(30))


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    date = Column(Date)
    amount = Column(Float)
    category = Column(String(30))
    notes = Column(String(30))
    account_id = Column(Integer, ForeignKey("accounts.account_id", ondelete="SET NULL"))
    username = Column(String(30), ForeignKey("users.username"))
