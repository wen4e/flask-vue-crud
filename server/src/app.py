import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from .utils.file_handler import JsonFileHandler
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

# 实例化应用
app = Flask(__name__)
app.config.from_object(config["development"])

# 启用 CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# 实例化文件处理器
file_handler = JsonFileHandler()


# 健康检查路由
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@app.route("/books", methods=["GET", "POST"])
def all_books():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        new_book = {
            "id": uuid.uuid4().hex,
            "title": post_data.get("title"),
            "author": post_data.get("author"),
            "read": post_data.get("read"),
        }
        file_handler.add_book(new_book)
        response_object["message"] = "Book added!"
    else:
        response_object["books"] = file_handler.read_books()
    return jsonify(response_object)


@app.route("/books/<book_id>", methods=["PUT", "DELETE"])
def single_book(book_id):
    response_object = {"status": "success"}
    if request.method == "PUT":
        post_data = request.get_json()
        updated_book = {
            "id": book_id,
            "title": post_data.get("title"),
            "author": post_data.get("author"),
            "read": post_data.get("read"),
        }
        file_handler.update_book(book_id, updated_book)
        response_object["message"] = "Book updated!"
    if request.method == "DELETE":
        file_handler.remove_book(book_id)
        response_object["message"] = "Book removed!"
    return jsonify(response_object)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
