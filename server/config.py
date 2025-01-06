import os


class Config:
    """基础配置类"""

    # Flask配置
    DEBUG = False
    TESTING = False

    # JSON文件存储路径
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    JSON_FILE_PATH = os.path.join(BASE_DIR, "data", "books.json")

    # CORS配置
    CORS_HEADERS = "Content-Type"


class DevelopmentConfig(Config):
    """开发环境配置"""

    DEBUG = True


class TestingConfig(Config):
    """测试环境配置"""

    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""

    DEBUG = False


# 配置映射
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
