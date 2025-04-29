<template>
  <el-dialog v-model="dialogVisible" title="生成页面" width="500">
    <el-form :model="form">
      <h3>{{ data.menuName }}</h3>
      <el-form-item label="页面名称">
        <el-input v-model="form.pageName" autocomplete="off" clearable />
      </el-form-item>
      <el-form-item label="页面路径">
        <el-input v-model="form.pagePath" autocomplete="off" clearable />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogVisible = false"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
const dialogVisible = ref(false)
let form = reactive({
  pageName: '',
  pagePath: '',
})
let data = reactive({
  menuName: '',
})
const show = (row) => {
  data = row
  console.log('🚀 ~ show ~ data:', data)
  form.pageName = row.menuCode
  form.pagePath = row.menuHerf
  dialogVisible.value = true
}
// 暴露给父组件使用
defineExpose({ show })
</script>

<style lang="scss" scoped></style>
