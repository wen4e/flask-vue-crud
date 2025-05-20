from flask import Blueprint, request
from utils.tbsp_handler import TbspHandler

# 创建Blueprint实例
tbsp_bp = Blueprint("tbsp_bp", __name__)

# 实例化处理器
tbsp_handler = TbspHandler()


@tbsp_bp.route(
    "/tbspApi",
    defaults={"path": ""},
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
)
@tbsp_bp.route(
    "/tbspApi/<path:path>",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
)
def proxy_tbsp_api(path):
    """
    代理所有以/tbspApi开头的请求到目标服务器
    例如：/tbspApi/a/b 将被转发到 http://10.20.29.157:7150/a/b
    """
    # 获取请求方法、请求头和各种参数
    method = request.method
    headers = {key: value for key, value in request.headers.items()}
    params = request.args
    data = request.get_data()

    # 调用处理器执行代理请求
    return tbsp_handler.proxy_request(
        path=path, method=method, headers=headers, params=params, data=data
    )
