<template>
  <div class="container">
    <div class="row">
      <el-upload ref="upload" class="upload-demo" action="http://localhost:5001/upload/excel" :file-list="fileList" :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload" :on-exceed="handleExceed" accept=".xlsx,.xls">
        <el-button type="primary">上传Excel文件</el-button>
      </el-upload>

      <el-table :data="trData" style="width: 100%">
        <el-table-column prop="trName" label="交易名称" />
        <el-table-column prop="trCode" label="交易码" />
        <el-table-column label="操作">
          <template #default>
            <el-button link type="primary" size="small" @click="handleDetail"> 详情 </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";
export default {
  data() {
    return {
      fileList: [], // 添加文件列表数据
      trData: [],
    };
  },
  methods: {
    // 上传成功处理
    handleSuccess(response) {
      ElMessage.success("文件上传成功");
      this.getTrCode();
    },

    // 上传失败处理
    handleError(error) {
      ElMessage.error("文件上传失败");
      console.error("上传失败:", error);
    },

    // 上传前验证
    beforeUpload(file) {
      const isExcel = file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" || file.type === "application/vnd.ms-excel";
      if (!isExcel) {
        ElMessage.error("只能上传Excel文件!");
        return false;
      }

      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isLt2M) {
        ElMessage.error("文件大小不能超过 2MB!");
        return false;
      }
      return true;
    },

    // 超出限制处理
    handleExceed() {
      ElMessage.warning("每次只能上传一个文件");
    },

    getTrCode() {
      const path = "http://localhost:5001/trCode";
      axios
        .get(path)
        .then((res) => {
          this.trData = res.data.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleDetail() {
      this.$router.push({ name: "Detail" });
    },
  },
  created() {
    this.getTrCode();
  },
};
</script>
