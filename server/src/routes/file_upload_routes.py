import os
import uuid
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from utils.file_handler import ExcelHandler

# 创建 Blueprint 实例
file_upload_bp = Blueprint("file_upload_bp", __name__)


@file_upload_bp.route("/upload/excel", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return jsonify({"error": "没有文件部分"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "没有选择文件"}), 400

    if file and ExcelHandler.allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        excel_filename_stem = os.path.splitext(original_filename)[
            0
        ]  # Get filename without extension

        unique_suffix = str(uuid.uuid4())
        # Keep original extension for saving temp file
        _, file_extension = os.path.splitext(original_filename)
        unique_temp_filename = f"{excel_filename_stem}_{unique_suffix}{file_extension}"

        # 使用 current_app 来访问应用配置
        filepath = os.path.join(
            current_app.config["UPLOAD_FOLDER"], unique_temp_filename
        )

        try:
            file.save(filepath)
            # Pass the excel_filename_stem for creating specific output subdirectories
            result = ExcelHandler.read_excel(filepath, excel_filename_stem)

            # 清理临时文件
            os.remove(filepath)

            if result["success"]:
                # result["message"] will contain the success message from process_file
                return jsonify(
                    {
                        "message": result.get("message", "文件处理成功"),
                        "data": result.get("data"),
                    }
                )  # data might be null
            else:
                return jsonify({"error": result["error"]}), 500

        except Exception as e:
            # 确保在发生异常时也尝试删除文件
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": f"处理文件时出错: {str(e)}"}), 500

    return jsonify({"error": "不允许的文件类型"}), 400
