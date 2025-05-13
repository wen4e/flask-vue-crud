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
from utils.openai_handler import OpenAIHandler
from utils.code_handler import CodeHandler


# 从 routes 包导入 Blueprints
from routes import coze_bp  # 导入 coze_bp


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
openai_handler = OpenAIHandler()
code_handler = CodeHandler()


@app.route(
    "/trCode", methods=["GET"]
)  # 这个路由可以保留在这里，或者也移到 tr_code_routes.py
def all_trcode():
    """获取所有交易码"""
    response_object = {"status": "success", "data": tr_handler.read_tr_codes()}
    return jsonify(response_object)


# chat接口
@app.route("/chat", methods=["POST"])  # 这个路由可以保留在这里，或者移到 chat_routes.py
def chat():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "缺少必要的prompt参数"}), 400

    result = openai_handler.chat_completion(data["prompt"])

    if result["success"]:
        return jsonify({"message": "请求成功", "data": result["data"]})
    else:
        return jsonify({"error": result["error"]}), 500


# 创建页面
@app.route(
    "/createPage", methods=["POST"]
)  # 这个路由可以保留在这里，或者移到 page_creation_routes.py
def create_page():
    data = request.get_json()
    if not data or "pageName" not in data:
        return jsonify({"error": "缺少必要的pageName参数"}), 400

    result = code_handler.create_page(data["pageName"])

    if result["success"]:
        return jsonify({"message": "请求成功", "data": result["data"]})
    else:
        return jsonify({"error": result["error"]}), 500


# 注册 Blueprints
app.register_blueprint(coze_bp)  # coze_bp 的路由是 /cozeApp，没有统一前缀


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
