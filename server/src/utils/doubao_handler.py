from openai import OpenAI
from .config import VOLC_CONFIG


class DoubaoHandler:
    def __init__(self):
        self.client = OpenAI(
            api_key=VOLC_CONFIG["ak"],  # 使用 ak 作为 api_key
            base_url="https://ark.cn-beijing.volces.com/api/v3",
        )
        self.system_message = {
            "role": "system",
            "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手",
        }

    def chat_completion(self, prompt, temperature=0.7, stream=False):
        try:
            messages = [self.system_message, {"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model="ep-20250122144359-6kmv5",
                messages=messages,
                temperature=temperature,
                max_tokens=4096,
                stream=stream,
            )

            if stream:
                return {"success": True, "data": response}

            return {"success": True, "data": response.choices[0].message.content}

        except Exception as e:
            error_msg = f"API调用失败: {str(e)}"
            print(f"Error: {error_msg}")
            return {"success": False, "error": error_msg}
