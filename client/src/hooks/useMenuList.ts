import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ref, nextTick, type Ref } from 'vue'
import { useLogin } from './useLogin'

export function useMenuList() {
  const { generateSerialNo, login, loginInfo } = useLogin()
  const loading = ref(true)
  interface MenuItem {
    menuName: string
    menuCode: string
    trCode: string
    uppMenuCode: string
    [key: string]: any // For any other properties
  }

  let menuList = ref<MenuItem[]>([])
  let originalMenuList: MenuItem[] = []

  // 获取菜单列表
  interface MenuListParams {
    menuScope: string
    isAdmin: string
    isOperator: string
    uppMenuCode: string | null
  }

  interface TableRef {
    getTableData: () => { tableData: any[] }
    setTreeExpand: (nodes: any[], expanded: boolean) => Promise<void>
  }

  interface MenuListResponse {
    success: boolean
    data?: MenuItem[]
    reason?: string
  }

  const getMenuList = async (params: MenuListParams, tableRef: Ref<TableRef | undefined>): Promise<MenuListResponse> => {
    const SerialNo = generateSerialNo()
    loading.value = true

    try {
      const response = await axios.post('/tbspApi/tbsp/tool-pageMenu', {
        headUserNo: loginInfo.value.userId,
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
            if (tableRef.value) {
              // 添加此检查
              const treeData = tableRef.value.getTableData()
              const firstLevelNodes = treeData.tableData
              tableRef.value
                .setTreeExpand(firstLevelNodes, true)
                .then(() => {})
                .catch((err) => {
                  console.error('展开节点失败:', err)
                })
            }
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
      return {
        success: false,
        reason: error instanceof Error ? error.message : '未知错误',
      }
    }
  }
  /**
   * 递归收集 menuCode
   * @param {Array} list  菜单列表（可能包含 children）
   * @returns {Array<string>}  所有 menuCode 的扁平数组
   */
  /**
   * 递归收集 menuCode
   * @param {Array} list  菜单列表（可能包含 children）
   * @returns {Array<string>}  所有 menuCode 的扁平数组
   */
  interface MenuTreeItem extends MenuItem {
    children?: MenuTreeItem[]
  }
  /**
   * 递归收集 menuCode
   * @param {Array} list  菜单列表（可能包含 children）
   * @returns {Array<string>}  所有 menuCode 的扁平数组
   */
  const getAllMenuCodes = (list: MenuTreeItem[]): string[] => {
    return list.reduce((codes: string[], item: MenuTreeItem) => {
      // 先把当前节点的 menuCode 加进去
      codes.push(item.menuCode)
      // 如果有 children，就递归收集
      if (item.children && item.children.length) {
        codes.push(...getAllMenuCodes(item.children))
      }
      return codes
    }, [])
  }

  // 搜索函数：根据条件过滤菜单数据
  const searchMenuList = (filterVal: string | null | undefined, $table?: TableRef) => {
    if (filterVal) {
      const tmpMenuList = originalMenuList.filter((item) => ['menuName', 'menuCode', 'trCode', 'uppMenuCode'].some((key) => item[key] && item[key].toLowerCase().includes(filterVal.toLowerCase())))
      const result = getAllMenuCodes(tmpMenuList)
      menuList.value = originalMenuList.filter((menu) => result.includes(menu.menuCode))
    } else {
      menuList.value = originalMenuList
      // 如果提供了表格引用，展开树节点
      if ($table) {
        nextTick(() => {
          const treeData = $table.getTableData()
          const firstLevelNodes = treeData.tableData
          $table
            .setTreeExpand(firstLevelNodes, true)
            .then(() => {})
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
    searchMenuList,
  }
}
