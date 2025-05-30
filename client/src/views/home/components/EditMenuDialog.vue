<template>
  <el-dialog v-model="dialogVisible" title="编辑菜单" width="80%" :before-close="handleClose">
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="130px" label-suffix=":" class="menu-form">
      <el-form-item label="菜单ID" prop="menuId">
        <el-input v-model="formData.menuId" placeholder="请输入菜单ID" :disabled="editType == 'edit'" />
      </el-form-item>

      <el-form-item label="菜单码" prop="menuCode">
        <el-input v-model="formData.menuCode" placeholder="请输入菜单码" :disabled="editType == 'edit'" />
      </el-form-item>

      <el-form-item label="菜单名称" prop="menuName">
        <el-input v-model="formData.menuName" placeholder="请输入菜单名称" />
      </el-form-item>

      <el-form-item label="上级菜单编码" prop="uppMenuCode">
        <el-input v-model="formData.uppMenuCode" placeholder="请输入上级菜单编码" />
      </el-form-item>

      <el-form-item label="菜单级别" prop="menuLevel">
        <el-select v-model="formData.menuLevel" placeholder="请选择菜单级别">
          <el-option v-for="(value, key) in MENU_LEVEL_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="菜单类型" prop="menuType">
        <el-select v-model="formData.menuType" placeholder="请选择菜单类型">
          <el-option v-for="(value, key) in MENU_TYPE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="排序编号" prop="sortNo">
        <el-input v-model="formData.sortNo" placeholder="请输入排序编号" />
      </el-form-item>

      <el-form-item label="页面是否缓存" prop="isKeepAlive">
        <el-select v-model="formData.isKeepAlive" placeholder="请选择">
          <el-option v-for="(value, key) in ENABLE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="审批标志" prop="workflowFlag">
        <el-select v-model="formData.workflowFlag" placeholder="请选择">
          <el-option v-for="(value, key) in ENABLE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="菜单链接" prop="menuHerf">
        <el-input v-model="formData.menuHerf" placeholder="请输入菜单链接" />
      </el-form-item>

      <el-form-item label="是否使用新图标库" prop="iconFlag">
        <el-select v-model="formData.iconFlag" placeholder="请选择">
          <el-option v-for="(value, key) in ENABLE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="菜单图标" prop="menuIcon">
        <el-input v-model="formData.menuIcon" placeholder="请输入菜单图标" />
      </el-form-item>

      <el-form-item label="菜单范围" prop="menuScope">
        <el-select v-model="formData.menuScope" placeholder="请选择菜单范围">
          <el-option v-for="(value, key) in MENU_SCOPE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="菜单分类" prop="menuKind">
        <el-select v-model="formData.menuKind" placeholder="请选择菜单分类">
          <el-option v-for="(value, key) in MENU_KIND_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="权限校验" prop="menuVerify">
        <el-select v-model="formData.menuVerify" placeholder="请选择权限校验">
          <el-option v-for="(value, key) in MENU_VERIFY_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="菜单显示" prop="menuDisplay">
        <el-select v-model="formData.menuDisplay" placeholder="请选择菜单显示">
          <el-option v-for="(value, key) in MENU_DISPLAY_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="菜单选中" prop="menuChecked">
        <el-select v-model="formData.menuChecked" placeholder="请选择菜单选中">
          <el-option v-for="(value, key) in MENU_CHECKED_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="交易码" prop="trCode">
        <el-input v-model="formData.trCode" placeholder="请输入交易码" />
      </el-form-item>

      <el-form-item label="系统编码" prop="subsystemCode">
        <el-input v-model="formData.subsystemCode" placeholder="请输入系统编码" />
      </el-form-item>

      <el-form-item label="文件夹编码" prop="folderCode">
        <el-input v-model="formData.folderCode" placeholder="请输入文件夹编码" />
      </el-form-item>

      <el-form-item label="审批候选人模式" prop="workflowAssigneeMode">
        <el-select v-model="formData.workflowAssigneeMode" placeholder="请选择">
          <el-option v-for="(value, key) in WORKFLOW_ASSIGNEE_MODE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="管理员是否可用" prop="isAdmin">
        <el-select v-model="formData.isAdmin" placeholder="请选择">
          <el-option v-for="(value, key) in ENABLE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="操作员是否可用" prop="isOperator">
        <el-select v-model="formData.isOperator" placeholder="请选择">
          <el-option v-for="(value, key) in ENABLE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>

      <el-form-item label="菜单属性" prop="menuAttribute">
        <el-select v-model="formData.menuAttribute" placeholder="请选择菜单属性">
          <el-option v-for="(value, key) in MENU_ATTRIBUTE_ENUM" :value="key" :key="key" :label="value" />
        </el-select>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import menuCommon from '@/utils/menuCommon'
import tbspApi from '@/api/tbsp'
import type { EditType } from '@/types/menu'

