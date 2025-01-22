<template>
  <div class="text-base mb-2">查询页面名称</div>
  <el-input class="w-64" v-model="pageName" placeholder="请输入查询页面名称" maxlength="10"></el-input>
  <el-button @click="submit" class="ml-2">生成</el-button>
  <div class="text-sm mt-2">{{ result }}</div>
</template>

<script setup>
import { ref } from "vue";
import api from "@/api";
const pageName = ref("");
const result = ref("");

const isCamelCase = (str) => {
  // 正则表达式规则:
  // ^[a-z] - 首字母必须小写
  // [a-zA-Z0-9]* - 后面可以是任意数量的字母和数字
  const camelCaseRegex = /^[a-z][a-zA-Z0-9]*$/;
  return camelCaseRegex.test(str);
};
// 提交转换请求
const MAX_RETRIES = 5;
const RETRY_DELAY = 300; // 1秒延迟

const submit = async (retryCount = 0) => {
  const prompt0 = `你是一位专业的文本转换大语言模型，请按照以下规则将输入字符串【${pageName.value}】转换成以小写开头的纯英文驼峰格式（camelCase）并直接输出结果：
1. 若输入中包含中文或其他语言字符，请尽量以合理的音译或译词来表达中文含义；
2. 只保留英文字母 (a-z, A-Z)，不包含数字、符号、空格等其他字符；
3. 输出必须是小写开头的驼峰格式，如 "questionRecord"、"userList"、"myHomePage" 等；
4. 最终只输出转换后的结果字符串，不要带任何附加说明或标点；
5. 若遇到无法直接翻译或音译的字符，也请尽量选取最接近的英文单词或简写。
**示例：**
- 输入：「问题记录」 => 输出：「questionRecord」
- 输入：「用户列表」 => 输出：「userList」
请将【${pageName.value}】转换并仅输出处理结果。`;
  const prompt1 = `请将【${pageName.value}】翻译成英文`;
  const res = await api.post("/chat", { prompt: prompt1 });
  const { data } = res;
  if (isCamelCase(data)) {
    result.value = data;
    return data; // 返回成功结果
  }
  if (retryCount < MAX_RETRIES) {
    await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY));
    console.log("重试次数:", retryCount + 1);
    // 等待重试结果并返回
    return await submit(retryCount + 1);
  }
};
</script>
