import uuid

from flask import Flask, request, jsonify, Response, g, current_app
from flask_cors import CORS

from sqlalchemy import create_engine, MetaData, select, update
from sqlalchemy.orm import scoped_session, sessionmaker

from src.sql_service import User, Account, Transaction, Base
from src.types import AccountType


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
            if string_blank(username):
                return jsonify({"response": "username cannot be blank"}), 400

            with Session.begin() as session:
                if user_exists(session, username):
                    user = get_user_from_db(session, username)
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    return (
                        jsonify(
                            {
                                "success": True,
                                "user": user.user_dict(),
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
                                "user": new_user.user_dict(),
                                "msg": "New user created",
                            }
                        ),
                        201,
                    )
        elif request.method == "GET":
            username = request.args["username"]

            # Error check
            if string_blank(username):
                return jsonify({"response": "username cannot be blank"}), 400

            with Session.begin() as session:
                if user_exists(session, username):
                    return (
                        jsonify(
                            {
                                "success": True,
                                "user": get_user_from_db(session, username).user_dict(),
                            }
                        ),
                        200,
                    )
            return jsonify({"success": False, "msg": "User does not exist"}), 404

        elif request.method == "DELETE":
            username = request.args["username"]

            # Error check
            if string_blank(username):
                return jsonify({"response": "username cannot be blank"}), 400

            with Session.begin() as session:
                if user_exists(session, username):
                    user = get_user_from_db(session, username)
                    session.delete(user)
                    return (
                        jsonify({"success": True, "msg": "User has been deleted"}),
                        200,
                    )
            return jsonify({"success": False, "msg": "User does not exist"}), 204

    ## Account endpoints ##
    @app.route("/account", methods=["POST", "GET", "DELETE"])
    def submit_account():
        if request.method == "POST":
            account_info = request.json
        elif request.method == "GET" or request.method == "DELETE":
            account_info = request.args

        with Session.begin() as session:
            if string_blank(account_info["username"]):
                return jsonify({"response": "username cannot be blank"}), 400
            if not user_exists(session, account_info["username"]):
                return (
                    jsonify({"success": False, "msg": "User does not exist"}),
                    400,
                )

            if request.method == "POST":
                if not account_type_valid(account_info["account_type"]):
                    return jsonify({"response": "Account type is not valid"}), 400

                # If a blank account_id is given, regard as new account entry
                if string_blank(account_info["account_id"]):
                    new_account_id = str(uuid.uuid4())
                    while account_exists(session, new_account_id):
                        new_account_id = str(uuid.uuid4())
                    new_account = Account(
                        account_id=new_account_id,
                        account_type=account_info["account_type"],
                        account_name=account_info["account_name"],
                        account_balance=account_info["account_balance"],
                        username=account_info["username"],
                    )
                    if string_blank(new_account.account_name):
                        new_account.account_name = "Squirtle is lucky"
                    if new_account.account_balance is None:
                        new_account.account_balance = 0
                    session.add(new_account)
                    return (
                        jsonify(
                            {
                                "success": True,
                                "account": new_account.account_dict(),
                                "msg": "New account successfully created",
                            }
                        ),
                        201,
                    )
                elif account_exists(session, account_info["account_id"]):
                    acct = get_account_from_db(session, account_info["account_id"])
                    acct.account_type = account_info["account_type"]
                    acct.account_name = account_info["account_name"]
                    acct.account_balance = account_info["account_balance"]
                    return (
                        jsonify(
                            {
                                "success": True,
                                "account": acct.account_dict(),
                                "msg": "Account info successfully updated",
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify({"success": False, "msg": "Account does not exist"}),
                        400,
                    )

            elif request.method == "GET":
                if not account_exists(session, account_info["account_id"]):
                    return (
                        jsonify({"success": False, "msg": "Account does not exist"}),
                        400,
                    )
                else:
                    acct = get_account_from_db(session, account_info["account_id"])
                    return (
                        jsonify({"success": True, "account": acct.account_dict()}),
                        200,
                    )

            elif request.method == "DELETE":
                if not account_exists(session, account_info["account_id"]):
                    return (
                        jsonify({"success": False, "msg": "Account does not exist"}),
                        400,
                    )
                else:
                    acct = get_account_from_db(session, account_info["account_id"])
                    session.delete(acct)
                    return (
                        jsonify({"success": True, "msg": "Account has been deleted"}),
                        200,
                    )

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


def user_exists(session, username):
    return session.query(
        session.query(User).filter(User.username == username).exists()
    ).scalar()


def get_user_from_db(session, username):
    return session.query(User).filter_by(username=username).one()


def account_exists(session, acct_id):
    return session.query(
        session.query(Account).filter(Account.account_id == acct_id).exists()
    ).scalar()


def get_account_from_db(session, acct_id):
    return session.query(Account).filter_by(account_id=acct_id).one()


def account_type_valid(acct_type: int):
    if acct_type is None:
        return False
    for type in AccountType:
        if acct_type == type.value:
            return True
    return False


def string_blank(s: str):
    return s is None or s == ""


def main():
    print("Starting app...")
    config = {
        "DATABASE_CONNECTION_STRING": "sqlite:///../../databases/finance_tracker.db"
    }
    app = create_app(config)
    app.run(debug=True)


if __name__ == "__main__":
    main()
