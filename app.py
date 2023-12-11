from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
import socket
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

# Function to fetch hostname and ip 
def fetchDetails():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return str(hostname), str(host_ip)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email}

# Connect to database
tries = 200
while tries > 0:
    try:
        db.create_all()
        tries = 0
    except:
        tries += -1
        print('Failed to connect to database. Waiting and then trying again (try countdown: %s)' % tries)
        time.sleep(3)  # Wait a bit until database is loaded

#db.create_all()
#""" Creating Database with App Context"""
#def create_db():
#    with app.app_context():
#        db.create_all()

# create a user
@app.route('/user', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'user created'}), 201)
  except:
    return make_response(jsonify({'message': 'error creating user'}), 500)

@app.route('/health', methods=['GET'])
def health():
    return make_response(jsonify(
      {'status': 'UP'}), 201)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except:
    return make_response(jsonify({'message': 'error retrieving list'}), 404)

# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
  except:
    return make_response(jsonify({'message': 'error: user not found'}), 404)

# update a user
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error updating user'}), 500)

# delete a user
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except:
    return make_response(jsonify({'message': 'error deleting user'}), 500)

@app.route("/details")
def details():
    hostname, ip = fetchDetails()
    return make_response(jsonify(HOSTNAME=hostname, IP=ip))
#if __name__ == '__main__':
#    create_db()
#    app.run(port = 5000, debug=True)