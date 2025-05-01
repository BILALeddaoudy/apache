from flask import Flask, request, jsonify
from user_manager import UserManager

app = Flask(__name__)
user_manager = UserManager()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    result = user_manager.register_user(name, username, password, confirm_password)
    return jsonify({"message": result})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    result = user_manager.login_user(username, password)
    return jsonify({"message": result})

@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    user = user_manager.get_user(username)
    if user:
        return jsonify({"name": user[0], "username": user[1]})
    else:
        return jsonify({"message": "User not found."}), 404

@app.route("/user/<username>", methods=["PUT"])
def update_user(username):
    data = request.json
    new_name = data.get("name")
    new_password = data.get("password")
    confirm_password = data.get("confirm_password")

    result = user_manager.update_user(username, new_name, new_password, confirm_password)
    return jsonify({"message": result})

@app.route("/users", methods=["GET"])
def list_users():
    users = user_manager.list_users()
    return jsonify({"users": [{"name": u[0], "username": u[1]} for u in users]})

if __name__ == "__main__":
    app.run(debug=True)
