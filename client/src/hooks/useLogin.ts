import axios from 'axios'
import { ElMessage } from 'element-plus'
import { getRandomString } from '@/utils/tools'
import { useLocalStorage } from '@vueuse/core'
import { ref } from 'vue'
// 在 useLogin.ts 中添加类型声明
interface LoginInfoData {
  userId?: string
  // 添加其他需要的属性
  [key: string]: any
}
export function useLogin() {
  // 创建持久化的存储引用
  const loginInfo = useLocalStorage<LoginInfoData>('loginInfo', {})
  const SerialNo = ref('')

  // 登录方法
  interface LoginRequest {
    headUserNo: string
    headTrDate: string
    headSerialNo: string
    headReqDate: string
    headReqTime: string
    headReqSerialNo: string
    headOrigDate: string
    headOrigTime: string
    headOrigSerialNo: string
    language: string
    orgNo: string
    userNo: string
    passwd: string
    verificationCode: string
    headChannel: string
    headOrgNo: string
    headCustNo: string
    headMenuCode: string
    headTrCode: string
  }

  interface LoginResponseData {
    respType: string
    [key: string]: any
  }

  type LoginCallback = () => void

  const login = async (callback?: LoginCallback): Promise<void> => {
    SerialNo.value = getRandomString(22)
    try {
      const requestData: LoginRequest = {
        headUserNo: 'jres',
        headTrDate: '20250210',
        headSerialNo: SerialNo.value,
        headReqDate: '20250210',
        headReqTime: '193246',
        headReqSerialNo: SerialNo.value,
        headOrigDate: '20250210',
        headOrigTime: '193246',
        headOrigSerialNo: SerialNo.value,
        language: '1',
        orgNo: '',
        userNo: 'jres',
        passwd: '33240f293bd2daad67ab8b1c6964b1b9',
        verificationCode: '',
        headChannel: '01',
        headOrgNo: '1',
        headCustNo: '000400000009999',
        headMenuCode: 'bank',
        headTrCode: 'tool',
      }

      const response = await axios.post<LoginResponseData>('/flaskApi/tbspApi/tbsp/bank/tool/login', requestData)

      // 直接更新loginInfo的值
      loginInfo.value = response.data
      if (response.data.respType === 'S') {
        ElMessage({
          message: '登录成功',
          type: 'success',
        })

        // 执行登录成功后的回调函数
        if (typeof callback === 'function') {
          callback()
        }
      }
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  // 生成新的序列号
  const generateSerialNo = () => {
    SerialNo.value = getRandomString(22)
    return SerialNo.value
  }

  return {
    login,
    loginInfo,
    generateSerialNo,
  }
}
