<template>
  <div class="text-base mb-2">查询页面名称</div>
  <el-input class="w-64" v-model="pageName" placeholder="请输入查询页面名称"></el-input>
</template>

<script setup>
import { ref } from "vue";
const pageName = ref("");
</script>

<style lang="scss" scoped></style>
