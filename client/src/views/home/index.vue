<template>
  <div>
    <!-- 搜索输入框 -->
    <el-form :inline="true" label-suffix="：">
      <el-form-item label="搜索">
        <el-input v-model.trim="filterName" class="w-[300px]" placeholder="菜单名称/菜单码/交易码/上级菜单编码" clearable @input="searchEvent"></el-input>
      </el-form-item>
      <el-form-item label="系统">
        <el-radio-group v-model="menuScope" @change="searchTable">
          <el-radio-button value="1001">企业端</el-radio-button>
          <el-radio-button value="4001">银行端</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="角色">
        <el-radio-group v-model="role" @change="searchTable">
          <el-radio-button value="ALL">全部</el-radio-button>
          <el-radio-button value="ADMIN">管理员</el-radio-button>
          <el-radio-button value="OPERATOR">操作员</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="复制sql">
        <el-button type="primary" @click="copySql('MYSQL')">复制mysql</el-button>
        <el-button type="primary" @click="copySql('ORACLE')">复制oracle</el-button>
      </el-form-item>
      <el-form-item label="接口文档">
        <el-upload ref="uploadRef" class="upload-demo" :action="uploadUrl" :file-list="fileList" :show-file-list="false" :on-success="handleSuccess" :on-error="handleError" :before-upload="beforeUpload" :on-exceed="handleExceed" accept=".xlsx,.xls">
          <el-button type="primary">上传Excel</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="网关地址">
        <el-select v-model="gatewayAddress" placeholder="请选择网关地址" @change="handleGatewayChange" class="w-[300px]">
          <el-option v-for="item in gatewayOptions" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
    </el-form>

    <!-- 表格 -->
    <vxe-table
      ref="tableRef"
      show-overflow
      :height="tableHeight"
      :column-config="{ resizable: true }"
      :scroll-y="{ enabled: true, gt: 0 }"
      border
      stripe
      :loading="loading"
      :tree-config="{
        transform: true,
        rowField: 'menuCode',
        parentField: 'uppMenuCode',
      }"
      :data="menuList"
      :checkbox-config="{ labelField: 'menuName', highlight: true }"
      :edit-config="{ trigger: 'manual', mode: 'row' }"
    >
      <vxe-column type="checkbox" title="菜单名称" tree-node width="320" fixed="left"></vxe-column>
      <vxe-column field="menuCode" title="菜单码" :edit-render="{ name: 'VxeInput' }" width="auto"></vxe-column>
      <vxe-column field="trCode" title="交易码" width="auto"></vxe-column>
      <vxe-column field="uppMenuCode" title="上级菜单码" width="auto"></vxe-column>
      <vxe-column field="menuLevel" title="菜单级别" width="auto"></vxe-column>
      <vxe-column field="menuKind" title="菜单分类" width="auto" :formatter="formatterMenuKind"></vxe-column>
      <vxe-column field="menuVerify" title="权限校验" width="auto" :formatter="formatterMenuVerify"></vxe-column>
      <vxe-column field="menuDisplay" title="菜单显示" width="auto" :formatter="formatterMenuDisplay"></vxe-column>
      <vxe-column field="menuChecked" title="菜单选中" width="auto" :formatter="formatterMenuChecked"></vxe-column>
      <vxe-column field="subsystemCode" title="系统编码" width="auto"></vxe-column>
      <vxe-column field="folderCode" title="文件夹编码" width="auto"></vxe-column>
      <vxe-column field="isAdmin" title="管理员是否可用" width="auto" :formatter="formatterFlag"></vxe-column>
      <vxe-column field="isOperator" title="操作员是否可用" width="auto" :formatter="formatterFlag"></vxe-column>
      <vxe-column field="menuAttribute" title="菜单属性" width="auto" :formatter="formatterMenuAttribute"></vxe-column>
      <vxe-column field="sortNo" title="排序编号" width="auto"></vxe-column>
      <vxe-column field="menuType" title="菜单类型" width="auto" :formatter="formatterMenuType"></vxe-column>
      <vxe-column field="menuHerf" title="菜单链接" width="auto"></vxe-column>
      <vxe-column field="workflowFlag" title="审批标志" width="auto" :formatter="formatterFlag"></vxe-column>
      <vxe-column field="isKeepAlive" title="页面是否缓存" width="auto" :formatter="formatterFlag"></vxe-column>
      <vxe-column title="操作" width="110" fixed="right">
        <template #default="{ row }">
          <template v-if="hasEditStatus(row)">
            <el-tooltip effect="dark" content="保存" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="saveRowEvent(row)">
                <Check />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="取消" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="cancelRowEvent()">
                <Close />
              </el-icon>
            </el-tooltip>
          </template>
          <template v-else>
            <el-tooltip effect="dark" content="编辑" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="editRowEvent(row)">
                <Edit />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="复制" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="copyRowEvent(row)">
                <CopyDocument />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="删除" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="delRowEvent(row)">
                <Delete />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="生成页面" placement="top">
              <el-icon class="cursor-pointer" @click="generatePageRowEvent(row)">
                <Document />
              </el-icon>
            </el-tooltip>
          </template>
        </template>
      </vxe-column>
    </vxe-table>
    <generate-page-dialog ref="generatePageDialogRef" />
  </div>
