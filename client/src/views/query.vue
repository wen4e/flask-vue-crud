<template>
  <div class="title">页面名称</div>
  <el-input class="w-64" v-model="pageName" placeholder="请输入页面名称"></el-input>
</template>

<script setup>
import { ref } from "vue";
const pageName = ref("");
</script>

<style lang="scss" scoped></style>
