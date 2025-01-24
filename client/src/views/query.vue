<template>
  <div class="text-base mb-2">生成页面</div>
  <el-form :model="formData" :rules="formRules" class="w-1/2" ref="formRef" label-width="120px">
    <el-form-item label="查询页面名称" prop="pageName">
      <el-input v-model.trim="formData.pageName" placeholder="请输入查询页面名称" maxlength="10" :clearable="true"></el-input>
    </el-form-item>
    <el-form-item label="">
      <el-button @click="submit(0)" type="primary">页面名称</el-button>
    </el-form-item>
  </el-form>
  <div class="mt-4 mb-4">
    <span class="text-sm">页面名称：</span>
    {{ result }}
  </div>
  <el-button @click="handlepage()" type="primary">生成页面</el-button>
</template>

<script setup>
import { ElMessage } from "element-plus";
import { isCamelCase, formatCamelCase } from "@/utils/tools";
import { ref, reactive } from "vue";
import api from "@/api";
const result = ref("");
const formRef = ref(null);
const formData = reactive({
  pageName: "",
});
const formRules = {
  pageName: [
    { required: true, message: "请输入查询页面名称", trigger: "blur" },
    {
      validator(rule, value, callback) {
        if (!/^[\u4e00-\u9fa5]+$/.test(value)) {
          callback(new Error("只能输入中文"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
};

// 提交转换请求
const MAX_RETRIES = 5;
const RETRY_DELAY = 300; // 1秒延迟

const submit = async (retryCount = 0) => {
  // 添加表单验证
  if (!formRef.value) return;
  await formRef.value.validate();
  const prompt0 = `请将【${formData.pageName}】翻译成英文，并将结果转换成小写字母开头的驼峰格式（camelCase）并直接输出结果。不需要多余的内容，只需要返回英文单词的驼峰格式即可。`;

  const prompt1 = `你是一位专业的文本转换大语言模型，请按照以下规则将输入字符串【${formData.pageName}】转换成以小写开头的纯英文驼峰格式（camelCase）并直接输出结果：
    1. 若输入中包含中文或其他语言字符，请尽量以合理的音译或译词来表达中文含义；
    2. 只保留英文字母 (a-z, A-Z)，不包含数字、符号、空格等其他字符；
    3. 输出必须是小写开头的驼峰格式，如 "questionRecord"、"userList"、"myHomePage" 等；
    4. 最终只输出转换后的结果字符串，不要带任何附加说明或标点；
    5. 若遇到无法直接翻译或音译的字符，也请尽量选取最接近的英文单词或简写。
    **示例：**
    - 输入：「问题记录」 => 输出：「questionRecord」
    - 输入：「用户列表」 => 输出：「userList」
    请将【${formData.pageName}】转换并仅输出处理结果。`;
  let prompt = prompt0;
  if (retryCount > 1) {
    prompt = prompt1;
  }
  const res = await api.post("/chat", { prompt });
  const { data } = res;
  let formattedData = formatCamelCase(data);
  if (isCamelCase(formattedData)) {
    result.value = formattedData;
    return formattedData; // 返回成功结果
  }
  if (retryCount < MAX_RETRIES) {
    await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY));
    // 等待重试结果并返回
    return await submit(retryCount + 1);
  } else {
    result.value = "转换失败，请检查输入内容";
    return "转换失败，请检查输入内容";
  }
};

// 生成页面
const handlepage = () => {
  if (!result.value) {
    ElMessage.error("请先转换页面名称");
    return;
  }
  api.post("/createPage", { pageName: result.value }).then((res) => {
    console.log(res);
  });
};
</script>
