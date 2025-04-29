const MENU_LEVEL_ENUM = {
  '0': '顶层菜单',
  '1': '一级菜单',
  '2': '二级菜单',
  '3': '三级菜单',
  '4': '四级菜单',
}

const MENU_TYPE_ENUM = {
  A: '查询类',
  C: '设置类',
}

const ENABLE_ENUM = {
  '0': '否',
  '1': '是',
}
const MENU_KIND_ENUM = {
  '0': '菜单',
  '1': '事件',
}
const MENU_VERIFY_ENUM = {
  '0': '不校验',
  '1': '校验自身',
  '2': '校验上级',
}
const MENU_DISPLAY_ENUM = {
  '0': '不显示',
  '1': '显示',
}
const MENU_CHECKED_ENUM = {
  '0': '普通',
  '1': '联动选中',
}
const WORKFLOW_ASSIGNEE_MODE_ENUM = {
  '0': '自动选择',
  '1': '弹窗选择',
}
const MENU_ATTRIBUTE_ENUM = {
  '00000000': '免登菜单',
  '10000000': '普通菜单',
  '90000000': '登录菜单',
}

const MENU_SCOPE_ENUM = {
  '1001': '企业PC',
  '1002': '企业APP',
  '4001': '银行PC',
}

export default {
  MENU_LEVEL_ENUM,
  MENU_TYPE_ENUM,
  ENABLE_ENUM,
  MENU_SCOPE_ENUM,
  MENU_KIND_ENUM,
  MENU_VERIFY_ENUM,
  MENU_DISPLAY_ENUM,
  MENU_CHECKED_ENUM,
  WORKFLOW_ASSIGNEE_MODE_ENUM,
  MENU_ATTRIBUTE_ENUM,
}

interface EnumObject {
  [key: string]: string
}

interface KeyValue {
  key: string
  value: string
}

export function transferEnumObj2Arr(enumObj: EnumObject): KeyValue[] {
  return Object.keys(enumObj).map((item) => ({ key: item, value: enumObj[item] }))
}
