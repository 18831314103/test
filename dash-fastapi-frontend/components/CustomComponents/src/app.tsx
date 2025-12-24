import { AvatarDropdown, AvatarName, Footer, } from '@/components';
import { currentUser as queryCurrentUser } from '@/services/apis/api';
import { LinkOutlined } from '@ant-design/icons';
import type { Settings as LayoutSettings } from '@ant-design/pro-components';
import { SettingDrawer } from '@ant-design/pro-components';
import type { RunTimeLayoutConfig } from '@umijs/max';
import { history, Link } from '@umijs/max';
import React from 'react';
import defaultSettings from '../config/defaultSettings';
import { errorConfig } from './requestErrorConfig';
import { ConfigProvider, theme } from 'antd';
import { ThemeProvider } from 'antd-style';
import { LOGO } from './components/RightContent';

const isDev = process.env.NODE_ENV === 'development';
const loginPath = '/experiment_application';

/**
 * @see  https://umijs.org/zh-CN/plugins/plugin-initial-state
 * */
export async function getInitialState(): Promise<{
  settings?: Partial<LayoutSettings>;
  currentUser?: API.CurrentUser;
  loading?: boolean;
  fetchUserInfo?: () => Promise<API.CurrentUser | undefined>;
}> {
  const fetchUserInfo = async () => {
    try {
      const msg = await queryCurrentUser({
        skipErrorHandler: true,
      });
      return msg.data;
    } catch (error) {
      // history.push(loginPath);
    }
    return undefined;
  };
  // 如果不是登录页面，执行
  const { location } = history;
  console.log(defaultSettings)
  if (location.pathname !== loginPath) {
    const currentUser = await fetchUserInfo();
    return {
      fetchUserInfo,
      currentUser,
      settings: defaultSettings as Partial<LayoutSettings>,
    };
  }
  return {
    fetchUserInfo,
    settings: defaultSettings as Partial<LayoutSettings>,
  };
}

// ProLayout 支持的api https://procomponents.ant.design/components/layout
export const layout: RunTimeLayoutConfig = ({ initialState, setInitialState }) => {
  return {
    // actionsRender: () => [<Question key="doc" />, <SelectLang key="SelectLang" />],
    // actionsRender:() => [<LOGO />],
    avatarProps: {
      // src: initialState?.currentUser?.avatar,
      title: <AvatarName />,
      render: (_, avatarChildren) => {
        return <AvatarDropdown>{avatarChildren}</AvatarDropdown>;
      },
    },
    // waterMarkProps: {
    //   content: initialState?.currentUser?.name,
    // },
    footerRender: () => <Footer />,
    onPageChange: () => {
      const { location } = history;
      // 如果没有登录，重定向到 login
      // if (!initialState?.currentUser && location.pathname !== loginPath) {
      //   history.push(loginPath);
      // }
    },
    // bgLayoutImgList: [
    //   {
    //     src: '/images/D2LWSqNny4sAAAAAAAAAAAAAFl94AQBr.webp',
    //     left: 85,
    //     bottom: 100,
    //     height: '303px',
    //   },
    //   {
    //     src: '/images/C2TWRpJpiC0AAAAAAAAAAAAAFl94AQBr.webp',
    //     bottom: -68,
    //     right: -45,
    //     height: '303px',
    //   },
    //   {
    //     src: '/images/F6vSTbj8KpYAAAAAAAAAAAAAFl94AQBr.webp',
    //     bottom: 0,
    //     left: 0,
    //     width: '331px',
    //   },
    // ],
    menuHeaderRender: undefined,
    // 自定义 403 页面
    // unAccessible: <div>unAccessible</div>,
    // 增加一个 loading 的状态
    childrenRender: (children) => {
      // if (initialState?.loading) return <PageLoading />;
      return (
        <>
          {children}
          {/* {isDev && (
            <SettingDrawer
              disableUrlParams
              enableDarkTheme
              settings={initialState?.settings}
              onSettingChange={(settings) => {
                setInitialState((preInitialState) => ({
                  ...preInitialState,
                  settings,
                }));
              }}
            />
          )} */}
        </>
      );
    },
    ...initialState?.settings,
  };
};
export function rootContainer(container: React.ReactNode) {
  return (
    <ConfigProvider
      theme={{
        // 修改全局字号配置
        token: {
          fontSize: 16, // 基础字号
          fontSizeSM: 14, // 小号文本
          fontSizeLG: 18, // 大号文本
          fontSizeHeading1: 20, // h1标题
          fontSizeHeading2: 18, // h2标题
          fontSizeHeading3: 16, // h3标题
        },
        // 组件级字号覆盖
        components: {
          Modal:{
            borderRadius:2
          },
          Form:{
            itemMarginBottom:10
          },
          DatePicker: {
            colorBorder: "#ffffffd9",
            borderRadius: 2
          },
          Select: {
            colorBorder: "#ffffffd9",
            borderRadius: 2
          },
          Input: {
            colorBorder: "#ffffffd9",
            borderRadius: 2
          },
          Button: {
            fontSize: 16,
            fontSizeLG: 18,
            fontSizeSM: 14,
            borderRadius: 2,
            colorBorder: "#fff"
          },
          Tree:{
            borderRadius: 2
          },
          Table: {
            fontSize: 16,
            headerSplitColor: "#000",
            headerBorderRadius: 0,
            headerColor: "rgb(204, 204, 204)",
            headerBg: "#373e45",
          },
          Menu: {
            fontSize: 20,
            itemHeight: 40
          },
        }
      }}
    >
      {container}
    </ConfigProvider>
  );
}
/**
 * @name request 配置，可以配置错误处理
 * 它基于 axios 和 ahooks 的 useRequest 提供了一套统一的网络请求和错误处理方案。
 * @doc https://umijs.org/docs/max/request#配置
 */
export const request = {
  ...errorConfig,
};
