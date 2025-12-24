/**
 * time: 2025-06-05
 * author: XJ
 * description: 数据管理右侧Table数据源
 */
import { useState, useCallback, SetStateAction } from 'react';

const initData: {
  tableSource: any[];
  actionData: { [key: string]: string };
} = {
  tableSource: [],
  actionData: {},
};
export default function dialogStatus() {
  const [paramSource, setParamSource] = useState(initData);
  return {
    paramSource,
    setParamSource,
  };
}
