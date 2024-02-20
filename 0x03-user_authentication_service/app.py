from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH  = Auth()

app.route('/', methods=['GET'])
def index():
    """ a get method that return a jsonify string
    """
    return jsonify({"message": "Bienvenue"})

app.route('/users', methods=['POST'])
def users(email, password):
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "main":
    app.run(host="0.0.0.0", port="5000")