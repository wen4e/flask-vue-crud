import os
import json
from typing import Dict, Any


class GatewayHandler:
    """处理网关配置的工具类"""

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.dirname(current_dir)
        self.gateway_file_path = os.path.join(src_dir, "data", "gateway.json")

    def _read_gateways(self) -> Dict[str, Any]:
        """读取网关配置文件"""
        try:
            with open(self.gateway_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                # 返回整个json内容
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或格式错误，返回空字典
            return {}

    def _write_data(self, data: Dict[str, Any]) -> bool:
        """写入完整配置数据到文件"""
        try:
            with open(self.gateway_file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_default_gateway(self) -> str:
        """获取默认网关配置"""
        data = self._read_gateways()
        # 如果存在 default 键且其值是一个包含 value 的字典，则返回该值
        if (
            "default" in data
            and isinstance(data["default"], dict)
            and "value" in data["default"]
        ):
            return data["default"]["value"]
        # 如果没有找到默认值，返回空字符串
        return ""

    def set_default_gateway(self, gateway_url: str) -> bool:
        """设置默认网关"""
        data = self._read_gateways()

        # 确保数据中有 default 键
        if "default" not in data:
            data["default"] = {}

        # 更新默认网关值
        data["default"]["value"] = gateway_url

        # 使用新的写入方法
        return self._write_data(data)
