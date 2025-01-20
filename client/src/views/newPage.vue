<template>
  <div class="container">
    <el-alert type="info" description="请点击按钮，新建一个页面" :closable="false"></el-alert>
    <div class="button-wrap">
      <el-button type="primary" @click="handleClick('QUERY')">新建查询页面</el-button>
      <el-button type="primary" @click="handleClick('EDIT')">新建编辑页面</el-button>
      <el-button type="primary" @click="handleClick('DETAIL')">新建详情页面</el-button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeMount, onBeforeUnmount, onUnmounted, onActivated, onDeactivated } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// 路由跳转方法
const handleClick = (type) => {
  router.push({
    name: type.toLowerCase(),
  });
};

// 生命周期钩子
onMounted(() => {
  // 挂载完成
});

onBeforeMount(() => {
  // 挂载前
});

onBeforeUnmount(() => {
  // 卸载前
});

onUnmounted(() => {
  // 卸载完成
});

onActivated(() => {
  // keep-alive 激活时
});

onDeactivated(() => {
  // keep-alive 停用时
});
</script>

<style lang="scss" scoped>
.button-wrap {
  margin-top: 20px;
}
</style>
