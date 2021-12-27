import os
import tempfile

import pytest

from src.app import create_app, init_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    config = {"DATABASE_CONNECTION_STRING": f"sqlite:///{db_path}", "TESTING": True}
    app = create_app(config)

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
