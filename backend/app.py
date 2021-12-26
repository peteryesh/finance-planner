import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS

from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import scoped_session, sessionmaker

from sql_service import User, Account, Transaction

def create_app():
    app = Flask(__name__)
    CORS(app)

    engine = create_engine('sqlite:///../../databases/finance_tracker.db')
    Session = sessionmaker(bind=engine)
    metadata = MetaData()

    @app.route('/', methods=['POST'])
    def default():
        return 'Hello world!'

    ## User endpoints ##
    @app.route('/adduser', methods=['POST'])
    def add_user():
        print(request.form['username'])
        print(request.form['first_name'])
        print(request.form['last_name'])
        print('hi there mr ang')
        return jsonify({'success': True})

    @app.route('/updateuser', methods=['POST'])
    def update_user():
        return ''

    @app.route('/deleteuser', methods=['GET'])
    def delete_user():
        return ''

    @app.route('/viewuser', methods=['GET'])
    def view_user():
        return ''
    
    ## Transaction endpoints ##
    @app.route('/addtransaction', methods=['POST'])
    def add_transaction():
        return ''
    
    @app.route('/updatetransaction', methods=['POST'])
    def update_transaction():
        return ''

    @app.route('/deletetransaction', methods=['GET'])
    def delete_transaction():
        return ''
    
    @app.route('/viewtransactions', methods=['GET'])
    def view_transactions():
        return ''
    
    ## Account endpoints
    @app.route('/addaccount', methods=['POST'])
    def add_account():
        return ''
    
    @app.route('/updateaccount', methods=['POST'])
    def update_account():
        return ''
    
    @app.route('/deleteaccount', methods=['GET'])
    def delete_account():
        return ''

    @app.route('/viewaccount', methods=['GET'])
    def view_account():
        return ''

    return app

def main():
    print('Starting app...')
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()