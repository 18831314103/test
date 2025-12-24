/**
 * time: 2025-06-05
 * author: XJ
 * description: 数据管理左侧
 */
import React, { useEffect, useState } from 'react';
import { Tree } from 'antd';
import type { GetProps, TreeDataNode } from 'antd';
import Search from 'antd/es/input/Search';
import { getParamByActionId, getXmlTree } from '@/services/apis/dataManager';
import { useModel } from '@umijs/max';

type DirectoryTreeProps = GetProps<typeof Tree.DirectoryTree>;

const { DirectoryTree } = Tree;

const LeftTree: React.FC = () => {
  const [treeData, setTreeData] = useState([]);
  const { paramSource, setParamSource } = useModel('DataManager.paramSource');

  const onSelect: DirectoryTreeProps['onSelect'] = (keys, info) => {
    const { node } = info;
    if (!node.isLeaf) return;
    getParamByActionId({ actionId: (node as any).id }).then((res) => {
      const { code, data } = res;
      if (code == 200) {
        setParamSource({ tableSource: data,actionData: (node as any).nodeInfo});
      }
    });
  };

  const onExpand: DirectoryTreeProps['onExpand'] = (keys, info) => {
    console.log('Trigger Expand', keys, info);
  };
  useEffect(() => {
    getXmlTree({}).then((res: any) => {
      setTreeData(res);
    });
  }, []);
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    // const newExpandedKeys = dataList
    //   .map((item) => {
    //     if (item.title.indexOf(value) > -1) {
    //       return getParentKey(item.key, defaultData);
    //     }
    //     return null;
    //   })
    //   .filter((item, i, self): item is React.Key => !!(item && self.indexOf(item) === i));
    // setExpandedKeys(newExpandedKeys);
    // setSearchValue(value);
    // setAutoExpandParent(true);
  };
  return (
    <>
      {/* <Search style={{ marginBottom: 8 }} placeholder="请输入关键字" onChange={onChange} /> */}
      <DirectoryTree
        rootStyle={{
          height: 'calc(100% - 110px)',
        }}
        showLine
        multiple
        fieldNames={{ title: 'name', key: 'id' }}
        //   draggable
        defaultExpandAll
        onSelect={onSelect}
        onExpand={onExpand}
        treeData={treeData}
      />
    </>
  );
};

export default LeftTree;
