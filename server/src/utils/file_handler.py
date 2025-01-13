import json
import os
import pandas as pd
import random
import string


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


# 处理json文件
class JsonFileHandler:
    def __init__(self, file_path="data/books.json"):
        self.file_path = file_path
        self._ensure_file_exists()
        self._init_default_data()

    def _init_default_data(self):
        """初始化默认数据"""
        if os.path.getsize(self.file_path) == 0:
            default_books = [
                {
                    "id": "1",
                    "title": "On the Road",
                    "author": "Jack Kerouac",
                    "read": True,
                },
                {
                    "id": "2",
                    "title": "Harry Potter",
                    "author": "J. K. Rowling",
                    "read": False,
                },
            ]
            self.write_books(default_books)

    def _ensure_file_exists(self):
        """确保 JSON 文件存在，如果不存在则创建"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def read_books(self):
        """读取所有图书"""
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"读取文件错误: {str(e)}")
            return []

    def write_books(self, books):
        """写入所有图书"""
        try:
            with open(self.file_path, "w") as f:
                json.dump(books, f, indent=4)
            return True
        except Exception as e:
            print(f"写入文件错误: {str(e)}")
            return False

    def add_book(self, book):
        """添加单本图书"""
        books = self.read_books()
        books.append(book)
        return self.write_books(books)

    def remove_book(self, book_id):
        """删除指定图书"""
        books = self.read_books()
        books = [book for book in books if book["id"] != book_id]
        return self.write_books(books)

    def update_book(self, book_id, updated_book):
        """更新指定图书"""
        books = self.read_books()
        for i, book in enumerate(books):
            if book["id"] == book_id:
                books[i] = updated_book
                return self.write_books(books)
        return False
