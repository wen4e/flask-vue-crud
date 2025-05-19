from cozepy import Coze, JWTAuth, JWTOAuthApp

# 从 config.py 导入配置字典
from .config import COZE_CONFIG


class CozeHandler:
    """
    使用 Coze 官方 Python SDK，通过 JWT OAuth 授权与 Coze OpenAPI 交互。
    配置信息统一通过 config.py 下的 COZE_CONFIG 获取。
    """

    def __init__(self):
        """
        初始化 CozeHandler，读取 config.py 中的所有 JWT 授权相关参数。
        COZE_CONFIG 示例:
        COZE_CONFIG = {
            "jwt_client_id": "your-client-id",
            "jwt_private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
            "jwt_public_key_id": "your-public-key-id",
            "base_url": "https://api.coze.cn/v1"  # 可选，默认用 api.coze.cn
        }
        """
        config = COZE_CONFIG

        # 读取 JWT 授权相关配置
        self.client_id = config.get("jwt_client_id")
        self.private_key = config.get("jwt_private_key")
        self.public_key_id = config.get("jwt_public_key_id")
        self.base_url = config.get("base_url")

        if not (self.client_id and self.private_key and self.public_key_id):
            raise RuntimeError(
                "COZE_CONFIG 配置缺失。请确认已配置 jwt_client_id、jwt_private_key、jwt_public_key_id。"
            )

        # 实例化 JWT OAuth 应用
        self.jwt_oauth_app = JWTOAuthApp(
            client_id=self.client_id,
            private_key=self.private_key,
            public_key_id=self.public_key_id,
            base_url=self.base_url,
        )

        # 初始化 Coze SDK 客户端，使用 JWT 授权
        self.coze_client = Coze(
            auth=JWTAuth(oauth_app=self.jwt_oauth_app), base_url=self.base_url
        )

    def run_workflow(self, payload: dict):
        """
        调用 Coze 官方 SDK 运行工作流。只需保证 payload 至少有 workflow_id，其它参数原样透传。
        Args:
            payload (dict): 结构包含 workflow_id 及其它任意参数
        Returns:
            dict: {"success": True, "data": ...} 或 {"success": False, "error": ...}
        """
        try:
            if not payload.get("workflow_id"):
                return {"success": False, "error": "参数缺失：workflow_id"}

            workflow_result = self.coze_client.workflows.runs.create(**payload)
            try:
                # 尝试使用对象的to_dict方法(如果存在)
                if hasattr(workflow_result, "to_dict"):
                    result_data = workflow_result.to_dict()
                # 或者使用__dict__属性
                elif hasattr(workflow_result, "__dict__"):
                    result_data = workflow_result.__dict__
                # 如果对象本身是可JSON序列化的
                else:
                    result_data = workflow_result

                # 返回 SDK 的 data 字段（如果有），否则原样返回
                return {
                    "success": True,
                    "data": result_data.get("data", result_data),
                }
            except Exception as json_error:
                return {"success": False, "error": f"JSON序列化失败: {str(json_error)}"}
        except Exception as e:
            return {"success": False, "error": f"Coze JWT SDK 调用失败: {str(e)}"}
