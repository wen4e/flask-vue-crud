<template>
  <el-form-item label="网关地址">
    <el-select v-model="gatewayAddress" placeholder="请选择网关地址" @change="handleGatewayChange" class="w-[300px]">
      <el-option v-for="item in gatewayOptions" :key="item.url" :label="item.name" :value="item.url">
        <div class="flex items-center justify-between w-full">
          <div>
            <span>{{ item.name }}</span>
            <span class="text-gray-500 ml-3"> {{ item.url }} </span>
          </div>
          <el-icon v-if="item.url !== gatewayAddress" @click.stop="handleDeleteGateway(item)" class="cursor-pointer text-red-500 ml-5" size="16">
            <Delete />
          </el-icon>
        </div>
      </el-option>
      <template #footer>
        <div class="p-2 border-t">
          <el-button type="primary" size="small" @click="showAddDialog = true" class="w-full">
            <el-icon><Plus /></el-icon>
            新增网关地址
          </el-button>
        </div>
      </template>
    </el-select>
  </el-form-item>
  <!-- 新增网关地址对话框 -->
  <el-dialog v-model="showAddDialog" title="新增网关地址" width="500px">
    <el-form :model="addForm" :rules="addRules" ref="addFormRef" label-width="80px">
      <el-form-item class="w-full" label="名称" prop="name">
        <el-input v-model="addForm.name" placeholder="请输入网关名称" />
      </el-form-item>
      <el-form-item class="w-full" label="API地址" prop="url">
        <el-input v-model="addForm.url" placeholder="请输入API地址" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAddGateway">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { safeJsonParse } from '@/utils/tools'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

// 定义组件的props
interface Props {
  onUpdate?: () => void
}

const props = withDefaults(defineProps<Props>(), {
  onUpdate: () => {},
})

// 组件内部状态
const gatewayAddress = ref('')
const gatewayOptions = ref([])
const showAddDialog = ref(false)
const addFormRef = ref()
// 新增表单数据
const addForm = ref({
  name: '',
  url: '',
})
// 表单验证规则
const addRules = {
  name: [{ required: true, message: '请输入网关名称', trigger: 'blur' }],
  url: [
    { required: true, message: '请输入API地址', trigger: 'blur' },
    { type: 'url', message: '请输入正确的URL格式', trigger: 'blur' },
  ],
}
// 定义网关API函数
const gatewayApi = (params: object) => {
  return api.post('/cozeApp', {
    workflow_id: '7507546709079179304',
    app_id: '7502253112191860774',
    parameters: params,
  })
}

// 查询网关地址数据
const getGatewayData = async () => {
  try {
    const res = await gatewayApi({
      type: 'query',
    })
    return safeJsonParse(res.data.data) // 返回解析后的数据
  } catch (error) {
    console.error('请求失败:', error)
    return null // 错误时返回 null
  }
}

// 查询默认网关
const getDefaultGateway = async () => {
  try {
    return await api.get('/gateway/defaultQuery')
  } catch (error) {
    console.error('查询默认网关失败:', error)
    return null // 错误时返回 null
  }
}

// 处理新增网关
const handleAddGateway = async () => {
  if (!addFormRef.value) return

  try {
    const valid = await addFormRef.value.validate()
    if (valid) {
      // 这里可以调用API保存新的网关地址
      // 暂时添加到本地列表中
      const params = {
        name: addForm.value.name,
        url: addForm.value.url,
        type: 'add', // 新增的默认为非活动状态
      }

      const res = await gatewayApi(params)
      const result = safeJsonParse(res.data.data)
      if (!result || !result.status) {
        ElMessage.error(result.msg || '新增网关地址失败，请稍后重试')
        return
      }
      // 重置表单
      addForm.value = { name: '', url: '' }
      showAddDialog.value = false
      // 重新加载网关数据
      initGateway()
      ElMessage.success(result.msg || '网关地址添加成功')
    }
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 处理删除网关
const handleDeleteGateway = async (gateway: any) => {
  try {
    await ElMessageBox.confirm(`确定要删除"${gateway.name}"网关地址吗？此操作不可撤销。`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    // 调用删除API
    const params = {
      url: gateway.url,
      type: 'del',
    }

    const res = await gatewayApi(params)
    const result = safeJsonParse(res.data.data)

    if (!result || !result.status) {
      ElMessage.error(result?.msg || '删除网关地址失败，请稍后重试')
      return
    }

    ElMessage.success(result.msg || '网关地址删除成功')

    // 重新加载网关数据
    initGateway()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除网关地址失败:', error)
      ElMessage.error('删除网关地址失败')
    }
  }
}

// 网关地址切换
const handleGatewayChange = (value: string) => {
  api
    .post('/gateway/change', { gatewayUrl: value })
    .then((response) => {
      if (response.data.success) {
        ElMessage.success('网关地址切换成功')
        // 更新父组件状态
        props.onUpdate?.()
      } else {
        ElMessage.error('切换网关地址失败')
      }
    })
    .catch((error) => {
      console.error('切换网关地址失败:', error)
      ElMessage.error('切换网关地址失败')
    })
}

const initGateway = async () => {
  // 初始化网关地址列表
  const data = await getGatewayData()
  if (data && data.data && data.data.length > 0) {
    gatewayOptions.value = data.data
  }
  // 获取默认网关地址
  const defaultRes = await getDefaultGateway()
  if (defaultRes && defaultRes.data && defaultRes.data.data) {
    gatewayAddress.value = defaultRes.data.data
  }
}

// 暴露给父组件的更新方法
const update = () => {
  initGateway()
}

// 暴露方法给父组件
defineExpose({
  update,
})

// 组件挂载时初始化
onMounted(() => {
  // 调用函数并获取返回值
  initGateway()
})
</script>
