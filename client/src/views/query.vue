<template>
  <div class="title">页面名称</div>
  <div class="w-64">
    <el-input class="w-64" v-model="pageName" placeholder="请输入页面名称"></el-input>
  </div>
</template>

<script setup>
import { ref } from "vue";
const pageName = ref("");
</script>

<style lang="scss" scoped></style>