</template>

<script setup lang="ts">
import generatePageDialog from './components/generatePageDialog.vue'
import { ElMessage } from 'element-plus'
import enums from '@/utils/menuCommon'
import { useClipboard } from '@vueuse/core'
import debounce from 'lodash/debounce'
import { ref } from 'vue'
import api from '@/api'
import { useMenuList } from '@/hooks/useMenuList' // 引入useMenuList hook
import { useExcelUpload } from '@/hooks/useExcelUpload' // 引入Excel上传hooks

// 使用menuList hook
const { loading, menuList, getMenuList: fetchMenuList, searchMenuList } = useMenuList()

// 表格相关
const tableRef = ref()
let tableHeight = ref()
const updateTableHeight = () => {
  tableHeight.value = window.innerHeight - 120
}
updateTableHeight()
window.onresize = debounce(updateTableHeight, 200)
const getSelectEvent = () => {
  const selectedRows = tableRef.value.getCheckboxRecords()
  return selectedRows
}
const exportSelectedSQL = ref('')
const buildPermMenu = (record, dateType, dual, notes) => {
  const CNST_TENANT_ID = notes == 'mysql' ? '@CNST_TENANT_ID' : 'CNST_TENANT_ID'
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
const handleSqlValue = (row, notes, dateType, dual) => {
  exportSelectedSQL.value += '-- ' + notes + '\r\n'
  for (let i = 0; i < row.length; i++) {
    buildPermMenu(row[i], dateType, dual, notes)
  }
  exportSelectedSQL.value += 'commit;\r\n'
}

// 复制sql
const copySql = (type) => {
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
// 表格格式化函数
const formatterMenuKind = ({ cellValue }: { cellValue: keyof typeof enums.MENU_KIND_ENUM }) => {
  return enums.MENU_KIND_ENUM[cellValue]
}
const formatterMenuVerify = ({ cellValue }: { cellValue: keyof typeof enums.MENU_VERIFY_ENUM }) => {
  return enums.MENU_VERIFY_ENUM[cellValue]
}
const formatterMenuDisplay = ({ cellValue }: { cellValue: keyof typeof enums.MENU_DISPLAY_ENUM }) => {
  return enums.MENU_DISPLAY_ENUM[cellValue]
}
const formatterMenuChecked = ({ cellValue }: { cellValue: keyof typeof enums.MENU_CHECKED_ENUM }) => {
  return enums.MENU_CHECKED_ENUM[cellValue]
}
const formatterMenuAttribute = ({ cellValue }: { cellValue: keyof typeof enums.MENU_ATTRIBUTE_ENUM }) => {
  return enums.MENU_ATTRIBUTE_ENUM[cellValue]
}
const formatterMenuType = ({ cellValue }: { cellValue: keyof typeof enums.MENU_TYPE_ENUM }) => {
  return enums.MENU_TYPE_ENUM[cellValue]
}
const formatterFlag = ({ cellValue }: { cellValue: keyof typeof enums.ENABLE_ENUM }): string => {
  return enums.ENABLE_ENUM[cellValue]
}

// 操作栏方法
const hasEditStatus = (row) => {
  const $table = tableRef.value
  if ($table) {
    return $table.isEditByRow(row)
  }
}
const editRowEvent = (row) => {
  const $table = tableRef.value
  if ($table) {
    $table.setEditRow(row)
  }
}
const saveRowEvent = (row) => {
  const $table = tableRef.value
  if ($table) {
    $table.clearEdit().then(() => {
      loading.value = true
      setTimeout(() => {
        loading.value = false
        ElMessage({
          message: 'Congrats, this is a success message.',
          type: 'success',
        })
      }, 300)
    })
  }
}
const cancelRowEvent = () => {
  const $table = tableRef.value
  if ($table) {
    $table.clearEdit()
  }
}
const copyRowEvent = (row) => {
  const $table = tableRef.value
  if ($table) {
    // 示例: 复制当前行数据处理逻辑
  }
}
const delRowEvent = (row) => {
  const $table = tableRef.value
  if ($table) {
    $table.remove(row)
  }
}
// 生成页面
const generatePageDialogRef = ref(null)
const generatePageRowEvent = (row) => {
  if (generatePageDialogRef.value) {
    generatePageDialogRef.value.show(row)
  }
}

// 搜索功能
const menuScope = ref('1001')
const filterName = ref('')
const role = ref('ALL')
const uppMenuCode = ref('corp-transactionBank')
const isAdmin = ref('')
const isOperator = ref('')

// 获取菜单列表
const getMenuList = async () => {
  const params = {
    menuScope: menuScope.value,
    isAdmin: isAdmin.value,
    isOperator: isOperator.value,
    uppMenuCode: uppMenuCode.value,
  }

  await fetchMenuList(params, tableRef)
}

const searchTable = () => {
  // 重置搜索条件
  filterName.value = ''
  if (role.value === 'ALL') {
    isAdmin.value = ''
    isOperator.value = ''
  } else if (role.value === 'ADMIN') {
    isAdmin.value = '1'
    isOperator.value = ''
  } else if (role.value === 'OPERATOR') {
    isAdmin.value = ''
    isOperator.value = '1'
  }
  if (menuScope.value === '1001') {
    uppMenuCode.value = 'corp-transactionBank'
  } else if (menuScope.value === '4001') {
    uppMenuCode.value = 'bank-transactionBank'
  }
  getMenuList()
}

// 搜索函数：根据 filterName 过滤菜单数据（示例中以 menuName 和 menuCode 字段作为匹配）
const handleSearch = () => {
  const filterVal = filterName.value.trim()
  searchMenuList(filterVal, tableRef.value)
}

const searchEvent = debounce(handleSearch, 500)

// 使用Excel上传hooks
const { fileList, uploadRef, uploadUrl, handleSuccess, handleError, beforeUpload, handleExceed } = useExcelUpload(() => {
  // 上传成功后的回调，比如刷新数据
  getMenuList()
})
// 初始化加载菜单列表
getMenuList()
// 在script setup中添加以下代码（放在其他ref定义附近）
const gatewayAddress = ref('')
const gatewayOptions = ref([])
// 网关地址查询
const handleGatewayQuery = () => {
  api
    .get('/gateway/query')
    .then((response) => {
      console.log('网关地址查询成功:', response.data[0].value)
      gatewayOptions.value = response.data

      // 这里可以添加查询网关地址后的其他逻辑
    })
    .catch((error) => {
      console.error('查询网关地址失败:', error)
    })
}
handleGatewayQuery()
// 网关地址切换
const handleGatewayChange = (value) => {
  api
    .post('/gateway/change', { gatewayUrl: value })
    .then((response) => {
      console.log('网关地址切换成功:', response)
      // 这里可以添加切换网关后的其他逻辑
    })
    .catch((error) => {
      console.error('切换网关地址失败:', error)
    })
  // 这里可以添加切换网关后的其他逻辑
}
// 新增网关地址
const handleGatewayAdd = (label, value) => {
  api
    .post('/gateway/add', { gatewayName: label, gatewayUrl: value })
    .then((response) => {
      console.log('网关地址切换成功:', response)
      // 这里可以添加切换网关后的其他逻辑
    })
    .catch((error) => {
      console.error('切换网关地址失败:', error)
    })
  // 这里可以添加切换网关后的其他逻辑
}
handleGatewayAdd('上海农商', 'http://10.20.162.57:7650')
// 删除网关地址
const handleGatewayDel = (value) => {
  api
    .post('/gateway/delete', { gatewayUrl: value })
    .then((response) => {
      console.log('网关地址切换成功:', response)
      // 这里可以添加切换网关后的其他逻辑
    })
    .catch((error) => {
      console.error('切换网关地址失败:', error)
    })
  // 这里可以添加切换网关后的其他逻辑
}
handleGatewayDel('http://localhost:8080')
</script>
