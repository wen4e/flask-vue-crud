import json
import os
import pandas as pd


# 处理excel文件
class ExcelHandler:
    ALLOWED_EXTENSIONS = {"xlsx", "xls"}
    DATA_DIR = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )

    @staticmethod
    def allowed_file(filename):
        """检查文件扩展名是否允许"""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ExcelHandler.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def read_excel(file_path):
        """读取Excel文件并处理"""
        try:
            result = ExcelHandler.process_file(file_path)
            if result["success"]:
                return {"success": True, "data": "Excel处理成功"}
            return {"success": False, "error": result["error"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def process_excel_data(df):
        """处理Excel数据的静态方法"""
        try:
            data = df.to_dict("records")
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def save_to_json(data, filename):
        """保存数据为JSON文件"""
        try:
            if not os.path.exists(ExcelHandler.DATA_DIR):
                os.makedirs(ExcelHandler.DATA_DIR)

            json_path = os.path.join(ExcelHandler.DATA_DIR, f"{filename}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return {"success": True, "file_path": json_path}
        except Exception as e:
            return {"success": False, "error": str(e)}  # 修复了这里的多余引号

    @staticmethod
    def process_file(file_path):
        """处理Excel文件"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            engine = "xlrd" if file_extension == ".xls" else "openpyxl"
            excel_file = pd.ExcelFile(file_path, engine=engine)

            # 遍历所有sheet，从第三个开始
            for sheet_name in excel_file.sheet_names[2:]:
                df = excel_file.parse(sheet_name)
                result = ExcelHandler.process_excel_data(df)
                if result["success"]:
                    ExcelHandler.save_to_json(result["data"], sheet_name)

            # 处理第二个sheet，提取C列和D列
            second_sheet = excel_file.parse(excel_file.sheet_names[1])
            tr_data = []
            if "交易名称" in second_sheet.columns and "交易码" in second_sheet.columns:
                for _, row in second_sheet.iterrows():
                    tr_data.append({"trName": row["交易名称"], "trCode": row["交易码"]})

            # 保存交易信息到tr.json
            ExcelHandler.save_to_json(tr_data, "tr")

            return {"success": True, "message": "数据处理完成"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# 获取data文件夹下的tr.json文件
class TrCodeHandler:
    def __init__(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(current_dir, "data", "tr.json")

    def read_tr_codes(self):
        """读取所有交易码"""
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except Exception:
            return []
