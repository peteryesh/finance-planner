import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS

from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import scoped_session, sessionmaker

from sql_service import *

def create_app():
    app = Flask(__name__)
    CORS(app)

    # engine = create_engine('sqlite:////~/finance_tracker.db')
    # Session = sessionmaker(bind=engine)
    # metadata = MetaData()

    @app.route('/', methods=['GET'])
    def default():
        return ''

    return app

def main():
    print('Starting app...')
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()