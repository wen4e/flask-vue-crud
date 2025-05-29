<template>
  <el-dialog v-model="dialogVisible" title="编辑菜单" width="80%" :before-close="handleClose">
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="120px" label-suffix="：">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="菜单名称" prop="menuName">
            <el-input v-model="formData.menuName" placeholder="请输入菜单名称" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="菜单码" prop="menuCode">
            <el-input v-model="formData.menuCode" placeholder="请输入菜单码" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="交易码" prop="trCode">
            <el-input v-model="formData.trCode" placeholder="请输入交易码" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="上级菜单码" prop="uppMenuCode">
            <el-input v-model="formData.uppMenuCode" placeholder="请输入上级菜单码" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="菜单级别" prop="menuLevel">
            <el-input v-model="formData.menuLevel" placeholder="请输入菜单级别" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="菜单分类" prop="menuKind">
            <el-select v-model="formData.menuKind" placeholder="请选择菜单分类">
              <el-option label="菜单" value="1" />
              <el-option label="按钮" value="2" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="权限校验" prop="menuVerify">
            <el-select v-model="formData.menuVerify" placeholder="请选择权限校验">
              <el-option label="是" value="1" />
              <el-option label="否" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="菜单显示" prop="menuDisplay">
            <el-select v-model="formData.menuDisplay" placeholder="请选择菜单显示">
              <el-option label="显示" value="1" />
              <el-option label="隐藏" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="菜单选中" prop="menuChecked">
            <el-select v-model="formData.menuChecked" placeholder="请选择菜单选中">
              <el-option label="选中" value="1" />
              <el-option label="未选中" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="系统编码" prop="subsystemCode">
            <el-input v-model="formData.subsystemCode" placeholder="请输入系统编码" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="文件夹编码" prop="folderCode">
            <el-input v-model="formData.folderCode" placeholder="请输入文件夹编码" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="管理员可用" prop="isAdmin">
            <el-select v-model="formData.isAdmin" placeholder="请选择">
              <el-option label="是" value="1" />
              <el-option label="否" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="操作员可用" prop="isOperator">
            <el-select v-model="formData.isOperator" placeholder="请选择">
              <el-option label="是" value="1" />
              <el-option label="否" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="菜单属性" prop="menuAttribute">
            <el-select v-model="formData.menuAttribute" placeholder="请选择菜单属性">
              <el-option label="普通" value="1" />
              <el-option label="特殊" value="2" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="排序编号" prop="sortNo">
            <el-input v-model="formData.sortNo" placeholder="请输入排序编号" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="菜单类型" prop="menuType">
            <el-select v-model="formData.menuType" placeholder="请选择菜单类型">
              <el-option label="页面" value="1" />
              <el-option label="链接" value="2" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="菜单链接" prop="menuHerf">
            <el-input v-model="formData.menuHerf" placeholder="请输入菜单链接" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="审批标志" prop="workflowFlag">
            <el-select v-model="formData.workflowFlag" placeholder="请选择">
              <el-option label="是" value="1" />
              <el-option label="否" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="页面缓存" prop="isKeepAlive">
            <el-select v-model="formData.isKeepAlive" placeholder="请选择">
              <el-option label="是" value="1" />
              <el-option label="否" value="0" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
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

// 定义组件的 props 和 emits
const emit = defineEmits(['update-success'])

// 响应式数据
const dialogVisible = ref(false)
const submitLoading = ref(false)
const formRef = ref()

// 表单数据
const formData = reactive({
  menuName: '',
  menuCode: '',
  trCode: '',
  uppMenuCode: '',
  menuLevel: 1,
  menuKind: '',
  menuVerify: '',
  menuDisplay: '',
  menuChecked: '',
  subsystemCode: '',
  folderCode: '',
  isAdmin: '',
  isOperator: '',
  menuAttribute: '',
  sortNo: 0,
  menuType: '',
  menuHerf: '',
  workflowFlag: '',
  isKeepAlive: '',
})

// 表单验证规则
const rules = {
  menuName: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  menuCode: [{ required: true, message: '请输入菜单码', trigger: 'blur' }],
}

// 打开弹窗
const show = (rowData: any) => {
  dialogVisible.value = true
  // 将行数据复制到表单数据中
  Object.keys(formData).forEach((key) => {
    if (rowData[key] !== undefined) {
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
    if (typeof formData[key] === 'string') {
      formData[key] = ''
    } else if (typeof formData[key] === 'number') {
      formData[key] = key === 'menuLevel' ? 1 : 0
    }
  })
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitLoading.value = true

    // 这里添加实际的提交逻辑，比如调用API
    // await updateMenu(formData)

    ElMessage.success('编辑成功')
    emit('update-success')
    handleClose()
  } catch (error) {
    console.error('表单验证失败:', error)
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
</style>
