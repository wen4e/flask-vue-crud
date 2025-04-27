import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ref, nextTick } from 'vue'
import { useLogin } from './useLogin'

export function useMenuList() {
  const { generateSerialNo, login, loginInfo } = useLogin()
  const loading = ref(true)
  let menuList = ref([])
  let originalMenuList = []

  // 获取菜单列表
  const getMenuList = async (params, tableRef) => {
    const SerialNo = generateSerialNo()
    loading.value = true
    try {
      const response = await axios.post('/tbspApi/tbsp/tool-pageMenu', {
        headUserNo: loginInfo.userId,
        headTrDate: '20250210',
        headSerialNo: SerialNo,
        headReqDate: '20250210',
        headReqTime: '195219',
        headReqSerialNo: SerialNo,
        headOrigDate: '20250210',
        headOrigTime: '195219',
        headOrigSerialNo: SerialNo,
        language: '1',
        menuScope: params.menuScope, //"1001": "企业PC"，"1002": "企业APP"，"4001": "银行PC"
        trCode: '',
        menuCode: null,
        menuName: null,
        isAdmin: params.isAdmin,
        isOperator: params.isOperator,
        uppMenuCode: params.uppMenuCode,
        menuCodeLike: null,
        menuNameLike: null,
        copyClick: true,
        pager: false,
        headMenuCode: 'tool-pageMenu',
      })
      if (response.data.respType === 'S') {
        loading.value = false
        // 将获取到的数据同时赋值给原始数据和当前显示数据
        originalMenuList = response.data.dtos
        menuList.value = response.data.dtos

        // 如果提供了表格引用，展开树节点
        if (tableRef) {
          nextTick(() => {
            const treeData = tableRef.value.getTableData()
            const firstLevelNodes = treeData.tableData
            tableRef.value
              .setTreeExpand(firstLevelNodes, true)
              .then(() => { })
              .catch((err) => {
                console.error('展开节点失败:', err)
              })
          })
        }

        return { success: true, data: response.data.dtos }
      } else if (response.data.respType === 'N') {
        ElMessage('登录超时，重新登录中')
        login(() => {
          // 登录成功后重新获取菜单列表
          getMenuList(params, tableRef)
        })
        return { success: false, reason: 'login_timeout' }
      } else {
        ElMessage.error(response.data.respMsg)
        return { success: false, reason: response.data.respMsg }
      }
    } catch (error) {
      console.error('Error fetching data:', error)
      return { success: false, reason: error.message }
    }
  }

  // 搜索函数：根据条件过滤菜单数据
  const searchMenuList = (filterVal, $table) => {
    if (filterVal) {
      menuList.value = originalMenuList.filter((item) =>
        ['menuName', 'menuCode', 'trCode', 'uppMenuCode'].some(
          (key) => item[key] && item[key].toLowerCase().includes(filterVal.toLowerCase())
        )
      )
    } else {
      menuList.value = originalMenuList
      // 如果提供了表格引用，展开树节点
      if ($table) {
        nextTick(() => {
          const treeData = $table.getTableData()
          const firstLevelNodes = treeData.tableData
          $table
            .setTreeExpand(firstLevelNodes, true)
            .then(() => { })
            .catch((err) => {
              console.error('展开节点失败:', err)
            })
        })
      }
    }

    return menuList
  }

  return {
    loading,
    menuList,
    getMenuList,
    searchMenuList
  }
}