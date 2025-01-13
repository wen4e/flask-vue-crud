import json
import os
import pandas as pd


# 处理excel文件
class ExcelHandler:
    ALLOWED_EXTENSIONS = {"xlsx", "xls"}

    @staticmethod
    def allowed_file(filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in ExcelHandler.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def read_excel(file_path):
        """读取Excel文件并返回数据"""
        try:
            df = pd.read_excel(file_path)
            return {"success": True, "data": df.to_dict("records")}
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
