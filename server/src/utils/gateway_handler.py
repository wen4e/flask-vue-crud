import os
import json
from typing import List, Dict, Any, Optional


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

    def query_gateways(self) -> List[Dict[str, str]]:
        """获取所有网关配置"""
        data = self._read_gateways()
        return data.get("list", [])

    def add_gateway(self, gateway: Dict[str, str]) -> bool:
        """添加新网关配置"""
        # 验证必要字段
        if not gateway.get("value") or not gateway.get("label"):
            return False

        # 读取完整的配置数据
        data = self._read_gateways()

        # 确保数据中有 list 键
        if "list" not in data:
            data["list"] = []

        # 检查是否已存在相同值的网关
        if any(g.get("value") == gateway.get("value") for g in data["list"]):
            return False

        # 将新网关添加到列表末尾
        data["list"].append(gateway)

        # 保存完整的配置数据
        return self._write_data(data)

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

    def delete_gateway(self, value: str) -> bool:
        """删除网关配置"""
        # 读取完整的配置数据
        data = self._read_gateways()

        # 如果不存在list键或list为空，直接返回False
        if "list" not in data or not data["list"]:
            return False

        # 记录原始长度
        original_length = len(data["list"])

        # 过滤掉要删除的项
        data["list"] = [g for g in data["list"] if g.get("value") != value]

        # 只有当列表长度变化时才写入数据（说明有删除操作）
        if len(data["list"]) < original_length:
            return self._write_data(data)

        return False
