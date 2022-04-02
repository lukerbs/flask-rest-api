from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, model
import argparse
import os

parser = argparse.ArgumentParser(description="Resets SQL database.")
parser.add_argument('-r', '--reset', type=str, metavar='', required=False, help='Enter true / false')
args = parser.parse_args()

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False )
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"UserDataAPI(name={name}, name={name}, gender={gender}, location={location })"

if args.reset == "true":
    try:
        os.system('rm database.db')
    except:
        pass
    db.create_all()
    print('New Database Created.')


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="User first and last name is required", required=True)
put_args.add_argument("age", type=int, help="User age")
put_args.add_argument("gender", type=str, help="User gender")
put_args.add_argument("location", type=str, help="User location")

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str, help="User first and last name is required")
user_update_args.add_argument("name", type=str, help="User first and last name is required")
user_update_args.add_argument("age", type=int, help="User age")
user_update_args.add_argument("gender", type=str, help="User gender")
user_update_args.add_argument("location", type=str, help="User location")


def user_not_found(user_id):
    if user_id not in users:
        abort(404, message="ABORTED: User does not exist.")

def user_already_exists(user_id):
    if user_id in users:
        abort(409, message="ABORTED: User already exists.")


resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'age': fields.Integer,
    'gender': fields.String,
    'location': fields.String
}

class UserDataAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User id does not exist")
        return result 

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = put_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="User id taken")

        user = UserModel(id=user_id, name=args['name'], age=args['age'], gender=args['gender'], location=args['location'] )
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User does not exist, cannot update")
        if args["name"]:
            result.name = args['name']
        if args["age"]:
            result.age = args['age']
        if args["gender"]:
            result.gender = args['gender']
        if args["location"]:
            result.location = args['location']

        db.session.commit()

        return result

    def delete(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User id does not exist")
        else:
            db.session.delete(result)
            db.session.commit()
            return '', 204


    #def post(self):
    #     return {"data":"Posted"}

api.add_resource(UserDataAPI, "/api/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True, port=8003)

