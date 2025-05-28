<template>
  <el-form-item label="接口文档">
    <el-upload ref="uploadRef" class="upload-demo" :action="uploadUrl" :file-list="fileList" :show-file-list="false" :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload" :on-exceed="handleExceed" accept=".xlsx,.xls">
      <el-button type="primary">上传Excel</el-button>
    </el-upload>
  </el-form-item>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

interface Props {
  uploadUrl?: string
}

interface Emits {
  (e: 'uploadSuccess', response: any): void
}

const props = withDefaults(defineProps<Props>(), {
  uploadUrl: '/flaskApi/upload/excel',
})

const emit = defineEmits<Emits>()

const fileList = ref([])
const uploadRef = ref(null)

// 上传成功处理
const handleSuccess = (response: any) => {
  ElMessage.success('文件上传成功')
  emit('uploadSuccess', response)
}

// 上传失败处理
const handleError = (error: any) => {
  ElMessage.error('文件上传失败')
  console.error('上传失败:', error)
}

// 上传前验证
const beforeUpload = (file: File) => {
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
</script>
