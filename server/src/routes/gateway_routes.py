from flask import Blueprint, jsonify, request
from utils.gateway_handler import GatewayHandler

# 创建 Blueprint 实例
gateway_bp = Blueprint("gateway_bp", __name__)

# 实例化处理器
gateway_handler = GatewayHandler()


@gateway_bp.route("/gateway/query", methods=["GET"])
def query_gateways():
    """获取所有网关配置"""
    gateways = gateway_handler.query_gateways()
    return jsonify({"success": True, "data": gateways})


@gateway_bp.route("/gateway/add", methods=["POST"])
def add_gateway():
    """添加新网关配置"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "缺少请求数据"}), 400

        # 确保请求包含必要字段
        if "gatewayUrl" not in data or "gatewayName" not in data:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "缺少必要字段 gatewayUrl 或 gatewayName",
                    }
                ),
                400,
            )

        # 转换前端参数格式为配置文件中使用的格式
        gateway = {"value": data.get("gatewayUrl"), "label": data.get("gatewayName")}

        success = gateway_handler.add_gateway(gateway)
        if success:
            return jsonify({"success": True, "message": "网关添加成功"})
        else:
            return (
                jsonify(
                    {"success": False, "error": "网关添加失败，可能已存在相同URL的网关"}
                ),
                400,
            )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@gateway_bp.route("/gateway/change", methods=["POST"])
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


@gateway_bp.route("/gateway/delete", methods=["POST"])
def delete_gateway():
    """删除网关配置"""
    try:
        data = request.get_json()
        if not data or "gatewayUrl" not in data:
            return jsonify({"success": False, "error": "缺少要删除的网关URL"}), 400

        # 获取需要删除的网关URL
        gateway_url = data.get("gatewayUrl")

        # 调用处理器删除网关
        success = gateway_handler.delete_gateway(gateway_url)

        if success:
            return jsonify({"success": True, "message": "网关删除成功"})
        else:
            return (
                jsonify({"success": False, "error": "网关删除失败，可能不存在该网关"}),
                400,
            )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
