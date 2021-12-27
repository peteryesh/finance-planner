import uuid

from flask import Flask, request, jsonify, Response, g, current_app
from flask_cors import CORS

from sqlalchemy import create_engine, MetaData, select, update
from sqlalchemy.orm import scoped_session, sessionmaker

from src.sql_service import User, Account, Transaction, Base


def create_app(config):
    app = Flask(__name__)

    app.config.update(config)

    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:4200"]}},
        supports_credentials=True,
    )

    with app.app_context():
        engine = get_db()
        Session = sessionmaker(bind=engine)
        metadata = MetaData()

    @app.route("/", methods=["POST"])
    def default():
        return "Hello world!"

    ## User endpoints ##
    @app.route("/user", methods=["POST", "GET", "PUT", "DELETE"])
    def add_user():
        if request.method == "POST":
            username = request.json["username"]
            first_name = request.json["first_name"]
            last_name = request.json["last_name"]

            # Error check
            if username == None or username == "":
                return jsonify({"response": "username cannot be blank"}), 400

            with Session.begin() as session:
                user_query = session.query(User).filter_by(username=username)
                if session.query(user_query.exists()).scalar():
                    user = user_query.one()
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    return (
                        jsonify(
                            {
                                "success": True,
                                "user": user.user_info(),
                                "msg": "Updated user information",
                            }
                        ),
                        200,
                    )
                else:
                    new_user = User(
                        username=username, first_name=first_name, last_name=last_name
                    )
                    session.add(new_user)
                    return (
                        jsonify(
                            {
                                "success": True,
                                "user": new_user.user_info(),
                                "msg": "New user created",
                            }
                        ),
                        200,
                    )
        elif request.method == "GET":
            username = request.args["username"]

            # Error check
            if username == None or username == "":
                return jsonify({"response": "username cannot be blank"}), 400

            with Session.begin() as session:
                user_query = session.query(User).filter_by(username=username)
                if session.query(user_query.exists()).scalar():
                    return (
                        jsonify(
                            {"success": True, "user": user_query.first().user_info()}
                        ),
                        200,
                    )
            return jsonify({"success": False, "msg": "User does not exist"}), 404
        elif request.method == "DELETE":
            username = request.args["username"]

            # Error check
            if username == None or username == "":
                return jsonify({"response": "username cannot be blank"}), 400

            with Session.begin() as session:
                user_query = session.query(User).filter_by(username=username)
                if session.query(user_query.exists()).scalar():
                    user = user_query.first()
                    session.delete(user)
                    return (
                        jsonify({"success": True, "msg": "User has been deleted"}),
                        200,
                    )
            return jsonify({"success": False, "msg": "User does not exist"}), 204

    @app.route("/updateuser", methods=["POST"])
    def update_user():
        return ""

    @app.route("/deleteuser", methods=["GET"])
    def delete_user():
        return ""

    @app.route("/viewuser", methods=["GET"])
    def view_user():
        return ""

    ## Transaction endpoints ##
    @app.route("/addtransaction", methods=["POST"])
    def add_transaction():
        return ""

    @app.route("/updatetransaction", methods=["POST"])
    def update_transaction():
        return ""

    @app.route("/deletetransaction", methods=["GET"])
    def delete_transaction():
        return ""

    @app.route("/viewtransactions", methods=["GET"])
    def view_transactions():
        return ""

    ## Account endpoints
    @app.route("/addaccount", methods=["POST"])
    def add_account():
        return ""

    @app.route("/updateaccount", methods=["POST"])
    def update_account():
        return ""

    @app.route("/deleteaccount", methods=["GET"])
    def delete_account():
        return ""

    @app.route("/viewaccount", methods=["GET"])
    def view_account():
        return ""

    return app


def get_db():
    """Establish a connection to the database and maintain that throughout the lifetime
    of a gien flask app context
    """
    if "db" not in g:
        g.db = create_engine(current_app.config["DATABASE_CONNECTION_STRING"])

    return g.db


def init_db():
    """Initialize all tables in the database"""
    db = get_db()
    Base.metadata.create_all(db)


def main():
    print("Starting app...")
    config = {
        "DATABASE_CONNECTION_STRING": "sqlite:///../../databases/finance_tracker.db"
    }
    app = create_app(config)
    app.run(debug=True)


if __name__ == "__main__":
    main()
