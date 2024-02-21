from flask import (Flask, jsonify, request, make_response,
                    abort, url_for, redirect)
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
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
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    
    abort(401)

@app.route('/sessions', methods=['DELETE'])
def logout():
    """Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
    abort(403)

@app.route('/profile', methods=['GET'])
def profile():
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
