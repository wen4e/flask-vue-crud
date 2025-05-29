<template>
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
      <el-button type="primary" @click="() => copySql('MYSQL', getSelectEvent)">复制mysql</el-button>
      <el-button type="primary" @click="() => copySql('ORACLE', getSelectEvent)">复制oracle</el-button>
    </el-form-item>
    <upload-excel @upload-success="getMenuList" />
    <gateway-selector ref="gatewaySelectorRef" :on-update="getMenuList" />
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
  >
    <vxe-column type="checkbox" title="菜单名称" tree-node width="320" fixed="left"></vxe-column>
    <vxe-column field="menuCode" title="菜单码" width="auto"></vxe-column>
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
    </vxe-column>
  </vxe-table>
  <generate-page-dialog ref="generatePageDialogRef" />
</template>

<script setup lang="ts">
import generatePageDialog from './components/generatePageDialog.vue'
// 引入网关管理
import GatewaySelector from './components/GatewaySelector.vue'
// 引入Excel上传组件
import UploadExcel from './components/UploadExcel.vue'
// 菜单相关枚举和工具函数
import enums from '@/utils/menuCommon'
import debounce from 'lodash/debounce'
import { ref } from 'vue'
import { useMenuList } from '@/hooks/useMenuList'
import { useCopySql } from '@/hooks/useCopySql'

// 使用menuList hook
const { loading, menuList, getMenuList: fetchMenuList, searchMenuList } = useMenuList()
// 复制SQL的hook
const { copySql } = useCopySql()
// 表格相关
const tableRef = ref()
let tableHeight = ref()
// 高度计算
const updateTableHeight = () => {
  tableHeight.value = window.innerHeight - 120
}
updateTableHeight()
window.onresize = debounce(updateTableHeight, 200)
const getSelectEvent = () => {
  const selectedRows = tableRef.value.getCheckboxRecords()
  return selectedRows
}

// 从 enums 中解构出格式化函数
const { formatterMenuKind, formatterMenuVerify, formatterMenuDisplay, formatterMenuChecked, formatterMenuAttribute, formatterMenuType, formatterFlag } = enums

// 操作栏方法
const editRowEvent = (row) => {
  console.log('🚀 ~ editRowEvent ~ row:', row)
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

// 初始化加载菜单列表
getMenuList()
</script>
