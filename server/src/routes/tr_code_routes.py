from flask import Blueprint, jsonify
from utils.file_handler import TrCodeHandler

# 创建 Blueprint 实例，可以指定 URL 前缀
tr_code_bp = Blueprint("tr_code_bp", __name__)

# 实例化相关的处理器
tr_handler = TrCodeHandler()


@tr_code_bp.route("/trCode", methods=["GET"])
def all_trcode():
    """获取所有交易码"""
    response_object = {"status": "success", "data": tr_handler.read_tr_codes()}
    return jsonify(response_object)
