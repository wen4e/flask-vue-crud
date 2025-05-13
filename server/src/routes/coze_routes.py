from flask import Blueprint, jsonify, request
from utils.coze_handler import CozeHandler  # 确保 CozeHandler 可以被正确导入

# 创建 Blueprint 实例
coze_bp = Blueprint("coze_bp", __name__)

# 实例化处理器
# 如果 CozeHandler 是无状态的，或者其状态与应用实例无关，可以在此实例化
# 否则，您可能需要使用应用工厂模式或在 app 创建时传递实例
coze_handler = CozeHandler()


@coze_bp.route("/cozeApp", methods=["POST"])
def coze_app_workflow():
    """
    调用 Coze 工作流接口。
    从请求体中获取完整的 payload 对象。
    payload 结构应为:
    {
        "workflow_id": "...",
        "app_id": "...",
        "parameters": {}
    }
    """
    payload = request.get_json()

    if not payload:
        return jsonify({"error": "缺少请求体"}), 400

    # 直接将接收到的 payload 传递给 coze_handler
    result = coze_handler.run_workflow(payload=payload)

    if result["success"]:
        # 直接返回其 data 部分
        data_to_return = result["data"]
        if isinstance(data_to_return, dict) and "debug_url" in data_to_return:
            del data_to_return["debug_url"]
        return jsonify(data_to_return)
    else:
        return jsonify({"error": result["error"]}), 500
