import requests
import json
import os
from flask import Response, stream_with_context


class TbspHandler:
    """处理TBSP API请求转发的工具类"""

    def __init__(self):
        # 获取当前文件所在目录路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取src目录路径
        src_dir = os.path.dirname(current_dir)
        # 构建gateway.json文件的完整路径
        self.gateway_path = os.path.join(src_dir, "data", "gateway.json")

    @property
    def base_url(self):
        """每次访问时重新从配置文件读取基础URL"""
        try:
            # 读取gateway.json文件
            with open(self.gateway_path, "r") as f:
                gateway_config = json.load(f)
                return gateway_config["default"]["value"]
        except Exception:
            # 出现异常时返回默认值
            return "http://10.20.29.157:7150"

    def proxy_request(self, path, method, headers=None, params=None, data=None):
        """
        将请求代理到目标服务器

        Args:
            path: 原始路径中去掉 /tbspApi 后的部分
            method: HTTP方法(GET, POST等)
            headers: 请求头
            params: URL参数
            data: 请求体数据

        Returns:
            代理后的响应
        """
        # 构建目标URL - 现在每次调用都会获取最新的base_url
        target_url = f"{self.base_url}/{path}" if path else self.base_url

        # 移除可能导致问题的请求头
        if headers:
            headers_copy = headers.copy()
            headers_copy.pop("Host", None)
            headers_copy.pop("Content-Length", None)
        else:
            headers_copy = {}

        try:
            # 发送请求到目标服务器
            response = requests.request(
                method=method,
                url=target_url,
                headers=headers_copy,
                params=params,
                data=data,
                stream=True,  # 使用流式响应
            )

            # 创建Flask响应对象，保持原始状态码和头信息
            flask_response = Response(
                stream_with_context(response.iter_content(chunk_size=1024)),
                status=response.status_code,
                content_type=response.headers.get("Content-Type", "text/plain"),
            )

            # 复制原始响应的头信息
            for key, value in response.headers.items():
                if key.lower() not in (
                    "content-encoding",
                    "transfer-encoding",
                    "content-length",
                ):
                    flask_response.headers[key] = value

            return flask_response

        except Exception as e:
            return {"success": False, "error": str(e)}, 500
