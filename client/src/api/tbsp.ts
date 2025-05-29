import axios from 'axios'
import { getRandomString } from '@/utils/tools'
import { useLocalStorage } from '@vueuse/core'

// 创建axios实例
const tbspApi = axios.create({
  baseURL: '/flaskApi/tbspApi/tbsp', // API的基础URL
  timeout: 5000, // 请求超时时间
})

// 请求拦截器
tbspApi.interceptors.request.use(
  (config) => {
    // 生成序列号
    const serialNo = getRandomString(22)
    const loginInfo = useLocalStorage('loginInfo', { userId: '' })

    // 添加公共请求头
    const commonHeaders = {
      headUserNo: loginInfo.value.userId,
      headReqTime: '193246',
      headReqSerialNo: serialNo,
      headTrDate: '20250210',
      headSerialNo: serialNo,
      headReqDate: '20250210',
      headOrigDate: '20250210',
      headOrigTime: '193246',
      headOrigSerialNo: serialNo,
      language: '1',
    }

    // 如果请求体存在，合并公共参数
    if (config.data) {
      config.data = { ...commonHeaders, ...config.data }
    } else {
      config.data = commonHeaders
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
tbspApi.interceptors.response.use(
  (response) => {
    // 在此处理响应数据
    return response
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default tbspApi
