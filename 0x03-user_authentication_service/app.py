from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app = Flask(__name__)
AUTH  = Auth()


@app.route('/', methods=['GET'])
def index():
    """ a get method that return a jsonify string
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users():
    """ a post method to register users
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except:
        return jsonify({"message": "email already registered"}), 400
    
@app.route('/sessions', methods=['POST'])
def login():
    """send a post request to login a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        if email and password:
            AUTH.valid_login(email, password)
            session_id = AUTH.create_session(email)
            response = make_response(jsonify({"email": email, "message": "logged in"}))
            response.set_cookie('session_id', session_id)
            return response
        abort(401)
    except Exception:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
