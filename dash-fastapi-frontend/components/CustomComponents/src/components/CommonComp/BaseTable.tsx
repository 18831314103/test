/**
 * time: 2025-04-02
 * author: XJ
 * description: 表格高阶组件
 */
import React, { useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { HolderOutlined } from '@ant-design/icons';
import type { DragEndEvent } from '@dnd-kit/core';
import { DndContext } from '@dnd-kit/core';
import type { SyntheticListenerMap } from '@dnd-kit/core/dist/hooks/utilities';
import { restrictToVerticalAxis } from '@dnd-kit/modifiers';
import { Resizable } from 'react-resizable';
import {
    arrayMove,
    SortableContext,
    useSortable,
    verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Button, Space, Table } from 'antd';
import type { TableColumnsType, TableProps } from 'antd';
import { useModel } from '@umijs/max';
import 'react-resizable/css/styles.css';

interface RowContextProps {
    setActivatorNodeRef?: (element: HTMLElement | null) => void;
    listeners?: SyntheticListenerMap;
}

const RowContext = React.createContext<RowContextProps>({});

const DragHandle: React.FC = () => {
    const { setActivatorNodeRef, listeners } = useContext(RowContext);
    return (
        <Button
            type="text"
            size="small"
            icon={<HolderOutlined />}
            style={{ cursor: 'move' }}
            ref={setActivatorNodeRef}
            {...listeners}
        />
    );
};

interface RowProps extends React.HTMLAttributes<HTMLTableRowElement> {
    'data-row-key': string;
}

const Row: React.FC<RowProps> = (props) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        setActivatorNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id: props['data-row-key'] });

    const style: React.CSSProperties = {
        ...props.style,
        transform: CSS.Translate.toString(transform),
        transition,
        ...(isDragging ? { position: 'relative',  } : {}),
    };

    const contextValue = useMemo<RowContextProps>(
        () => ({ setActivatorNodeRef, listeners }),
        [setActivatorNodeRef, listeners],
    );

    return (
        <RowContext.Provider value={contextValue}>
            <tr {...props} ref={setNodeRef} style={style} {...attributes} />
        </RowContext.Provider>
    );
};
const ResizableHeaderCell = React.memo(({ width, onResize, onResizeStart, onResizeStop, index, ...restProps }: any) => {
    return (
        <Resizable
            width={width || 100}
            height={0}
            handle={
                <span
                    className="react-resizable-handle"
                    onClick={(e) => e.stopPropagation()}
                />
            }
            onResize={(e: any, data: any) => onResize(e, data, index)}
            onResizeStart={(e: any, data: any) => onResizeStart(e, data, index)}
            onResizeStop={(e: any, data: any) => {
                onResizeStop(e, data, index);
            }}
            draggableOpts={{ enableUserSelectHack: false }}
        >
            <th {...restProps} />
        </Resizable>
    );
});

