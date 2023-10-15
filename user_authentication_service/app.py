#!/usr/bin/env python3
""" This script defines API endpoints for user authentication.
"""

from flask import Flask, jsonify, redirect, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def root() -> str:
    """ Handle root endpoint, returning a welcome message.
    """
    return jsonify({'message': 'Welcome'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ Handle user registration.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'User created'})
    except ValueError:
        return jsonify({"message": "Email already registered"}, 400)


@app.route("/sessions", methods=["POST"])
def login() -> str:
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({
            "email": email,
            "message": "logged in",
            "session_id": session_id
        })
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ Handle user logout and session termination.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    logged_in_user = AUTH.get_user_from_session_id(session_id)
    if not logged_in_user:
        abort(403)
    AUTH.destroy_session(logged_in_user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ Retrieve user profile information.
    """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    message = {"email": user.email}
    return jsonify(message), 200


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    """ Handle password reset request.
    """
    try:
        email = request.form.get('email')
    except KeyError:
        abort(403)
    try:
        reset_user_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    message = {"email": email, "reset_token": reset_user_token}
    return jsonify(message), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=True)
def update_password() -> str:
    """ Handle password update after a reset request.
    """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    message = {"email": email, "message": "Password updated"}
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
