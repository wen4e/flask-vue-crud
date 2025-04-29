import axios from 'axios'

// 创建axios实例
const api = axios.create({
  timeout: 5000 // 请求超时时间
})

// 请求拦截器
api.interceptors.request.use(config => {
  // 在此处理请求headers等
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器
api.interceptors.response.use(response => {
  // 在此处理响应数据
  return response.data
}, error => {
  return Promise.reject(error)
})


export default api