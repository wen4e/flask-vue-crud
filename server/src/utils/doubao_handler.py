from volcenginesdkarkruntime import Ark
from .config import VOLC_CONFIG


class DoubaoHandler:
    def __init__(self):
        # 从环境变量获取密钥，便于管理和安全性
        self.client = Ark(
            ak=VOLC_CONFIG["ak"],
            sk=VOLC_CONFIG["sk"],
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            timeout=120,
            max_retries=2,
        )
        self.system_message = {
            "role": "system",
            "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手",
        }

    def chat_completion(self, prompt, temperature=0.7, stream=False):
        try:
            messages = [self.system_message, {"role": "user", "content": prompt}]
            print(messages)
            # 验证凭证是否配置
            if not self.client.ak or not self.client.sk:
                return {"success": False, "error": "API凭证未正确配置"}

            response = self.client.chat.completions.create(
                model="ep-20250122144359-6kmv5",
                messages=messages,
                temperature=temperature,
                max_tokens=4096,
                stream=stream,
                extra_headers={"x-is-encrypted": "true"},
            )

            print(response)

            if stream:
                return {"success": True, "data": response}

            return {"success": True, "data": response.choices[0].message.content}

        except Exception as e:
            error_msg = f"API调用失败: {str(e)}"
            print(f"Error: {error_msg}")  # 添加日志
            return {"success": False, "error": error_msg}
