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
      <el-descriptions title="接口信息" :column="2" border>
        <el-descriptions-item label="接口名称">
          {{ trDetail.trName }}
        </el-descriptions-item>
        <el-descriptions-item label="交易码">
          {{ trDetail.trCode }}
        </el-descriptions-item>
        <!-- 根据实际返回的数据结构添加更多字段 -->
        <el-descriptions-item label="创建时间" v-if="trDetail.createTime">
          {{ trDetail.createTime }}
        </el-descriptions-item>
        <el-descriptions-item label="更新时间" v-if="trDetail.updateTime">
          {{ trDetail.updateTime }}
        </el-descriptions-item>
        <el-descriptions-item label="状态" v-if="trDetail.status">
          <el-tag :type="trDetail.status === 'active' ? 'success' : 'warning'">
            {{ trDetail.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="描述" v-if="trDetail.description" span="2">
          {{ trDetail.description }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <div v-else class="no-data">
      <el-empty description="未找到交易信息" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const trDetail = ref(null)

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
