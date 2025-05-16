import { ref } from 'vue'
import { ElMessage } from 'element-plus'

/**
 * Excel文件上传hooks
 * @param successCallback 上传成功后的回调函数
 * @param uploadUrl 上传地址，默认为/flaskApi/upload/excel
 * @returns 上传相关的属性和方法
 */
export function useExcelUpload(successCallback?: () => void, uploadUrl = '/flaskApi/upload/excel') {
  const fileList = ref([])
  const uploadRef = ref(null)

  // 上传成功处理
  const handleSuccess = (response) => {
    ElMessage.success('文件上传成功')
    if (successCallback) {
      successCallback()
    }
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

  return {
    fileList,
    uploadRef,
    uploadUrl,
    handleSuccess,
    handleError,
    beforeUpload,
    handleExceed,
  }
}
