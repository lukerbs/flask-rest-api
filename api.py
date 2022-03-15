from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, model

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False )
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"UserDataAPI(name={name}, name={name}, gender={gender}, location={location })"


put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="User first and last name is required", required=True)
put_args.add_argument("age", type=int, help="User age")
put_args.add_argument("gender", type=str, help="User gender")
put_args.add_argument("location", type=str, help="User location")




def user_not_found(user_id):
    if user_id not in users:
        abort(404, message="ABORTED: User does not exist.")

def user_already_exists(user_id):
    if user_id in users:
        abort(409, message="ABORTED: User already exists.")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'gender': fields.String,
    'location': fields.String
}

class UserDataAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        result = UserModel.query.get(id=user_id)
        return result 

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = put_args.parse_args() 
        user = UserModel(id=user_id, name=args['name'], age=args['age'], gender=args['gender'], location=args['location'] )
        db.session.add(user)
        db.session.commit()
        return user, 201

    def delete(self, user_id):
        user_not_found(user_id)
        del users[user_id]
        print('Deleted User.')
        return '', 204


    # def post(self):
    #     return {"data":"Posted"}

api.add_resource(UserDataAPI, "/api/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True, port=8003)

