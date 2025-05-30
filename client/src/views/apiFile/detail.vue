<template>
  <div class="container">
    <div class="detail-header">
      <el-button @click="goBack" type="default">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>接口详情</h2>
    </div>

    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else-if="trDetail" class="detail-content">
      <el-descriptions title="接口信息">
        <el-descriptions-item label="接口名称">
          {{ trDetail.apiName }}
        </el-descriptions-item>
        <el-descriptions-item label="交易码">
          {{ trDetail.trCode }}
        </el-descriptions-item>
      </el-descriptions>

      <el-descriptions title="请求参数" style="margin-top: 20px">
        <el-descriptions-item v-for="(value, key) in trDetail.requestParams" :key="key" :label="key">
          {{ value }}
        </el-descriptions-item>
      </el-descriptions>

      <el-descriptions title="响应参数" style="margin-top: 20px">
        <el-descriptions-item v-for="(value, key) in responseParamsWithoutDtos" :key="key" :label="key">
          {{ value }}
        </el-descriptions-item>
      </el-descriptions>

      <el-descriptions v-for="(dto, index) in trDetail.responseParams.dtos" :key="index" :title="`响应数据 ${index + 1}`" style="margin-top: 20px">
        <el-descriptions-item v-for="(value, key) in dto" :key="key" :label="key">
          {{ value }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <div v-else class="no-data">
      <el-empty description="未找到交易信息" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const trDetail = ref(null)

// 计算属性：获取除了dtos之外的响应参数
const responseParamsWithoutDtos = computed(() => {
  if (!trDetail.value?.responseParams) return {}
  const { dtos, ...otherParams } = trDetail.value.responseParams
  return otherParams
})

// 获取交易详情
const getTrDetail = async (trCode: string) => {
  if (!trCode) {
    ElMessage.error('交易码不能为空')
    return
  }

  loading.value = true
  try {
    const res = await api.get('/trCode', {
      params: { trCode },
    })

    // 检查接口返回状态
    if (res.data.status === 'success') {
      trDetail.value = res.data.data || null
      if (!trDetail.value) {
        ElMessage.warning('未找到对应的交易信息')
      }
    } else {
      // 失败时显示错误信息
      const errorMsg = res.data.message || '获取交易详情失败'
      ElMessage.error(errorMsg)
      trDetail.value = null
    }
  } catch (error) {
    console.error('获取交易详情失败:', error)
    ElMessage.error('获取交易详情失败')
  } finally {
    loading.value = false
  }
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 生命周期钩子
onMounted(() => {
  const trCode = route.query.trCode as string
  if (trCode) {
    getTrDetail(trCode)
  } else {
    ElMessage.error('缺少交易码参数')
  }
})
</script>

<style lang="scss" scoped>
.container {
  padding: 20px;
}

.detail-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 12px;

  h2 {
    margin: 0;
    color: #303133;
  }
}

.loading {
  margin-top: 20px;
}

.detail-content {
  margin-top: 20px;
}

.no-data {
  margin-top: 40px;
  text-align: center;
}

:deep(.el-descriptions__title) {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
</style>
