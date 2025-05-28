<template>
  <div class="container">
    <el-upload ref="upload" class="upload-demo" :action="`/flaskApi/upload/excel`" :file-list="fileList" :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload" :on-exceed="handleExceed" accept=".xlsx,.xls">
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const fileList = ref([])
const trData = ref([])

// 上传成功处理
const handleSuccess = (response) => {
  ElMessage.success('文件上传成功')
  getTrCode()
}

// 上传失败处理
const handleError = (error) => {
  ElMessage.error('文件上传失败')
  console.error('上传失败:', error)
}

// 上传前验证
const beforeUpload = (file) => {
  const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.type === 'application/vnd.ms-excel'
  if (!isExcel) {
    ElMessage.error('只能上传Excel文件!')
    return false
  }

  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('文件大小不能超过 2MB!')
    return false
  }
  return true
}

// 超出限制处理
const handleExceed = () => {
  ElMessage.warning('每次只能上传一个文件')
}

const getTrCode = async () => {
  try {
    const res = await api.get('/trCode')
    trData.value = res.data.data || []
  } catch (error) {
    console.error(error)
  }
}

const handleDetail = () => {
  router.push({ name: 'Detail' })
}

// 生命周期钩子
onMounted(() => {
  getTrCode()
})
</script>
