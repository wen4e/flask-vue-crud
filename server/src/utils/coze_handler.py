import requests
from .config import COZE_CONFIG


class CozeHandler:
    """
    用于处理与 Coze API 交互的类。
    """

    def __init__(self):
        """
        初始化 CozeHandler。
        从配置中加载 API 密钥和基础 URL。
        """
        self.api_key = COZE_CONFIG["api_key"]
        self.base_url = COZE_CONFIG["base_url"]
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def run_workflow(self, workflow_id: str, app_id: str, user_input: str):
        """
        运行 Coze 工作流。

        Args:
            workflow_id (str): 工作流 ID。
            app_id (str): 应用 ID。
            user_input (str): 用户输入。

        Returns:
            dict: 包含 API 调用结果的字典。
                  成功时: {"success": True, "data": response_data}
                  失败时: {"success": False, "error": error_message}
        """
        url = f"{self.base_url}/workflow/run"
        payload = {
            "workflow_id": workflow_id,
            "parameters": {"input": user_input},
            "app_id": app_id,
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()  # 如果请求失败 (状态码 4xx 或 5xx), 则抛出 HTTPError 异常
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            error_msg = f"Coze API 调用失败: {str(e)}"
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_details = e.response.json()
                    error_msg += f" - Details: {error_details}"
                except (
                    ValueError
                ):  # response.json() 可能会因为响应体不是有效的JSON而失败
                    error_msg += f" - Raw response: {e.response.text}"
            print(f"Error: {error_msg}")
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"处理 Coze API 响应时发生未知错误: {str(e)}"
            print(f"Error: {error_msg}")
            return {"success": False, "error": error_msg}
