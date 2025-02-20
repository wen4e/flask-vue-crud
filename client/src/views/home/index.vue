<template>
  <div>
    <!-- 搜索输入框 -->
    <vxe-input v-model="filterName" type="search" placeholder="搜索菜单" clearable @change="searchEvent" style="margin-bottom: 16px"></vxe-input>

    <vxe-table ref="tableRef" show-overflow :column-config="{ resizable: true }" :scroll-y="{ enabled: true, gt: 0 }" height="600" border stripe :loading="loading" :tree-config="{ transform: true, rowField: 'menuCode', parentField: 'uppMenuCode' }" :data="menuList" :checkbox-config="{ labelField: 'menuName', highlight: true }" :edit-config="{ trigger: 'manual', mode: 'row' }">
      <vxe-column type="checkbox" title="菜单名称" tree-node width="320" fixed="left"></vxe-column>
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
      <vxe-column title="操作" width="110" fixed="right">
        <template #default="{ row }">
          <template v-if="hasEditStatus(row)">
            <el-tooltip effect="dark" content="保存" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="saveRowEvent(row)">
                <Check />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="取消" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="cancelRowEvent()">
                <Close />
              </el-icon>
            </el-tooltip>
          </template>
          <template v-else>
            <el-tooltip effect="dark" content="编辑" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="editRowEvent(row)">
                <Edit />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="复制" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="copyRowEvent(row)">
                <CopyDocument />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="删除" placement="top">
              <el-icon class="mr-2 cursor-pointer" @click="delRowEvent(row)">
                <Delete />
              </el-icon>
            </el-tooltip>
            <el-tooltip effect="dark" content="生成页面" placement="top">
              <el-icon class="cursor-pointer" @click="generatePageRowEvent(row)">
                <Document />
              </el-icon>
            </el-tooltip>
          </template>
        </template>
      </vxe-column>
    </vxe-table>
    <generate-page-dialog ref="generatePageDialogRef" />
  </div>
</template>

<script setup>
import generatePageDialog from "./components/generatePageDialog.vue";
import { ElMessage } from "element-plus";
import { getRandomString } from "@/utils/tools";
import enums from "@/utils/menuCommon";
import axios from "axios";
import { useLocalStorage } from "@vueuse/core";
import { ref, nextTick } from "vue";
import XEUtils from "xe-utils";

let SerialNo = "";

// 新增变量：用于存储接口返回的完整菜单数据，用于搜索过滤
let originalMenuList = [];

// 搜索框绑定值
const filterName = ref("");

// 表格相关
const loading = ref(false);
const tableRef = ref();
let menuList = ref([]);

// 表格格式化函数
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

// 操作栏方法
const hasEditStatus = (row) => {
  const $table = tableRef.value;
  if ($table) {
    return $table.isEditByRow(row);
  }
};
const editRowEvent = (row) => {
  const $table = tableRef.value;
  if ($table) {
    $table.setEditRow(row);
  }
};
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
const cancelRowEvent = () => {
  const $table = tableRef.value;
  if ($table) {
    $table.clearEdit();
  }
};
const copyRowEvent = (row) => {
  const $table = tableRef.value;
  if ($table) {
    // 示例: 复制当前行数据处理逻辑
  }
};
const generatePageDialogRef = ref(null);
const generatePageRowEvent = (row) => {
  if (generatePageDialogRef.value) {
    generatePageDialogRef.value.show(row);
  }
};

// 登录方法
const login = async () => {
  SerialNo = getRandomString(22);
  try {
    const response = await axios.post("/tbspApi/tbsp/bank/tool/login", {
      headUserNo: "jres",
      headTrDate: "20250210",
      headSerialNo: SerialNo,
      headReqDate: "20250210",
      headReqTime: "193246",
      headReqSerialNo: SerialNo,
      headOrigDate: "20250210",
      headOrigTime: "193246",
      headOrigSerialNo: SerialNo,
      language: "1",
      orgNo: "",
      userNo: "jres",
      passwd: "33240f293bd2daad67ab8b1c6964b1b9",
      verificationCode: "",
      headChannel: "01",
      headOrgNo: "1",
      headCustNo: "000400000009999",
      headMenuCode: "bank",
      headTrCode: "tool",
    });
    const loginInfo = response.data;
    useLocalStorage("loginInfo", loginInfo);
    if (response.data.respType === "S") {
      getMenuList();
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// 获取菜单列表（接口返回数据同时存入 originalMenuList 供搜索使用）
const getMenuList = async () => {
  SerialNo = getRandomString(22);
  try {
    const loginInfo = useLocalStorage("loginInfo", {});
    const response = await axios.post("/tbspApi/tbsp/tool-pageMenu", {
      headUserNo: loginInfo.value.userId,
      headTrDate: "20250210",
      headSerialNo: SerialNo,
      headReqDate: "20250210",
      headReqTime: "195219",
      headReqSerialNo: SerialNo,
      headOrigDate: "20250210",
      headOrigTime: "195219",
      headOrigSerialNo: SerialNo,
      language: "1",
      menuScope: "4001",
      trCode: "",
      menuCode: null,
      menuName: null,
      isAdmin: "",
      isOperator: "",
      uppMenuCode: "bank-transactionBank",
      menuCodeLike: null,
      menuNameLike: null,
      copyClick: true,
      pager: false,
      headMenuCode: "tool-pageMenu",
    });
    if (response.data.respType === "S") {
      // 将获取到的数据同时赋值给原始数据和当前显示数据
      originalMenuList = response.data.dtos;
      menuList.value = response.data.dtos;
      nextTick(() => {
        const treeData = tableRef.value.getTableData();
        const firstLevelNodes = treeData.tableData;
        tableRef.value
          .setTreeExpand(firstLevelNodes, true)
          .then(() => {})
          .catch((err) => {
            console.error("展开节点失败:", err);
          });
      });
    } else {
      login();
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// 搜索函数：根据 filterName 过滤菜单数据（示例中以 menuName 和 menuCode 字段作为匹配）
const handleSearch = () => {
  const filterVal = filterName.value.trim().toLowerCase();
  if (filterVal) {
    menuList.value = originalMenuList.filter((item) => ["menuName", "menuCode", "trCode", "uppMenuCode"].some((key) => item[key] && item[key].toLowerCase().includes(filterVal)));
  } else {
    menuList.value = originalMenuList;
    nextTick(() => {
      const treeData = tableRef.value.getTableData();
      const firstLevelNodes = treeData.tableData;
      tableRef.value
        .setTreeExpand(firstLevelNodes, true)
        .then(() => {})
        .catch((err) => {
          console.error("展开节点失败:", err);
        });
    });
  }
};

// 节流搜索，避免频繁触发
const searchEvent = XEUtils.throttle(handleSearch, 500, { trailing: true, leading: true });

// 初始化加载菜单列表
getMenuList();
</script>
