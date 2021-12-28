from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import sessionmaker
from src.sql_service import Base, User, Account, Transaction

## Testing only: drop all tables and recreate them based on sql_service schemas ##
## Not for migration yet ##


def main():
    config = {
        "DATABASE_CONNECTION_STRING": "sqlite:///../../databases/finance_tracker.db"
    }
    engine = create_engine(config["DATABASE_CONNECTION_STRING"])
    Session = sessionmaker(bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
