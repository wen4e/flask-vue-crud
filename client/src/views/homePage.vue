<template>
  <div></div>
</template>

<script setup>
import { getRandomString } from "@/utils/tools";
import axios from "axios";
import { useLocalStorage } from "@vueuse/core";
const SerialNo = getRandomString(22);
// 获取菜单列表
const getMenuList = async () => {
  try {
    const loginInfo = useLocalStorage("loginInfo", {});
    const response = await axios.post("/tbspApi/tbsp/tool-pageMenu", { headUserNo: loginInfo.value.userId, headTrDate: "20250210", headSerialNo: SerialNo, headReqDate: "20250210", headReqTime: "195219", headReqSerialNo: SerialNo, headOrigDate: "20250210", headOrigTime: "195219", headOrigSerialNo: SerialNo, language: "1", menuScope: "4001", trCode: "", menuCode: null, menuName: null, isAdmin: "", isOperator: "", uppMenuCode: "bank-transactionBank", menuCodeLike: null, menuNameLike: null, copyClick: true, pager: false, headMenuCode: "tool-pageMenu" });
    const menuList = response.data;
    useLocalStorage("menuList", menuList);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};
// 登录
const login = async () => {
  try {
    const response = await axios.post("/tbspApi/tbsp/bank/tool/login", { headUserNo: "jres", headTrDate: "20250210", headSerialNo: SerialNo, headReqDate: "20250210", headReqTime: "193246", headReqSerialNo: SerialNo, headOrigDate: "20250210", headOrigTime: "193246", headOrigSerialNo: SerialNo, language: "1", orgNo: "", userNo: "jres", passwd: "33240f293bd2daad67ab8b1c6964b1b9", verificationCode: "", headChannel: "01", headOrgNo: "1", headCustNo: "000400000009999", headMenuCode: "bank", headTrCode: "tool" });
    const loginInfo = response.data;
    useLocalStorage("loginInfo", loginInfo);
    getMenuList();
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

login();
</script>
