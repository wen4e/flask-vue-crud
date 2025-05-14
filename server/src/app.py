import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))  # => server/src
server_dir = os.path.dirname(current_dir)  # => server

# 确保能找到 server/src 下的 utils
sys.path.append(current_dir)
# 确保能找到 server/config.py
sys.path.append(server_dir)

from flask import Flask, send_from_directory
from flask_cors import CORS

# 从 routes 包导入 Blueprints
from routes import coze_bp, create_page_bp, chat_bp, file_upload_bp, tr_code_bp


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


# 注册 Blueprints
app.register_blueprint(coze_bp)
app.register_blueprint(create_page_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(file_upload_bp)
app.register_blueprint(tr_code_bp)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
