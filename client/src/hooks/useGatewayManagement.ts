import { ref } from 'vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

export function useGatewayManagement() {
  const gatewayAddress = ref('')
  const gatewayOptions = ref([])

  // 查询所有网关地址
  const handleGatewayQuery = () => {
    return api
      .get('/gateway/query')
      .then((response) => {
        gatewayOptions.value = response.data
        return response.data
      })
      .catch((error) => {
        console.error('查询网关地址失败:', error)
        ElMessage.error('查询网关地址失败')
        return []
      })
  }

  // 查询默认网关地址
  const handleGatewayDefaultQuery = () => {
    return api
      .get('/gateway/defaultQuery')
      .then((response) => {
        gatewayAddress.value = response.data
        return response.data
      })
      .catch((error) => {
        console.error('查询默认网关地址失败:', error)
        ElMessage.error('查询默认网关地址失败')
        return ''
      })
  }

  // 网关地址切换 - 添加回调参数
  const handleGatewayChange = (value, callback) => {
    return api
      .post('/gateway/change', { gatewayUrl: value })
      .then((response) => {
        ElMessage.success('网关地址切换成功')
        // 如果提供了回调函数，则调用它
        if (typeof callback === 'function') {
          callback()
        }
        return response.data
      })
      .catch((error) => {
        console.error('切换网关地址失败:', error)
        ElMessage.error('切换网关地址失败')
        return null
      })
  }

  // 新增网关地址 - 添加回调参数
  const handleGatewayAdd = (label, value, callback) => {
    return api
      .post('/gateway/add', { gatewayName: label, gatewayUrl: value })
      .then((response) => {
        ElMessage.success('网关地址添加成功')
        // 添加成功后刷新列表
        handleGatewayQuery()
        // 如果提供了回调函数，则调用它
        if (typeof callback === 'function') {
          callback()
        }
        return response.data
      })
      .catch((error) => {
        console.error('添加网关地址失败:', error)
        ElMessage.error('添加网关地址失败')
        return null
      })
  }

  // 删除网关地址 - 添加回调参数
  const handleGatewayDel = (value, callback) => {
    return api
      .post('/gateway/delete', { gatewayUrl: value })
      .then((response) => {
        ElMessage.success('网关地址删除成功')
        // 删除成功后刷新列表
        handleGatewayQuery()
        // 如果提供了回调函数，则调用它
        if (typeof callback === 'function') {
          callback()
        }
        return response.data
      })
      .catch((error) => {
        console.error('删除网关地址失败:', error)
        ElMessage.error('删除网关地址失败')
        return null
      })
  }

  // 初始化
  const initGateway = async () => {
    await handleGatewayQuery()
    await handleGatewayDefaultQuery()
  }

  // 初始加载
  initGateway()

  return {
    gatewayAddress,
    gatewayOptions,
    handleGatewayQuery,
    handleGatewayDefaultQuery,
    handleGatewayChange,
    handleGatewayAdd,
    handleGatewayDel,
  }
}
