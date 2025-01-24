import os


class CodeHandler:
    def __init__(self):
        # 获取当前文件所在目录的父级目录(server/src)
        current_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        # 获取目标目录(code/src/views/orgManage)
        self.target_dir = os.path.join(
            os.path.dirname(current_dir), "code", "src", "views", "orgManage"
        )

    def create_page(self, code):
        """
        创建Vue页面
        :param code: 页面代码/名称
        :return: dict 包含成功状态和相关信息
        """
        try:
            # 确保目标目录存在
            if not os.path.exists(self.target_dir):
                os.makedirs(self.target_dir)

            # 构造文件名
            file_name = f"{code}.vue"
            file_path = os.path.join(self.target_dir, file_name)

            # 检查文件是否已存在
            if os.path.exists(file_path):
                return {"success": False, "error": f"文件 {file_name} 已存在"}

            # Vue页面模板
            template = """<template>
  <div class="${code}-container">
    <h1>${code}</h1>
  </div>
</template>

<script>
export default {
  name: '${code}',
  data() {
    return {
      // 数据属性
    }
  },
  methods: {
    // 方法定义
  }
}
</script>

<style scoped>
.${code}-container {
  padding: 20px;
}
</style>
""".replace(
                "${code}", code
            )

            # 写入文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(template)

            return {"success": True, "data": {"file": file_name, "path": file_path}}

        except Exception as e:
            return {"success": False, "error": f"创建页面时发生错误: {str(e)}"}
