import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS

from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import scoped_session, sessionmaker

from sql_service import *

def create_app():
    app = Flask(__name__)
    CORS(app)

    engine = create_engine('postgresql://peter:supersecretpassword@localhost:5432/postgresdb')
    Session = sessionmaker(bind=engine)
    metadata = MetaData()

    @app.route('/', methods=['GET'])
    def default():
        # with Session.begin() as session:
        #     user1 = User(first_name='peter', last_name='noh')
        #     user2 = User(first_name='john', last_name='smith')
        #     session.add(user1)
        #     session.add(user2)
        return "hello there"

    @app.route('/createusertable', methods=['GET'])
    def init_user_tables():
        create_user_table(metadata)
        metadata.create_all(engine)
        return "hi"
    
    @app.route('/resetusertable', methods=['GET'])
    def reset_user_tables():
        with Session.begin() as session:
            pass
        data = {}
        return jsonify(data)
    
    @app.route('/deleteusertable', methods=['GET'])
    def delete_user_table():
        User.__table__.drop(engine)
        return jsonify({'success': True})
    
    @app.route('/testadduser', methods=['GET'])
    def test_add_user():
        with Session.begin() as session:
            user = User(
                user_id = uuid.uuid4(),
                username = 'myusername',
                first_name = 'Peter',
                last_name = 'Noh' 
            )
            session.add(user)
        return jsonify({'success': True})

    @app.route('/adduser', methods=['POST'])
    def add_user():
        user = request.get_json()
        with Session.begin() as session:
            user_row = User(user_id = uuid.uuid4(), username = user['user_name'], first_name = user['first_name'], last_name = user['last_name'])
            session.add(user_row)
            print(user_row.id)
            user_info = user_row.user_info()
        return jsonify({'success': True, 'user': user_info})

    @app.route('/viewallusers', methods=['GET'])
    def view_all():
        with Session() as session:
            all_users = select(User)
            result = session.execute(all_users)
            data = {
                'users': []
            }
            for user in result.scalars():
                print(f"{user.first_name} {user.last_name}")
                data['users'].append(user.user_info())
            return jsonify(data)

    return app

def main():
    print('Starting app...')
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main()