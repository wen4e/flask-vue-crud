from flask import Blueprint, jsonify, request
from utils.openai_handler import OpenAIHandler  # 确保 OpenAIHandler 可以被正确导入

# 创建 Blueprint 实例
chat_bp = Blueprint("chat_bp", __name__)

# 实例化处理器
openai_handler = OpenAIHandler()


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "缺少必要的prompt参数"}), 400

    result = openai_handler.chat_completion(data["prompt"])

    if result["success"]:
        return jsonify({"message": "请求成功", "data": result["data"]})
    else:
        return jsonify({"error": result["error"]}), 500
