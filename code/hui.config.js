const { version, name } = require("./package.json");
const path = require('path')
module.exports = {
  // 应用 id
  id: "65996080-bf79-11ea-bbcf-cf306e4ddc9d",
  // 应用类型
  type: "app",
  // 打开之后将使用内置的路由引擎，自动处理路由关系，否则需要手动设置路由
  autoRouting: false,
  // 设置路由前缀，通常用于部署到非根目录
  base: `/frame-layout/${name}/`,
  publicPath: `/${name}/`,
  // 配置路由模式
  mode: "hash",
  // 开启 CSS MODULES 特性设置
  cssModules: false,
  // 插件
  plugins: ["hui-plugin-micro-app", 'hui-plugin-dart', 'hui-plugin-see', 'hui-plugin-jsx', {
    plugin: 'hui-plugin-lint',
    // 插件配置
    options: {
      // 插件配置
      lintOnSave: true,
      fixOnSave: true
    }
  }],
  libs: {
    custRoleTemplateInfo: './src/views/orgManage/custRoleTemplate_info',
    userRoleTemplateInfo: './src/views/orgManage/userRoleTemplate_info',
    orgInfoInfo: './src/views/orgManage/orgInfo_info',
    orgInfoMerge: './src/views/orgManage/orgInfo_merge',
    orgAuthInfo: './src/views/orgManage/orgAuth_info',
    orgRoleInfo: './src/views/orgManage/orgRole_info',
    orgPostInfo: './src/views/orgManage/orgPost_info',
    systemPostInfo: './src/views/orgManage/systemPost_info',
    orgUserInfo: './src/views/orgManage/orgUser_info',
    orgUserReset: './src/views/orgManage/orgUser_reset',
    corpInfoInfo: './src/views/corpManage/corpInfo_info',
    corpAuthInfo: './src/views/corpManage/corpAuth_info',
    corpRoleInfo: './src/views/corpManage/corpRole_info',
    corpPostInfo: './src/views/corpManage/corpPost_info',
    corpMngInfo: './src/views/corpManage/corpMng_info',
    corpMemberMngInfo: './src/views/corpManage/corpMemberMng_info',
    custChoice2: './src/views/common/custChoice2',
    corpUserInfo: './src/views/corpManage/corpUser_info',
    corpUserReset: './src/views/corpManage/corpUser_reset',
    corpUKeyInfo: './src/views/corpManage/corpUKey_info',
    corpUKeyChangeInfo: './src/views/corpManage/corpUKeyChange_info',
    corpUKeyWorkFlow: './src/views/corpManage/corpUKey_workFlow',
    acctInfoInfo: './src/views/acctManage/acctInfo_info',
    acctAuthCorpInfo: './src/views/acctManage/acctAuthCorp_info',
    acctAuthUserDel: './src/views/acctManage/acctAuthUser_del',
    acctAuthUserUpd: './src/views/acctManage/acctAuthUser_upd',
    acctAuthUserInfo: './src/views/acctManage/acctAuthUser_info',
    acctNoticeInfo: './src/views/acctManage/acctNotice_info',
    tfrWhiteInfo: './src/views/payManage/tfrWhite_info',
    tfrLandLimitInfo: './src/views/payManage/tfrLandLimit_info',
    tfrLimitInfo: './src/views/payManage/tfrLimit_info',
    tfrLandProcessInfo: './src/views/payManage/tfrLandProcess_info',
    unionBankNoInfoInfo: './src/views/sysManage/unionBankNoInfo_info',
    noticeInfoInfo: './src/views/sysManage/noticeInfo_info',
  },
  alias: {
    '@utils': '@/utils',
    '@scripts': '@/scripts',
    '@assets': '@/assets',
    '@views': '@/views',
  },
  // 使用 Vuex 进行状态管理
  vuex: true,
  // // 代理
  // proxy: {
  //   "/tbsp":{
  //     // target:'http://10.20.47.206:7150',//开发环境
  //     target:'http://10.20.29.157:8150',//测试环境
  //     changeOrigin: true,
  //     pathRewrite: {
  //       '^/tbsp': '/tbsp'
  //     }
  //   },
  // },
  // 部署配置
  see: {
    // 系统类型
    systemType: "web",
    //配置 SEE 平台发布物的包名称
    packageName: `bank-basicPlatform-${version}`,
    //配置see平台发布物的类型
    appType: `bank-basicPlatform`,
    // 配置 SEE 平台发布物的模版变量
    // variables: [
    //   //headTenantId
    //   {
    //     type: "input",
    //     label: "租户号",
    //     tooltip: "",
    //     name: "headTenantId",
    //     default: "000",
    //   },
    //   {
    //     type: "switch",
    //     label: "是否启用报文加密",
    //     tooltip: "报文加解密开关",
    //     name: "pubKey",
    //     options: "true:是;false:否",
    //     default: "false",
    //   }
    // ],
  },
  configureWebpack: (config) => {
    // 变量名称混淆
    config.optimization.minimizer[0].options.terserOptions.mangle = true
    // 多进程提高打包速度
    config.optimization.minimizer[0].options.terserOptions.parallel = true
    // 去掉console和debugger
    config.optimization.minimizer[0].options.terserOptions.compress = {
      drop_console: true, // 移除所有的console.log语句
      drop_debugger: true,
      pure_funcs: ["console.log"]
    }
  },
};
