from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import ConfigInMemoryDataBase
import json

app = Flask(__name__)


def change_database(conf):
    if conf == "mysql":
        app.config.from_object("config.ConfigMySQL")
    elif conf == "sqlite":
        app.config.from_object("config.ConfigSQLite")
    elif conf == "in_memory":
        global in_memory_db
        in_memory_db = ConfigInMemoryDataBase().db
    return conf


database_method = change_database("in_memory")

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    patronymic = db.Column(db.String(50))

    def __init__(self, firstname, lastname, patronymic):
        self.firstname = firstname
        self.lastname = lastname
        self.patronymic = patronymic


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname', 'patronymic')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/user', methods=['POST'])
def add_user():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    patronymic = request.json['patronymic']

    if database_method == "mysql" or database_method == "sqlite":
        user = User(firstname, lastname, patronymic)
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user)

    elif database_method == "in_memory":
        return json.dumps(in_memory_db.add_user(firstname, lastname, patronymic))


@app.route('/user', methods=['GET'])
def get_all_users():
    if database_method == "mysql" or database_method == "sqlite":
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result)
    elif database_method == "in_memory":
        return json.dumps(in_memory_db.get_all_users())


@app.route('/user/<int:id>', methods=['GET'])
def get_users_by_id(id):
    if database_method == "mysql" or database_method == "sqlite":
        user = User.query.get(id)
        return user_schema.jsonify(user)
    elif database_method == "in_memory":
        return json.dumps(in_memory_db.get_user_by_id(id))


@app.route('/user/<int:id>', methods=['PUT'])
def change_user(id):
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    patronymic = request.json['patronymic']

    if database_method == "mysql" or database_method == "sqlite":
        user = User.query.get(id)
        user.firstname = firstname
        user.lastname = lastname
        user.patronymic = patronymic
        db.session.commit()
        return user_schema.jsonify(user)
    elif database_method == "in_memory":
        return json.dumps(in_memory_db.change_user(id, firstname, lastname, patronymic))


@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    if database_method == "mysql" or database_method == "sqlite":
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return user_schema.jsonify(user)
    elif database_method == "in_memory":
        return json.dumps(in_memory_db.delete_user(id))

@app.route('/user', methods=['DELETE'])
def delete_all():
    if database_method == "mysql" or database_method == "sqlite":
        return user_schema.jsonify({"message": "coming soon"})
    elif database_method == "in_memory":
        return json.dumps(in_memory_db.delete_all())


if __name__ == '__main__':
    app.run(debug=True)
