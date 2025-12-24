// import { QuestionCircleOutlined } from '@ant-design/icons';
// import { SelectLang as UmiSelectLang } from '@umijs/max';
// import React from 'react';

import { Col, Row } from "antd";

// export type SiderTheme = 'light' | 'dark';

// export const SelectLang = () => {
//   return (
//     <UmiSelectLang
//       style={{
//         padding: 4,
//       }}
//     />
//   );
// };

// export const Question = () => {
//   return (
//     <div
//       style={{
//         display: 'flex',
//         height: 26,
//       }}
//       onClick={() => {
//         window.open('https://pro.ant.design/docs/getting-started');
//       }}
//     >
//       <QuestionCircleOutlined />
//     </div>
//   );
// };
export const LOGO = () => {
  return (
    <div
      style={{
        position: "absolute",
        left: 30,
        width:200,
      }}
    >
      <img style={{ height:22,position:"absolute",top:-14,left:30}} src="/images/logo.9664b644.png"></img>
      <span style={{
        fontSize: 12,
        fontFamily: "Microsoft YaHei",
        position:"absolute",
        top:-9,
        letterSpacing:"1px",
        transform: "scale(.7)",
        color:"#fff"
      }}>-有效载荷运行管理中心-</span>
    </div>
  );
};