interface BaseTable extends TableProps {
    tableWidth: number;
    columnsA: any[];
    table_state:any;
    table_state_fun:any;
    twoHeight:number[]
}
const BaseTable: React.FC<BaseTable> = (props) => {
    
    const [tableWidth, setTableWidth] = useState<number>(props.tableWidth);
    const [columns, setColumns] = useState(props.columnsA);
    const tableRef = useRef<any>(null);
    const startPosition = useRef<any>(null);
    // 动态更新参考线位置（实时跟随鼠标）
    const updateGuideLine = useCallback((clientX: any) => {
        const guideLine = document.getElementById("resize-guide-line");
        if (!guideLine || !tableRef.current) return;
        const tableRect = tableRef.current.getBoundingClientRect();
        guideLine.style.left = `${clientX - tableRect.left}px`;
    }, []);
    useEffect(() => {
        if (!tableRef.current.offsetWidth || !tableRef.current) return;
        // 宽度监听
        const resizeObserver = new ResizeObserver(() => {
            if (tableRef.current?.offsetWidth) {
                console.log(tableRef.current.offsetWidth)
                setTableWidth(tableRef.current.offsetWidth);
            }
        });
        resizeObserver.observe(tableRef.current);

        return () => resizeObserver.disconnect();
    }, [tableRef.current])
    useEffect(() => {
        // 参考线元素
        const guideLine = document.createElement("div");
        guideLine.id = "resize-guide-line";
        guideLine.style.cssText = `
          position: absolute;
          top: 0;
          bottom: 0;
          width: 1px;
          background: #1890ff;
          display: none;
          z-index: 99999;
          pointer-events: none;
        `;
        tableRef.current?.appendChild(guideLine);
        // 鼠标移动监听
        const handleMouseMove = (e: any) => {
            const guideLine = document.getElementById("resize-guide-line");
            if (guideLine?.style.display === "block") {
                updateGuideLine(e.clientX);
            }
        };
        document.addEventListener("mousemove", handleMouseMove);


        return () => {

            document.removeEventListener("mousemove", handleMouseMove);
            guideLine.remove();
        };
    }, [updateGuideLine, tableRef.current]);
    const handleResize = useCallback((e: any, { size }: any, index: any) => {
        updateGuideLine(e.clientX);
    }, [updateGuideLine]);

    const handleResizeStart = useCallback((e: any, data: any, index: any) => {
        const guideLine = document.getElementById("resize-guide-line");
        if (guideLine) {
            guideLine.style.display = "block";
            updateGuideLine(e.clientX);
            startPosition.current = e.clientX;
        }
    }, [updateGuideLine]);
    const handleResizeStop = useCallback((e: any, { size }: any, index: any) => {
        const width = e.clientX - startPosition.current;
        setColumns(prevColumns => {
            const newColumns = [...prevColumns];
            const newPercent = width + newColumns[index].width;
            newColumns[index] = {
                ...newColumns[index],
                width: newPercent
            };
            return newColumns;
        });

        const guideLine = document.getElementById("resize-guide-line");
        if (guideLine) guideLine.style.display = "none";
    }, [tableWidth]);

    const onDragEnd = ({ active, over }: DragEndEvent) => {
        if (active.id !== over?.id) {
            props.table_state_fun((item: { dataSource: any[]; }) => {

                const activeIndex = item.dataSource.findIndex((record) => record.key === active?.id);
                const overIndex = item.dataSource.findIndex((record) => record.key === over?.id);
                return {
                    ...item,
                    dataSource: arrayMove(item.dataSource, activeIndex, overIndex)

                }
            })
        }
    };

    return (
        <div ref={tableRef} style={{ backgroundColor: "#0c0c0c", padding: 10, position: "relative", width: "100%", minWidth: "800px" }}>
            <DndContext modifiers={[restrictToVerticalAxis]} onDragEnd={onDragEnd}>
                <SortableContext items={props.table_state.dataSource.map((i: { key: any; }) => i.key)} strategy={verticalListSortingStrategy}>
                    <Table
                        style={{ height: props.table_state.isCollapsible ? window.innerHeight - props.twoHeight[0] : window.innerHeight -  props.twoHeight[1] }}
                        rowKey="key"
                        components={{
                            body: { row: Row },
                            header: {
                                cell: (props: any) => (
                                    <ResizableHeaderCell
                                        {...props}
                                        onResize={handleResize}
                                        onResizeStart={handleResizeStart}
                                        onResizeStop={handleResizeStop}
                                    />
                                ),
                            },
                        }}
                        columns={columns as any}
                        dataSource={props.table_state.dataSource}
                        size='small'
                        scroll={{ y: props.table_state.isCollapsible ? window.innerHeight -  props.twoHeight[0] - 95 : window.innerHeight -  props.twoHeight[1] - 85, x: tableWidth - 35 }}
                        {...props}
                    />
                </SortableContext>
            </DndContext>
        </div>
    );
};

export default BaseTable;