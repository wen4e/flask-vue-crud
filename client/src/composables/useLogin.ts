import { ElMessage } from 'element-plus'
import { useLocalStorage } from '@vueuse/core'
import tbspApi from '@/api/tbsp'

export function useLogin() {
  // 创建持久化的存储引用
  const loginInfo = useLocalStorage('loginInfo', { userId: '' })

  // 登录方法
  const login = async (callback) => {
    try {
      const requestData = {
        userNo: 'jres',
        passwd: '33240f293bd2daad67ab8b1c6964b1b9',
        verificationCode: '',
        headChannel: '01',
        headOrgNo: '1',
        headCustNo: '000400000009999',
        headMenuCode: 'bank',
        headTrCode: 'tool',
      }

      const response = await tbspApi.post('/bank/tool/login', requestData)

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

  return {
    login,
  }
}
