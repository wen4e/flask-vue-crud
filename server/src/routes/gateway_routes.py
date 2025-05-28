from flask import Blueprint, jsonify, request
from utils.gateway_handler import GatewayHandler

# 创建 Blueprint 实例
gateway_bp = Blueprint("gateway_bp", __name__, url_prefix="/gateway")

# 实例化处理器
gateway_handler = GatewayHandler()


@gateway_bp.route("/defaultQuery", methods=["GET"])
def query_default_gateway():
    """获取默认网关配置"""
    default_gateway = gateway_handler.get_default_gateway()
    return jsonify({"success": True, "data": default_gateway})


@gateway_bp.route("/change", methods=["POST"])
def change_gateway():
    """修改默认网关配置"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "缺少请求数据"}), 400

        # 确保请求包含必要字段
        if "gatewayUrl" not in data:
            return (
                jsonify({"success": False, "error": "缺少必要字段 gatewayUrl"}),
                400,
            )

        gateway_url = data.get("gatewayUrl")

        success = gateway_handler.set_default_gateway(gateway_url)
        if success:
            return jsonify({"success": True, "message": "默认网关修改成功"})
        else:
            return (
                jsonify({"success": False, "error": "默认网关修改失败"}),
                400,
            )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
