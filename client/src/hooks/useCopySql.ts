import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useClipboard } from '@vueuse/core'

export function useCopySql() {
  const exportSelectedSQL = ref('')

  const buildPermMenu = (record: any, dateType: string, dual: string, notes: string) => {
    const CNST_TENANT_ID = notes === 'mysql' ? '@CNST_TENANT_ID' : 'CNST_TENANT_ID'
    const menuId = record.menuId ? `'${record.menuId}'` : null
    const menuCode = record.menuCode ? `'${record.menuCode}'` : null
    const menuName = record.menuName ? `'${record.menuName}'` : null
    const uppMenuCode = record.uppMenuCode ? `'${record.uppMenuCode}'` : null
    const menuIcon = record.menuIcon ? `'${record.menuIcon}'` : null
    const menuHerf = record.menuHerf ? `'${record.menuHerf}'` : null
    const menuLevel = record.menuLevel ? `'${record.menuLevel}'` : null
    const menuScope = record.menuScope ? `'${record.menuScope}'` : null
    const menuType = record.menuType ? `'${record.menuType}'` : null
    const menuKind = record.menuKind ? `'${record.menuKind}'` : `0`
    const menuVerify = record.menuVerify ? `'${record.menuVerify}'` : `0`
    const menuDisplay = record.menuDisplay ? `'${record.menuDisplay}'` : `0`
    const menuChecked = record.menuChecked ? `'${record.menuChecked}'` : `0`
    const menuAttribute = record.menuAttribute ? `'${record.menuAttribute}'` : null
    const trCode = record.trCode ? `'${record.trCode}'` : null
    const subsystemCode = record.subsystemCode ? `'${record.subsystemCode}'` : null
    const folderCode = record.folderCode ? `'${record.folderCode}'` : null
    const workflowFlag = record.workflowFlag ? `'${record.workflowFlag}'` : `0`
    const workflowAssigneeMode = record.workflowAssigneeMode ? `'${record.workflowAssigneeMode}'` : null
    const iconFlag = record.iconFlag ? `'${record.iconFlag}'` : `0`
    const isKeepAlive = record.isKeepAlive ? `'${record.isKeepAlive}'` : `0`
    const isAdmin = record.isAdmin ? `'${record.isAdmin}'` : `0`
    const isOperator = record.isOperator ? `'${record.isOperator}'` : `0`
    const sortNo = record.sortNo ? `'${record.sortNo}'` : null
    const jumpHerf = record.jumpHerf ? `'${record.jumpHerf}'` : null

    exportSelectedSQL.value += `INSERT INTO PERM_MENU (TENANT_ID, STAT, MENU_ID, MENU_CODE, MENU_NAME, UPP_MENU_CODE, MENU_ICON, MENU_HERF, MENU_LEVEL, MENU_SCOPE, MENU_TYPE, MENU_KIND, MENU_VERIFY, MENU_DISPLAY, MENU_CHECKED, MENU_ATTRIBUTE, TR_CODE, SUBSYSTEM_CODE, FOLDER_CODE, WORKFLOW_FLAG, WORKFLOW_ASSIGNEE_MODE, ICON_FLAG, IS_KEEP_ALIVE, IS_ADMIN, IS_OPERATOR, SORT_NO, CRE_DATE, UPD_DATE, JUMP_HERF)
SELECT ${CNST_TENANT_ID}, '1', ${menuId}, ${menuCode}, ${menuName}, ${uppMenuCode}, ${menuIcon}, ${menuHerf}, ${menuLevel}, ${menuScope}, ${menuType}, ${menuKind}, ${menuVerify}, ${menuDisplay}, ${menuChecked}, ${menuAttribute}, ${trCode}, ${subsystemCode}, ${folderCode}, ${workflowFlag}, ${workflowAssigneeMode}, ${iconFlag}, ${isKeepAlive}, ${isAdmin}, ${isOperator}, ${sortNo}, ${dateType}, ${dateType}, ${jumpHerf} ${dual}
WHERE NOT EXISTS (SELECT 1 FROM PERM_MENU WHERE MENU_CODE = ${menuCode} AND TENANT_ID = ${CNST_TENANT_ID});
`
  }

  const handleSqlValue = (row: any[], notes: string, dateType: string, dual: string) => {
    exportSelectedSQL.value += '-- ' + notes + '\r\n'
    for (let i = 0; i < row.length; i++) {
      buildPermMenu(row[i], dateType, dual, notes)
    }
    exportSelectedSQL.value += 'commit;\r\n'
  }

  const copySql = (type: 'MYSQL' | 'ORACLE', getSelectEvent: () => any[]) => {
    const selectedRows = getSelectEvent()
    if (selectedRows.length === 0) {
      ElMessage({
        message: '请先选择要复制的数据',
        type: 'warning',
      })
      return
    }

    exportSelectedSQL.value = ''

    switch (type) {
      case 'MYSQL':
        handleSqlValue(selectedRows, 'mysql', 'now()', '')
        break
      case 'ORACLE':
        handleSqlValue(selectedRows, 'oracle', 'sysdate', 'from dual')
        break
      default:
        break
    }

    const { copy } = useClipboard()
    copy(exportSelectedSQL.value)
    ElMessage({
      message: '复制SQL语句成功',
      type: 'success',
    })
  }

  return {
    copySql,
    exportSelectedSQL,
  }
}
