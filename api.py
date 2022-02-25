from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

put_args = reqparse.RequestParser()
put_args.add_argument("name", type=str, help="User first and last name is required", required=True)
put_args.add_argument("age", type=int, help="User age")
put_args.add_argument("gender", type=str, help="User gender")
put_args.add_argument("location", type=str, help="User location")


# users = {
#     "4150":{"name":"Luke", "age":26, "gender":"Male", "location":"San Juan Bautista"},
#     "5877":{"name":"Bella", "age":25, "gender":"Female", "location":"Gilroy"}
#     }
users = {}

class HelloWorld(Resource):
    def get(self, user_id):
        return users[user_id]
    def put(self, user_id):
        args = put_args.parse_args()
        users[user_id] = args
        return users[user_id], 201

    # def post(self):
    #     return {"data":"Posted"}

api.add_resource(HelloWorld, "/api/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True, port=8003)

