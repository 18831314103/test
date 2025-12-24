import type { ProLayoutProps } from '@ant-design/pro-components';

/**
 * @name
 */
const Settings: ProLayoutProps & {
  pwa?: boolean;
  logo?: string | null;
} = {
  navTheme: 'realDark',
  // 拂晓蓝
  colorPrimary: '#1890ff',
  layout: 'mix',
  contentWidth: 'Fluid',
  fixedHeader: false,
  fixSiderbar: true,
  colorWeak: false,
  title: ' ',
  pwa: true,
  logo: "./images/logo.svg",
  iconfontUrl: '',
  footerRender: false,
  contentStyle: {
    background: `url('/images/D2LWSqNny4sAAAAAAAAAAAAAFl94AQBr.webp'),url('/images/C2TWRpJpiC0AAAAAAAAAAAAAFl94AQBr.webp'),url('/images/F6vSTbj8KpYAAAAAAAAAAAAAFl94AQBr.webp'),linear-gradient(-45deg, transparent 10px, rgb(90 98 112 / 50%) 0px)`,
    backgroundSize:`auto 303px, auto 303px, 331px auto, 100% 100%`,
    backgroundPosition:`left 85px bottom 100px, bottom -68px right -45px, bottom 0px left 0px,left top`,
    backgroundRepeat:"no-repeat",
    padding: 5,
  },

  token: {
    // 参见ts声明，demo 见文档，通过token 修改样式
    //https://procomponents.ant.design/components/layout#%E9%80%9A%E8%BF%87-token-%E4%BF%AE%E6%94%B9%E6%A0%B7%E5%BC%8F
    bgLayout: "#000",
    sider: {
      colorMenuBackground: "#1e2229",
    },
    header: {
      colorBgHeader: "linear-gradient(-45deg,transparent 10px,#17253c 0)"
    },
    pageContainer: {
      marginBlockPageContainerContent: 10,
      marginInlinePageContainerContent: 10,
      paddingInlinePageContainerContent: 10,
      paddingBlockPageContainerContent: 10,
    }
  },
};

export default Settings;
