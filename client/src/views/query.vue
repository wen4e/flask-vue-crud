<template>
  <div class="text-base mb-2">生成页面</div>
  <el-form :model="formData" :rules="formRules" class="w-1/2" ref="formRef" label-width="120px">
    <el-form-item label="查询页面名称" prop="pageName">
      <el-input v-model.trim="formData.pageName" placeholder="请输入查询页面名称" maxlength="10" :clearable="true"></el-input>
    </el-form-item>
    <el-form-item label="">
      <el-button @click="submit()" type="primary">页面名称</el-button>
    </el-form-item>
  </el-form>
  <div class="mt-4 mb-4">
    <span class="text-sm">页面名称：</span>
    {{ result }}
  </div>
  <el-button @click="handlepage()" type="primary">生成页面</el-button>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { ref, reactive } from 'vue'
import api from '@/api'
const result = ref('')
const formRef = ref(null)
const formData = reactive({
  pageName: '',
})
const formRules = {
  pageName: [
    { required: true, message: '请输入查询页面名称', trigger: 'blur' },
    {
      validator(rule, value, callback) {
        if (!/^[\u4e00-\u9fa5]+$/.test(value)) {
          callback(new Error('只能输入中文'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

const submit = async () => {
  // 添加表单验证
  if (!formRef.value) return

  const res = await api.post('/cozeApp', {
    workflow_id: '7502280447989121075',
    app_id: '7502253112191860774',
    parameters: { input: formData.pageName },
  })
  // 假设 res.data 是 "{\"output\":\"userInput\"}" 这样的字符串
  try {
    const parsedData = JSON.parse(res.data)
    if (parsedData && parsedData.output) {
      result.value = parsedData.output
    } else {
      // 如果解析后的数据没有 output 属性，或者解析失败，可以设置一个默认值或错误提示
      result.value = '无效的响应格式'
      console.error('Parsed data does not contain output:', parsedData)
    }
  } catch (error) {
    // JSON 解析失败处理
    result.value = '解析响应失败'
    console.error('Failed to parse JSON response:', error)
    ElMessage.error('从服务器获取的响应格式不正确')
  }
}

// 生成页面
const handlepage = () => {
  if (!result.value) {
    ElMessage.error('请先转换页面名称')
    return
  }
  api.post('/createPage', { pageName: result.value }).then((res) => {
    console.log(res)
  })
}
</script>
