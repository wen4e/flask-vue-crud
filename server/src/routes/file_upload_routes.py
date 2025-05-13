import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from utils.file_handler import ExcelHandler

file_upload_bp = Blueprint(
    "file_upload_bp", __name__
)  # 没有统一的 url_prefix，因为原始路由是 /upload/excel


@file_upload_bp.route("/upload/excel", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return jsonify({"error": "没有文件部分"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "没有选择文件"}), 400

    if file and ExcelHandler.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # UPLOAD_FOLDER 从 app.config 获取
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        # 确保上传目录存在
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        unique_filename = f"{str(uuid.uuid4())}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)

        try:
            file.save(filepath)
            result = ExcelHandler.read_excel(
                filepath
            )  # ExcelHandler 的方法是静态的或在此处实例化

            # 清理临时文件
            if os.path.exists(filepath):
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
