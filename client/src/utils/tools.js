
// 校验是否为驼峰格式
export const isCamelCase = (str) => {
  // 正则表达式规则:
  // ^[a-z] - 首字母必须小写
  // [a-zA-Z0-9]* - 后面可以是任意数量的字母和数字
  const camelCaseRegex = /^[a-z][a-zA-Z0-9]*$/;
  return camelCaseRegex.test(str);
};

// 合并提取单词和格式化功能
export const formatCamelCase = (str) => {
  // 1. 提取英文单词
  const words = str.match(/[a-zA-Z][a-z]*/g);
  if (!words) return '';

  // 2. 格式化处理
  // 处理首个单词，确保首字母小写
  words[0] = words[0].toLowerCase();

  // 处理后续单词，确保首字母大写
  for (let i = 1; i < words.length; i++) {
    words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1).toLowerCase();
  }

  // 合并所有单词
  return words.join('');
};

export const getRandomString = (len) => {
  len = len || 32;
  let $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'; // 默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1
  let maxPos = $chars.length;
  let randomString = '';
  for (let i = 0; i < len; i++) {
    randomString += $chars.charAt(Math.floor(Math.random() * maxPos));
  }
  return randomString;
}