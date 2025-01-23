// 格式化结果字符串,例如：'hello-world' 或 'hello world' => 'helloWorld'
export const formatResult = (str) => {
  // 移除连字符，替换为空格
  let processedStr = str.replace(/-/g, " ");

  // 分割成单词数组，过滤空字符串
  let words = processedStr.split(/\s+/).filter((word) => word.length > 0);

  if (words.length === 0) return "";

  // 处理首个单词，确保首字母小写
  words[0] = words[0].toLowerCase();

  // 处理后续单词，确保首字母大写
  for (let i = 1; i < words.length; i++) {
    words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1).toLowerCase();
  }

  // 合并所有单词
  return words.join("");
};