const { MENU_TYPE_ENUM, MENU_LEVEL_ENUM, ENABLE_ENUM, MENU_KIND_ENUM, MENU_VERIFY_ENUM, MENU_DISPLAY_ENUM, MENU_CHECKED_ENUM, MENU_ATTRIBUTE_ENUM, MENU_SCOPE_ENUM, WORKFLOW_ASSIGNEE_MODE_ENUM } = menuCommon

// 定义组件的 props 和 emits
const emit = defineEmits(['update-success'])

// 定义编辑类型
const editType = ref<EditType>('edit')

// 响应式数据
const dialogVisible = ref(false)
const submitLoading = ref(false)
const formRef = ref()

// 表单数据
const formData = reactive({
  menuId: '',
  menuCode: '',
  menuName: '',
  uppMenuCode: '',
  menuLevel: '',
  menuType: '',
  sortNo: '',
  isKeepAlive: '',
  workflowFlag: '',
  menuHerf: '',
  iconFlag: '',
  menuIcon: '',
  menuScope: '',
  menuKind: '',
  menuVerify: '',
  menuDisplay: '',
  menuChecked: '',
  trCode: '',
  subsystemCode: '',
  folderCode: '',
  workflowAssigneeMode: '',
  isAdmin: '',
  isOperator: '',
  menuAttribute: '',
})

// 表单验证规则
const rules = {
  menuId: [{ required: true, message: '请输入菜单ID', trigger: 'blur' }],
  menuCode: [{ required: true, message: '请输入菜单码', trigger: 'blur' }],
  menuName: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  uppMenuCode: [{ required: true, message: '请输入上级菜单编码', trigger: 'blur' }],
  menuLevel: [{ required: true, message: '请选择菜单级别', trigger: 'change' }],
  menuType: [{ required: true, message: '请选择菜单类型', trigger: 'change' }],
  sortNo: [{ required: true, message: '请输入排序编号', trigger: 'blur' }],
  menuScope: [{ required: true, message: '请选择菜单范围', trigger: 'change' }],
  menuKind: [{ required: true, message: '请选择菜单分类', trigger: 'change' }],
  menuVerify: [{ required: true, message: '请选择权限校验', trigger: 'change' }],
  menuDisplay: [{ required: true, message: '请选择菜单显示', trigger: 'change' }],
  menuChecked: [{ required: true, message: '请选择菜单选中', trigger: 'change' }],
  subsystemCode: [{ required: true, message: '请输入系统编码', trigger: 'blur' }],
  folderCode: [{ required: true, message: '请输入文件夹编码', trigger: 'blur' }],
  isAdmin: [{ required: true, message: '请选择管理员是否可用', trigger: 'change' }],
  isOperator: [{ required: true, message: '请选择操作员是否可用', trigger: 'change' }],
  menuAttribute: [{ required: true, message: '请选择菜单属性', trigger: 'change' }],
}

// 打开弹窗
const show = (rowData: any, type: EditType = 'edit') => {
  dialogVisible.value = true
  editType.value = type

  // 将行数据复制到表单数据中
  Object.keys(formData).forEach((key) => {
    if (rowData && rowData[key] !== undefined) {
      formData[key] = rowData[key]
    }
  })
}

// 关闭弹窗
const handleClose = () => {
  dialogVisible.value = false
  // 重置表单
  if (formRef.value) {
    formRef.value.resetFields()
  }
  // 清空表单数据
  Object.keys(formData).forEach((key) => {
    formData[key] = ''
  })
}

// 抽出API请求方法
const submitMenuData = async (data: any) => {
  const apiUrl = editType.value === 'edit' ? '/tool-updGlobalMenu' : '/tool-addGlobalMenu'
  return await tbspApi.post(apiUrl, data)
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitLoading.value = true

    // 准备提交数据
    const submitData = Object.assign({}, formData, {
      workflowFlagOps: formData.workflowFlag,
      permWorkflowFlagOps: formData.workflowFlag,
      permWorkflowFlag: formData.workflowFlag,
    })

    // 调用对应的API
    const response = await submitMenuData(submitData)

    // 检查响应结果
    if (response.data && response.data.respType === 'S') {
      const successMsg = editType.value === 'edit' ? '编辑成功' : '新增成功'
      ElMessage.success(successMsg)
      emit('update-success')
      handleClose()
    } else {
      // 处理业务失败的情况
      const errorMsg = response.data?.respMsg || (editType.value === 'edit' ? '编辑失败' : '新增失败')
      ElMessage.error(errorMsg)
    }
  } catch (error) {
    console.error('请求失败:', error)
    ElMessage.error('网络请求失败，请稍后重试')
  } finally {
    submitLoading.value = false
  }
}

// 暴露方法给父组件使用
defineExpose({
  show,
})
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}

.menu-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.menu-form .el-form-item {
  margin-bottom: 0;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .menu-form {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 769px) and (max-width: 1200px) {
  .menu-form {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1201px) {
  .menu-form {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
