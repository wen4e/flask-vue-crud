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

// 表格格式化函数
const formatterMenuKind = ({ cellValue }: { cellValue: keyof typeof MENU_KIND_ENUM }) => {
  return MENU_KIND_ENUM[cellValue]
}
const formatterMenuVerify = ({ cellValue }: { cellValue: keyof typeof MENU_VERIFY_ENUM }) => {
  return MENU_VERIFY_ENUM[cellValue]
}
const formatterMenuDisplay = ({ cellValue }: { cellValue: keyof typeof MENU_DISPLAY_ENUM }) => {
  return MENU_DISPLAY_ENUM[cellValue]
}
const formatterMenuChecked = ({ cellValue }: { cellValue: keyof typeof MENU_CHECKED_ENUM }) => {
  return MENU_CHECKED_ENUM[cellValue]
}
const formatterMenuAttribute = ({ cellValue }: { cellValue: keyof typeof MENU_ATTRIBUTE_ENUM }) => {
  return MENU_ATTRIBUTE_ENUM[cellValue]
}
const formatterMenuType = ({ cellValue }: { cellValue: keyof typeof MENU_TYPE_ENUM }) => {
  return MENU_TYPE_ENUM[cellValue]
}
const formatterFlag = ({ cellValue }: { cellValue: keyof typeof ENABLE_ENUM }): string => {
  return ENABLE_ENUM[cellValue]
}

export default {
  // 只导出格式化函数
  formatterMenuKind,
  formatterMenuVerify,
  formatterMenuDisplay,
  formatterMenuChecked,
  formatterMenuAttribute,
  formatterMenuType,
  formatterFlag,
}
