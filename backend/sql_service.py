import uuid
from typing import cast

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

PostgreSQLUUID = cast(
    "sqlalchemy.types.TypeEngine[uuid.UUID]",
    UUID(as_uuid=True)
)

def create_user_table(metadata):
    user_table = Table(
        "users",
        metadata,
        Column('user_id', PostgreSQLUUID, primary_key=True),
        Column('username', String(30)),
        Column('first_name', String(30)),
        Column('last_name', String(30))
    )

class User(Base):
    __tablename__ = 'users'

    user_id = Column(PostgreSQLUUID, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    def __repr__(self):
        return "<User(first_name='%s', last_name='%s')>" % (self.first_name, self.last_name)

    def user_info(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name
        }