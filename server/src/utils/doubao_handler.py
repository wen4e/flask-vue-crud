from openai import OpenAI
from .config import VOLC_CONFIG


class DoubaoHandler:
    def __init__(self):
        self.client = OpenAI(
            api_key=VOLC_CONFIG["ak"],  # 使用 ak 作为 api_key
            base_url=VOLC_CONFIG["baseUrl"],  # 使用 baseUrl 作为 base_url
        )
        self.system_message = {
            "role": "system",
            "content": "You are a helpful assistant",
        }

    def chat_completion(self, prompt, temperature=0.7, stream=False):
        try:
            # messages = [self.system_message, {"role": "user", "content": prompt}]
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=VOLC_CONFIG["mode"],
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
