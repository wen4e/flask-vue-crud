<template>
  <div class="text-base mb-2">查询页面名称</div>
  <el-input class="w-64" v-model="pageName" placeholder="请输入查询页面名称"></el-input>
  <el-button @click="submit">生成</el-button>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api";
const pageName = ref("");
const submit = () => {
  api.post("/chat", { prompt: pageName.value }).then((res) => {
    console.log(res);
  });
};
</script>
