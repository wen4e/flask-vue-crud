<template>
  <vxe-table ref="tableRef" border stripe :loading="loading" :tree-config="treeConfig" :data="menuList" :checkbox-config="checkboxConfig" :edit-config="editConfig">
    <vxe-column type="checkbox" title="菜单名称" tree-node width="auto" fixed="left"></vxe-column>
    <vxe-column field="menuCode" title="菜单码" :edit-render="{ name: 'VxeInput' }" width="auto"></vxe-column>
    <vxe-column field="trCode" title="交易码" width="auto"></vxe-column>
    <vxe-column field="uppMenuCode" title="上级菜单编码" width="auto"></vxe-column>
    <vxe-column field="menuLevel" title="菜单级别" width="auto"></vxe-column>
    <vxe-column field="menuKind" title="菜单分类" width="auto" :formatter="formatterMenuKind"></vxe-column>
    <vxe-column field="menuVerify" title="权限校验" width="auto" :formatter="formatterMenuVerify"></vxe-column>
    <vxe-column field="menuDisplay" title="菜单显示" width="auto" :formatter="formatterMenuDisplay"></vxe-column>
    <vxe-column field="menuChecked" title="菜单选中" width="auto" :formatter="formatterMenuChecked"></vxe-column>
    <vxe-column field="subsystemCode" title="系统编码" width="auto"></vxe-column>
    <vxe-column field="folderCode" title="文件夹编码" width="auto"></vxe-column>
    <vxe-column field="isAdmin" title="管理员是否可用" width="auto" :formatter="formatterFlag"></vxe-column>
    <vxe-column field="isOperator" title="操作员是否可用" width="auto" :formatter="formatterFlag"></vxe-column>
    <vxe-column field="menuAttribute" title="菜单属性" width="auto" :formatter="formatterMenuAttribute"></vxe-column>
    <vxe-column field="sortNo" title="排序编号" width="auto"></vxe-column>
    <vxe-column field="menuType" title="菜单类型" width="auto" :formatter="formatterMenuType"></vxe-column>
    <vxe-column field="menuHerf" title="菜单链接" width="auto"></vxe-column>
    <vxe-column field="workflowFlag" title="审批标志" width="auto" :formatter="formatterFlag"></vxe-column>
    <vxe-column field="isKeepAlive" title="页面是否缓存" width="auto" :formatter="formatterFlag"></vxe-column>
    <vxe-column title="操作" width="125" fixed="right">
      <template #default="{ row }">
        <template v-if="hasEditStatus(row)">
          <el-tooltip effect="dark" content="保存" placement="top">
            <el-icon class="mr-2 cursor-pointer" @click="saveRowEvent(row)"><Check /></el-icon>
          </el-tooltip>
          <el-tooltip effect="dark" content="取消" placement="top">
            <el-icon class="mr-2 cursor-pointer" @click="cancelRowEvent()"><Close /></el-icon>
          </el-tooltip>
        </template>
        <template v-else>
          <el-tooltip effect="dark" content="编辑" placement="top">
            <el-icon class="mr-2 cursor-pointer" @click="editRowEvent(row)"><Edit /></el-icon>
          </el-tooltip>
        </template>
        <el-tooltip effect="dark" content="复制" placement="top">
          <el-icon class="mr-2 cursor-pointer" @click="copyRowEvent(row)"><CopyDocument /></el-icon>
        </el-tooltip>
        <el-tooltip effect="dark" content="删除" placement="top">
          <el-icon class="mr-2 cursor-pointer" @click="delRowEvent(row)"><Delete /></el-icon>
        </el-tooltip>
        <el-tooltip effect="dark" content="生成页面" placement="top">
          <el-icon class="cursor-pointer" @click="generatePageRowEvent(row)"><Document /></el-icon>
        </el-tooltip>
      </template>
    </vxe-column>
  </vxe-table>
  <generate-page-dialog ref="generatePageDialogRef" />
</template>

<script setup>
import generatePageDialog from "./components/generatePageDialog.vue";
import { ElMessage } from "element-plus";
import { getRandomString } from "@/utils/tools";
import enums from "@/utils/menuCommon";
import axios from "axios";
import { useLocalStorage } from "@vueuse/core";
import { ref, reactive } from "vue";
let menuList = ref([]);
const generatePageDialogRef = ref(null); // 新增的 ref
const treeConfig = reactive({
  transform: true,
  rowField: "menuCode",
  parentField: "uppMenuCode",
});
const checkboxConfig = reactive({
  labelField: "menuName",
  highlight: true,
});
const editConfig = reactive({
  trigger: "manual",
  mode: "row",
});
const SerialNo = getRandomString(22);
// 表格格式化
const formatterMenuKind = ({ cellValue }) => {
  return enums.MENU_KIND_ENUM[cellValue];
};
const formatterMenuVerify = ({ cellValue }) => {
  return enums.MENU_VERIFY_ENUM[cellValue];
};
const formatterMenuDisplay = ({ cellValue }) => {
  return enums.MENU_DISPLAY_ENUM[cellValue];
};
const formatterMenuChecked = ({ cellValue }) => {
  return enums.MENU_CHECKED_ENUM[cellValue];
};
const formatterMenuAttribute = ({ cellValue }) => {
  return enums.MENU_ATTRIBUTE_ENUM[cellValue];
};
const formatterMenuType = ({ cellValue }) => {
  return enums.MENU_TYPE_ENUM[cellValue];
};
const formatterFlag = ({ cellValue }) => {
  return enums.ENABLE_ENUM[cellValue];
};
// 操作栏
const loading = ref(false);
const tableRef = ref();
const hasEditStatus = (row) => {
  const $table = tableRef.value;
  if ($table) {
    return $table.isEditByRow(row);
  }
};
// 编辑
const editRowEvent = (row) => {
  const $table = tableRef.value;
  if ($table) {
    $table.setEditRow(row);
  }
};
// 保存
const saveRowEvent = (row) => {
  const $table = tableRef.value;
  if ($table) {
    $table.clearEdit().then(() => {
      loading.value = true;
      setTimeout(() => {
        loading.value = false;
        ElMessage({
          message: "Congrats, this is a success message.",
          type: "success",
        });
      }, 300);
    });
  }
};
// 取消编辑
const cancelRowEvent = () => {
  const $table = tableRef.value;
  if ($table) {
    $table.clearEdit();
  }
};
// 复制
const copyRowEvent = (row) => {
  const $table = tableRef.value;
  if ($table) {
  }
};
// 生成页面
const generatePageRowEvent = (row) => {
  if (generatePageDialogRef.value) {
    generatePageDialogRef.value.show(row);
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
// 获取菜单列表
const getMenuList = async () => {
  try {
    const loginInfo = useLocalStorage("loginInfo", {});
    const response = await axios.post("/tbspApi/tbsp/tool-pageMenu", { headUserNo: loginInfo.value.userId, headTrDate: "20250210", headSerialNo: SerialNo, headReqDate: "20250210", headReqTime: "195219", headReqSerialNo: SerialNo, headOrigDate: "20250210", headOrigTime: "195219", headOrigSerialNo: SerialNo, language: "1", menuScope: "4001", trCode: "", menuCode: null, menuName: null, isAdmin: "", isOperator: "", uppMenuCode: "bank-transactionBank", menuCodeLike: null, menuNameLike: null, copyClick: true, pager: false, headMenuCode: "tool-pageMenu" });
    menuList.value = response.data.dtos;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};
</script>
