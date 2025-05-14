import json
import os
import pandas as pd
import random
import string


class ExcelHandler:
    ALLOWED_EXTENSIONS = {"xlsx", "xls"}
    # 用于存储生成的JSON文件的目录
    JSON_OUTPUT_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
    )
    DTO_COUNT = 15  # 默认生成的DTO对象数量

    @staticmethod
    def allowed_file(filename):
        """检查文件扩展名是否允许"""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ExcelHandler.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def generate_mock_data(data_type: str, key_name: str = ""):
        """根据类型和键名生成模拟数据。"""
        t = data_type.strip().lower()
        if t in ("int", "integer", "number"):
            return random.randint(0, 100)
        if t in ("float", "double"):
            return round(random.uniform(0, 1000), 2)
        if t == "boolean":
            return random.choice([True, False])
        if t == "string":
            if key_name.endswith(("No", "Nos")):
                return "".join(random.choices(string.digits, k=15))
            if key_name.endswith("Date"):
                return "".join(random.choices(string.digits, k=8))
            if key_name == "currency":
                return "01"
            if key_name == "organizationNos":
                return "".join(random.choices(string.digits, k=4))
            if key_name == "directAtti":
                return random.choice(["1", "0"])
            if key_name == "tagIds":
                return "".join(random.choices(string.digits, k=3))
            if key_name.endswith("Name"):
                return "恒生电子股份有限公司"  # 示例，考虑使其可配置或更多样化
            if key_name.endswith("count"):
                return "".join(random.choices(string.digits, k=3))
            if key_name.endswith(("Bal", "Amt")):
                return "{:.2f}".format(random.uniform(0, 999.99))
            if key_name.endswith("Num"):
                return "".join(random.choices(string.digits, k=3))
            if key_name == "percent":
                return "{:.4f}".format(random.uniform(0, 1))
            return "".join(random.choices(string.ascii_letters + string.digits, k=10))
        return None

    @staticmethod
    def process_sheet_data(df: pd.DataFrame, dto_count: int = DTO_COUNT) -> dict:
        """处理工作表DataFrame以提取接口参数并生成JSON模拟数据。"""
        result = {
            "requestParams": {},
            "responseParams": {
                "respCode": "000000000000",
                "respEx": None,
                "respMsg": "交易成功",
                "respStatus": "S",
                "respType": "S",
            },
        }
        # 仅当 dto_count > 0 时初始化 dtos
        if dto_count > 0:
            result["responseParams"]["dtos"] = [{} for _ in range(dto_count)]
        else:
            result["responseParams"]["dtos"] = []

        mode = None  # 可以是 "request"、"response" 或 "dto"
        header_found = False  # 在当前模式下找到“属性名”或“类型”后为True

        for _, row in df.iterrows():
            if row.empty or pd.isna(row.iloc[0]):  # 跳过空行
                continue

            first_cell_value = str(row.iloc[0]).strip()

            if first_cell_value == "入参":
                mode = "request"
                header_found = False
                continue
            if first_cell_value == "返回":
                mode = "response"
                header_found = False
                continue
            if "DTO" in first_cell_value and mode == "response":  # DTO 是响应的一部分
                mode = "dto"
                header_found = False
                continue

            if mode and not header_found:
                # 检查当前行是否为标题行
                if first_cell_value in (
                    "属性名",
                    "类型",
                ):  # 假设这些是标题指示符
                    header_found = True
                continue  # 在当前模式下找到标题之前继续跳过

            if not mode or not header_found:  # 如果未处于某种模式或尚未找到标题，则跳过
                continue

            key_name = first_cell_value
            data_type = None
            if len(row) > 1 and not pd.isna(row.iloc[1]):
                data_type = str(row.iloc[1]).strip()

            if not key_name or not data_type:  # 如果 key_name 或 data_type 缺失，则跳过
                continue

            mock_value = ExcelHandler.generate_mock_data(data_type, key_name)

            if mode == "request":
                result["requestParams"][key_name] = mock_value
            elif mode == "response":
                if key_name != "dtos":  # dtos 是一个特殊键，单独处理
                    result["responseParams"][key_name] = mock_value
            elif mode == "dto":
                if result["responseParams"]["dtos"]:  # 检查 dtos 列表是否存在且不为空
                    for dto_item in result["responseParams"]["dtos"]:
                        dto_item[key_name] = mock_value

        # 如果 dtos 已初始化但所有项都为空，则进行清理
        if "dtos" in result["responseParams"] and all(
            not item for item in result["responseParams"]["dtos"]
        ):
            result["responseParams"].pop("dtos", None)
        elif (
            "dtos" in result["responseParams"] and not result["responseParams"]["dtos"]
        ):  # 如果初始化为空列表
            result["responseParams"].pop("dtos", None)

        return result

    @staticmethod
    def save_to_json(data, sheet_name, excel_filename_stem):
        """保存数据为JSON文件到data目录中"""
        try:
            # target_dir = os.path.join(ExcelHandler.JSON_OUTPUT_DIR, excel_filename_stem) # 旧的路径逻辑
            target_dir = ExcelHandler.JSON_OUTPUT_DIR  # 直接使用data目录
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)  # 如果data目录不存在，则创建

            # 为了避免不同Excel文件的同名sheet导致文件覆盖，
            # 建议在文件名中加入Excel文件名作为前缀。
            # 如果不希望加入前缀，可以直接使用: json_filename = f"{sheet_name}.json"
            # 但请注意，这可能导致文件被覆盖。
            json_filename = f"{sheet_name}.json"
            json_path = os.path.join(target_dir, json_filename)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {"success": True, "file_path": json_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def process_file(file_path, excel_filename_stem):
        """处理Excel文件, 为每个符合条件的sheet生成JSON文件"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            engine = "xlrd" if file_extension == ".xls" else "openpyxl"

            xls = pd.ExcelFile(file_path, engine=engine)

            # 需要排除处理的工作表
            excluded_sheets = ("报文头说明", "接口目录")
            processed_files_count = 0

            for sheet_name in xls.sheet_names:
                if sheet_name in excluded_sheets:
                    continue

                # 解析工作表时不使用标题行，以便我们可以根据单元格内容定义结构
                df = xls.parse(sheet_name=sheet_name, header=None)

                json_data = ExcelHandler.process_sheet_data(df, ExcelHandler.DTO_COUNT)

                save_result = ExcelHandler.save_to_json(
                    json_data, sheet_name, excel_filename_stem
                )
                if not save_result["success"]:
                    # 如果一个工作表保存失败，我们可以停止或收集错误
                    # 目前，返回遇到的第一个错误
                    return {
                        "success": False,
                        "error": f"Failed to save JSON for sheet {sheet_name}: {save_result['error']}",
                    }
                processed_files_count += 1

            if processed_files_count == 0:
                return {
                    "success": False,
                    "error": "No eligible sheets found for processing in the Excel file.",
                }

            return {
                "success": True,
                # 更新成功消息中的路径
                "message": f"Successfully processed {processed_files_count} sheet(s). JSON files saved in '{ExcelHandler.JSON_OUTPUT_DIR}'.",
            }
        except Exception as e:
            return {"success": False, "error": f"Error processing Excel file: {str(e)}"}

    @staticmethod
    def read_excel(file_path, excel_filename_stem):
        """读取Excel文件并处理, 调用 process_file"""
        try:
            # process_file 现在处理核心逻辑和保存JSON文件
            result = ExcelHandler.process_file(file_path, excel_filename_stem)
            return result  # process_file 返回一个包含成功状态和消息/错误的字典
        except Exception as e:
            return {"success": False, "error": str(e)}


# 获取data文件夹下的tr.json文件
# 如果 tr.json 的来源或结构根据新的 Excel 处理逻辑发生变化，则此类可能需要调整。
# 如果处理名为 "tr" 的工作表，则新逻辑将生成一个 tr.json。
class TrCodeHandler:
    def __init__(self):
        # 假设如果 tr.json 是由新逻辑生成的，它将位于以 excel 文件名命名的子文件夹中。
        # 如果其生成路径是动态的，这可能需要一种更强大的方法来定位 tr.json。
        # 目前，假设它可能直接位于 JSON_OUTPUT_DIR 或已知的子文件夹中。
        # 这部分是推测性的，因为新逻辑并未明确创建顶层 tr.json。
        # 如果 tr.json 是从名为 'tr' 的工作表（在 'example.xlsx' excel 文件中）生成的，
        # 它将位于 .../json_output/example/tr.json
        # 原始的 TrCodeHandler 在 server/src/data/tr.json 中查找
        # 这需要澄清在新系统中如何期望找到/生成 tr.json。
        # 目前，保留原始路径逻辑，但它可能与新的生成方式不一致。
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(current_dir, "data", "tr.json")  # 原始路径

    def read_tr_codes(self):
        """读取所有交易码"""
        if not os.path.exists(self.file_path):
            # 如果已知常见的 excel 名称（例如 "default"），则尝试在新的输出结构中查找它
            # 如果需要，这是一个更强大的发现机制的占位符。
            # 例如：self.file_path = os.path.join(ExcelHandler.JSON_OUTPUT_DIR, "some_excel_stem", "tr.json")
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
