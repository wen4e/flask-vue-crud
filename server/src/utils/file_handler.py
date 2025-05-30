import json
import os
import pandas as pd
import random
import string


class ExcelHandler:
    ALLOWED_EXTENSIONS = {"xlsx", "xls"}
    # 用于存储生成的JSON文件的目录 - 修改为data/api
    JSON_OUTPUT_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "api",  # 新增api子目录
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
    def process_sheet_data(df: pd.DataFrame, dto_count: int = 15) -> dict:
        """处理工作表DataFrame以提取接口参数并生成JSON模拟数据。"""
        # 提取apiName和trCode
        api_name = (
            str(df.iloc[3, 1]).strip() if len(df) > 3 and len(df.columns) > 1 else ""
        )
        tr_code = (
            str(df.iloc[2, 1]).strip() if len(df) > 2 and len(df.columns) > 1 else ""
        )

        # 创建基本结构
        result = {
            "apiName": api_name,
            "trCode": tr_code,
            "requestParams": {},
            "responseParams": {
                "respCode": "000000000000",
                "respEx": None,
                "respMsg": "交易成功",
                "respStatus": "S",
                "respType": "S",
            },
        }

        # 第一步：扫描表格，识别所有DTO类型和它们的关系
        dto_types = {}  # 存储所有识别到的DTO类型
        dto_relations = {}  # 存储DTO之间的关系
        dto_fields = {}  # 存储每个DTO类型的字段
        dto_list_fields = {}  # 存储哪些字段是List类型，以及包含的DTO类型
        dto_parent_fields = {}  # 存储DTO类型与其父DTO的关系及字段名
        bizpage_responses = {}  # 存储BizPageResponse及其泛型类型
        current_dto_context = None  # 当前正在处理的DTO上下文

        import re

        # 首先扫描表格找出所有DTO类型和它们之间的关系
        for i, row in df.iterrows():
            if row.empty or pd.isna(row.iloc[0]):
                continue

            row_as_string = " ".join([str(cell) for cell in row if not pd.isna(cell)])

            # 识别DTO类型标题行（例如AcctBlanceBankTotalDTO）
            if re.search(r"^[A-Za-z]+[A-Za-z0-9]*DTO\b", row_as_string, re.IGNORECASE):
                dto_match = re.search(
                    r"^([A-Za-z]+[A-Za-z0-9]*DTO)\b", row_as_string, re.IGNORECASE
                )
                if dto_match:
                    current_dto_context = dto_match.group(1)
                    if current_dto_context not in dto_types:
                        dto_types[current_dto_context] = True
                        dto_fields[current_dto_context] = {}
                    continue

            # 寻找DTO定义行 - 特别关注BizPageResponse模式
            if "extends" in row_as_string:
                # 识别BizPageResponse模式
                bizpage_match = re.search(
                    r"extends\s+BizPageResponse\s*<\s*(\w+DTO\w*)\s*>", row_as_string
                )
                if bizpage_match:
                    response_class_match = re.search(
                        r"(\w+Resp)\s+extends", row_as_string
                    )
                    if response_class_match:
                        response_class = response_class_match.group(1)
                        dto_class = bizpage_match.group(1)
                        dto_types[dto_class] = True
                        dto_fields[dto_class] = {}
                        bizpage_responses[response_class] = dto_class
                        dto_list_fields["dtos"] = dto_class  # 自动添加dtos字段

                # 提取一般DTO类名
                dto_matches = re.findall(r"(\w+DTO\w*)", row_as_string)
                if dto_matches:
                    for dto_name in dto_matches:
                        dto_types[dto_name] = True
                        if dto_name not in dto_fields:
                            dto_fields[dto_name] = {}

            # 寻找List类型字段，记录DTO间的层级关系
            if "List<" in row_as_string:
                field_name = str(row.iloc[0]).strip()
                if field_name and field_name not in ["类型", "属性名"]:
                    generic_match = re.search(r"List\s*<\s*(\w+)\s*>", row_as_string)
                    if generic_match:
                        list_type = generic_match.group(1)
                        # 检查是否为非T类型(具体DTO类型)
                        if list_type != "T" and (
                            list_type.endswith("DTO") or list_type in dto_types
                        ):
                            dto_list_fields[field_name] = list_type
                            # 确保此DTO类型被记录
                            dto_types[list_type] = True
                            if list_type not in dto_fields:
                                dto_fields[list_type] = {}

                            # 记录字段所属的DTO上下文
                            if current_dto_context:
                                if list_type not in dto_parent_fields:
                                    dto_parent_fields[list_type] = []
                                dto_parent_fields[list_type].append(
                                    {"parent": current_dto_context, "field": field_name}
                                )

        # 如果没有识别到任何DTO类型，使用默认处理
        if not dto_types:
            # 原始简单处理逻辑...
            return result

        # 第二步：处理表格内容，提取字段属性
        mode = None  # "request" 或 "response"
        current_dto = None
        header_found = False

        for _, row in df.iterrows():
            if row.empty or pd.isna(row.iloc[0]):
                continue

            first_cell_value = str(row.iloc[0]).strip()
            row_as_string = " ".join([str(cell) for cell in row if not pd.isna(cell)])

            # 检查是否进入新的DTO定义区域
            for dto_name in dto_types:
                if (
                    dto_name in row_as_string
                    and "class" not in row_as_string
                    and "extends" not in row_as_string
                ):
                    current_dto = dto_name
                    header_found = False
                    break

            if first_cell_value == "入参":
                mode = "request"
                current_dto = None
                header_found = False
                continue
            if first_cell_value == "返回":
                mode = "response"
                current_dto = None
                header_found = False
                continue

            if (mode or current_dto) and not header_found:
                if first_cell_value in ("属性名", "类型"):
                    header_found = True
                continue

            if not (mode or current_dto) or not header_found:
                continue

            key_name = first_cell_value

            # 获取表格各列的值，确保有足够的列
            row_values = [
                str(cell).strip() if not pd.isna(cell) else "" for cell in row
            ]

            # 确保至少有9列数据（属性名、类型、说明、必输、元数据类型、最小、最大、精度、正则、备注）
            while len(row_values) < 10:
                row_values.append("")

            data_type = row_values[1] if len(row_values) > 1 else ""
            description = row_values[2] if len(row_values) > 2 else ""
            required_str = row_values[3] if len(row_values) > 3 else ""
            metadata_type = row_values[4] if len(row_values) > 4 else ""
            min_value_str = row_values[5] if len(row_values) > 5 else "0"
            max_value_str = row_values[6] if len(row_values) > 6 else "255"
            precision_str = row_values[7] if len(row_values) > 7 else "0"
            pattern = row_values[8] if len(row_values) > 8 else ""
            remark = row_values[9] if len(row_values) > 9 else ""

            if not key_name or key_name in ["属性名", "类型"]:
                continue

            # 转换required为布尔值
            required = required_str.upper() in ["Y", "TRUE", "是", "必输"]

            # 转换数值字段
            try:
                min_value = int(min_value_str) if min_value_str.isdigit() else 0
            except:
                min_value = 0

            try:
                max_value = int(max_value_str) if max_value_str.isdigit() else 255
            except:
                max_value = 255

            try:
                precision = int(precision_str) if precision_str.isdigit() else 0
            except:
                precision = 0

            # 检查是否为List类型
            if data_type and "List<" in data_type:
                generic_match = re.search(r"List\s*<\s*(\w+)\s*>", data_type)
                if generic_match:
                    list_type = generic_match.group(1)
                    if list_type.endswith("DTO") or list_type in dto_types:
                        dto_list_fields[key_name] = list_type
                        # 确保DTO类型被记录
                        dto_types[list_type] = True
                        if list_type not in dto_fields:
                            dto_fields[list_type] = {}

                        # 记录父子DTO关系
                        if current_dto:
                            if list_type not in dto_parent_fields:
                                dto_parent_fields[list_type] = []
                            dto_parent_fields[list_type].append(
                                {"parent": current_dto, "field": key_name}
                            )

            # 构建字段信息对象
            field_info = {
                "dataType": data_type,
                "description": description,
                "required": required,
                "metadataType": metadata_type,
                "minValue": min_value,
                "maxValue": max_value,
                "precision": precision,
                "pattern": pattern,
                "remark": remark,
            }

            # 根据上下文添加字段
            if current_dto:
                dto_fields[current_dto][key_name] = field_info
            elif mode == "request":
                result["requestParams"][key_name] = field_info
            elif mode == "response" and key_name not in dto_list_fields:
                result["responseParams"][key_name] = field_info

        # 递归构建DTO对象的函数，增强版
        def build_dto_object(dto_type, visited=None, depth=0, parent_context=None):
            """递归构建DTO对象，包括其中的嵌套字段"""
            if visited is None:
                visited = set()

            # 防止无限递归
            if depth > 5 or dto_type in visited or dto_type not in dto_fields:
                return {}

            # 防止循环引用
            visited.add(dto_type)

            # 复制基本字段
            dto_obj = dto_fields[dto_type].copy()

            # 处理此DTO中的List类型字段
            for field_name, field_value in list(dto_obj.items()):
                if field_name in dto_list_fields:
                    list_item_type = dto_list_fields[field_name]
                    if list_item_type in dto_types:
                        # 生成嵌套列表
                        nested_items = []
                        for _ in range(
                            min(3, dto_count)
                        ):  # 每个列表默认生成3个项目，不超过dto_count
                            nested_dto = build_dto_object(
                                list_item_type,
                                visited.copy(),
                                depth + 1,
                                {"dto": dto_type, "field": field_name},
                            )
                            if nested_dto:  # 只添加非空对象
                                nested_items.append(nested_dto)
                        if nested_items:
                            dto_obj[field_name] = nested_items

            # 特殊处理：查找该DTO类型是否有子DTO关系未在字段中体现
            # 例如AcctBlanceBankTotalDTO应该包含dtos字段(List<DepositBalDTO>)
            for child_dto, parent_info_list in dto_parent_fields.items():
                for parent_info in parent_info_list:
                    if parent_info["parent"] == dto_type:
                        field_name = parent_info["field"]
                        # 如果该字段还未被处理，添加它
                        if field_name not in dto_obj:
                            nested_items = []
                            for _ in range(min(3, dto_count)):
                                nested_dto = build_dto_object(
                                    child_dto,
                                    visited.copy(),
                                    depth + 1,
                                    {"dto": dto_type, "field": field_name},
                                )
                                if nested_dto:
                                    nested_items.append(nested_dto)
                            if nested_items:
                                dto_obj[field_name] = nested_items

            return dto_obj

        # 第三步：构建嵌套的响应结构
        # 处理主响应结构中的dtos字段
        if "dtos" in dto_list_fields and dto_list_fields["dtos"] in dto_types:
            dto_type = dto_list_fields["dtos"]
            dtos = []
            for _ in range(min(dto_count, 5)):  # 限制生成数量
                dto_obj = build_dto_object(dto_type)
                if dto_obj:  # 只添加非空对象
                    dtos.append(dto_obj)
            if dtos:
                result["responseParams"]["dtos"] = dtos

        # 处理响应中的其他顶级List字段
        for field_name, list_item_type in dto_list_fields.items():
            # 跳过已处理的dtos字段
            if field_name == "dtos" and "dtos" in result["responseParams"]:
                continue

            # 检查字段是否属于任何DTO（非顶级字段）
            is_dto_field = False
            for dto in dto_fields.values():
                if field_name in dto:
                    is_dto_field = True
                    break

            # 如果不是DTO的字段，则是顶级字段，需要直接添加到响应中
            if (
                not is_dto_field
                and list_item_type in dto_types
                and field_name not in result["responseParams"]
            ):
                items = []
                for _ in range(min(3, dto_count)):  # 默认生成3个项目
                    dto_item = build_dto_object(list_item_type)
                    if dto_item:
                        items.append(dto_item)
                if items:
                    result["responseParams"][field_name] = items

        return result

    @staticmethod
    def save_to_json(data, sheet_name, excel_filename_stem):
        """保存数据为JSON文件到data目录中"""
        try:
            target_dir = ExcelHandler.JSON_OUTPUT_DIR  # 直接使用data/api目录
            if not os.path.exists(target_dir):
                os.makedirs(
                    target_dir, exist_ok=True
                )  # 如果data/api目录不存在，则创建（包括父目录）

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

            # 处理第二个sheet，提取交易名称和交易码列，生成tr.json
            if len(xls.sheet_names) > 1:
                second_sheet = xls.parse(xls.sheet_names[1])
                tr_data = []
                if (
                    "交易名称" in second_sheet.columns
                    and "交易码" in second_sheet.columns
                ):
                    for _, row in second_sheet.iterrows():
                        tr_name = row["交易名称"]
                        tr_code = row["交易码"]
                        # 仅添加非空的交易信息
                        if pd.notna(tr_name) and pd.notna(tr_code):
                            tr_data.append({"trName": tr_name, "trCode": tr_code})

                # 追加保存交易信息到tr.json - 修改保存路径
                target_dir = ExcelHandler.JSON_OUTPUT_DIR  # 使用data/api目录
                # 确保目录存在
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)

                json_path = os.path.join(target_dir, "tr.json")

                # 如果文件存在，读取现有内容并合并
                existing_tr_data = []
                if os.path.exists(json_path):
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            existing_tr_data = json.load(f)
                    except Exception as e:
                        return {
                            "success": False,
                            "error": f"Failed to read existing tr.json: {str(e)}",
                        }

                # 合并数据(通过trCode去重)
                existing_tr_codes = set(item["trCode"] for item in existing_tr_data)
                merged_tr_data = existing_tr_data.copy()

                # 只添加不存在的交易码
                for item in tr_data:
                    if item["trCode"] not in existing_tr_codes:
                        merged_tr_data.append(item)
                        existing_tr_codes.add(item["trCode"])

                # 保存合并后的数据
                tr_save_result = ExcelHandler.save_to_json(merged_tr_data, "tr", "")
                if not tr_save_result["success"]:
                    return {
                        "success": False,
                        "error": f"Failed to save tr.json: {tr_save_result['error']}",
                    }
            # 需要排除处理的工作表
            excluded_sheets = ("报文头说明", "接口目录")
            processed_files_count = 0

            for sheet_name in xls.sheet_names:
                if sheet_name in excluded_sheets:
                    continue

                # 解析工作表时不使用标题行，以便我们可以根据单元格内容定义结构
                df = xls.parse(sheet_name=sheet_name, header=None)

                # 直接使用process_sheet_data返回的结果，不再需要单独提取apiName和trCode
                json_data = ExcelHandler.process_sheet_data(df, ExcelHandler.DTO_COUNT)

                save_result = ExcelHandler.save_to_json(
                    json_data, sheet_name, excel_filename_stem
                )
                if not save_result["success"]:
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
class TrCodeHandler:
    def __init__(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 修改tr.json文件路径到data/api目录
        self.api_dir = os.path.join(current_dir, "data", "api")
        self.tr_file_path = os.path.join(self.api_dir, "tr.json")

    def read_tr_codes(self):
        """读取所有交易码"""
        if not os.path.exists(self.tr_file_path):
            return []

        try:
            with open(self.tr_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def read_trcode_detail(self, tr_code):
        """根据交易码读取对应的JSON文件"""
        if not tr_code:
            return None

        # 构建文件路径
        json_filename = f"{tr_code}.json"
        json_file_path = os.path.join(self.api_dir, json_filename)

        # 检查文件是否存在
        if not os.path.exists(json_file_path):
            return None

        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            # 可以记录日志
            print(f"读取文件 {json_file_path} 时出错: {str(e)}")
            return None
