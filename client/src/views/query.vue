<template>
  <div class="text-base mb-2">查询页面名称</div>
  <el-input class="w-64" v-model="pageName" placeholder="请输入查询页面名称" maxlength="10"></el-input>
  <el-button @click="submit" class="ml-2">生成</el-button>
  <div class="text-sm mt-2">{{ result }}</div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api";
const pageName = ref("");
const result = ref("");
const submit = () => {
  const prompt = `请帮我生成一个符合要求的前端.vue页面名称,名称是[${pageName.value}]，要求返回驼峰格式的英文名称，返回的结果是纯英文，例如：userList`;
  api.post("/chat", { prompt }).then((res) => {
    result.value = res.data;
  });
};
</script>
