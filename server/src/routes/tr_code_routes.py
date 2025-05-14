from flask import Blueprint, jsonify
from utils.file_handler import TrCodeHandler  # 确保路径正确，或者已添加到 sys.path

# 创建 Blueprint 实例，可以指定 URL 前缀
tr_code_bp = Blueprint("tr_code_bp", __name__)

# 实例化相关的处理器
# 如果处理器是无状态的或者其状态与应用实例无关，可以在此实例化
# 否则，您可能需要使用应用工厂模式传递应用上下文或处理器实例
tr_handler = TrCodeHandler()


@tr_code_bp.route("/trCode", methods=["GET"])
def all_trcode():
    """获取所有交易码"""
    response_object = {"status": "success", "data": tr_handler.read_tr_codes()}
    return jsonify(response_object)


# 可以将其他与交易码相关的路由也放在这里
