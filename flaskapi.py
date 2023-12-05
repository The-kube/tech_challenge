from flask import Flask, json

users = [{"id": 1, "name": "bob"}, {"id": 2, "name": "john"}]

api = Flask(__name__)

@api.route('/users', methods=['GET'])
def get_users():
  return json.dumps(users)

@api.route('/users', methods=['POST'])
def post_users():
  return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run()