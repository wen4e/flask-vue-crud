from flask import Blueprint, jsonify, request
from utils.code_handler import CodeHandler  # 确保 CodeHandler 可以被正确导入

# 创建 Blueprint 实例
create_page_bp = Blueprint("create_page_bp", __name__)

# 实例化处理器
code_handler = CodeHandler()


@create_page_bp.route("/createPage", methods=["POST"])
def create_page():
    data = request.get_json()
    if not data or "pageName" not in data:
        return jsonify({"error": "缺少必要的pageName参数"}), 400

    result = code_handler.create_page(data["pageName"])

    if result["success"]:
        return jsonify({"message": "请求成功", "data": result["data"]})
    else:
        return jsonify({"error": result["error"]}), 500
