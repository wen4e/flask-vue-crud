import uuid
import os
import sys
from werkzeug.utils import secure_filename


current_dir = os.path.dirname(os.path.abspath(__file__))  # => server/src
server_dir = os.path.dirname(current_dir)  # => server

# 确保能找到 server/src 下的 utils
sys.path.append(current_dir)
# 确保能找到 server/config.py
sys.path.append(server_dir)

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from utils.file_handler import TrCodeHandler, ExcelHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 实例化应用
app = Flask(
    __name__,
    static_folder="static",  # 前端静态文件所在文件夹名称
    static_url_path="",  # 设置成 '' 使得访问静态文件时的URL是根路径
)

# 启用 CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# 添加文件上传配置
UPLOAD_FOLDER = os.path.join(current_dir, "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/upload/excel", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return jsonify({"error": "没有文件部分"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "没有选择文件"}), 400

    if file and ExcelHandler.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{str(uuid.uuid4())}_{filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

        try:
            file.save(filepath)
            result = ExcelHandler.read_excel(filepath)

            # 清理临时文件
            os.remove(filepath)

            if result["success"]:
                return jsonify({"message": "文件上传成功", "data": result["data"]})
            else:
                return jsonify({"error": result["error"]}), 500

        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": f"处理文件时出错: {str(e)}"}), 500

    return jsonify({"error": "不允许的文件类型"}), 400


# 实例化处理器
tr_handler = TrCodeHandler()


@app.route("/trCode", methods=["GET"])
def all_trcode():
    """获取所有交易码"""
    response_object = {"status": "success", "data": tr_handler.read_tr_codes()}
    return jsonify(response_object)


# 在现有import下添加
from utils.doubao_handler import DoubaoHandler

# 在app实例化后添加
doubao_handler = DoubaoHandler()


# 添加新的路由
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "缺少必要的prompt参数"}), 400

    result = doubao_handler.chat_completion(data["prompt"])

    if result["success"]:
        return jsonify({"message": "请求成功", "data": result["data"]})
    else:
        return jsonify({"error": result["error"]}), 500


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    # 如果请求的路径在静态文件夹中（static/...）存在，就直接返回该文件
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # 否则返回index.html，让Vue前端去处理路由
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
