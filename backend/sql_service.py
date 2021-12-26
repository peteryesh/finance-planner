import uuid
from typing import cast

from sqlalchemy import Table, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    def __repr__(self):
        return "<User(first_name='%s', last_name='%s')>" % (self.first_name, self.last_name)

    def user_info(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True)
    account_type = Column(String)
    account_name = Column(String)
    account_balance = Column(Float)
    user_id = Column(Integer)

class Transaction(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(Integer, primary_key=True)
    date = Column(Date)
    amount = Column(Float)
    category = Column(String)
    notes = Column(String)
    account_id = Column(Integer)