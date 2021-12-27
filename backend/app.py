import uuid

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from sqlalchemy import create_engine, MetaData, select, update
from sqlalchemy.orm import scoped_session, sessionmaker

from sql_service import User, Account, Transaction

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins":["http://localhost:4200"]}},supports_credentials=True)

    engine = create_engine('sqlite:///../../databases/finance_tracker.db')
    Session = sessionmaker(bind=engine)
    metadata = MetaData()

    @app.route('/', methods=['POST'])
    def default():
        return 'Hello world!'

    ## User endpoints ##
    @app.route('/user', methods=['POST', 'GET', 'PUT', 'DELETE'])
    def add_user():
        if request.method == 'POST':
            username = request.json['username']
            first_name = request.json['first_name']
            last_name = request.json['last_name']

            # Error check
            if username == None or username == '':
                return jsonify({'status': 400, 'response': 'username cannot be blank'})

            with Session.begin() as session:
                user_query = session.query(User).filter_by(username=username)
                if session.query(user_query.exists()).scalar():
                    user = user_query.one()
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    return jsonify({'success': True, 'user': user.user_info(), 'msg': "Updated user information"})
                else:
                    new_user = User(username=username, first_name=first_name, last_name=last_name)
                    session.add(new_user)
                    return jsonify({'success': True, 'user': new_user.user_info(), 'msg': "New user created"})
        elif request.method == 'GET':
            username = request.args['username']

            # Error check
            if username == None or username == '':
                return Response(response='username cannot be blank', status=400)

            with Session.begin() as session:
                user_query = session.query(User).filter_by(username=username)
                if session.query(user_query.exists()).scalar():
                    return jsonify({'success': True, 'user': user_query.first().user_info()})
            return jsonify({'success': False, 'msg': 'User does not exist'})
        elif request.method == 'DELETE':
            username = request.args['username']

            # Error check
            if username == None or username == '':
                return Response(response='username cannot be blank', status=400)

            with Session.begin() as session:
                user_query = session.query(User).filter_by(username=username)
                if session.query(user_query.exists()).scalar():
                    user = user_query.first()
                    session.delete(user)
                    return jsonify({'success': True, 'msg': 'User has been deleted'})
            return jsonify({'success': False, 'msg': 'User does not exist'})


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