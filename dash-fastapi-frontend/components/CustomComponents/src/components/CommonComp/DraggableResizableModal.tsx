/**
 * time: 2025-04-02
 * author: XJ
 * description: 弹出框高阶组件
 */
import React, { useRef, useEffect, useState } from 'react';
import { Modal } from 'antd';
import type { ModalProps } from 'antd';
import './DraggableModal.css';

interface DraggableModalProps extends ModalProps {
    children?: React.ReactNode;
    minWidth?: number;
    minHeight?: number;
}

const DraggableModal: React.FC<DraggableModalProps> = ({
    children,
    title,
    minWidth = 400,
    minHeight = 300,
    width = 520,
    height = 400,
    ...props
}) => {
    const modalRef = useRef<HTMLDivElement>(null);
    const headerRef = useRef<HTMLDivElement>(null);
    const resizeHandleRef = useRef<HTMLDivElement>(null);

    const [modalSize, setModalSize] = useState({
        width: typeof width === 'number' ? width : 520,
        height: typeof height === 'number' ? height : 520,
    });
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const param_ref = useRef<any>({
        isDragging: false,
        isResizing: false,
        startX: 0,
        startY: 0,
        startPosX: 0,
        startPosY: 0,
        startWidth: 0,
        startHeight: 0
    })

    useEffect(() => {
        const header = headerRef.current;
        const resizeHandle = resizeHandleRef.current;
        const modal = modalRef.current;

        if (!header || !resizeHandle || !modal || !props.open) return;
        const handleHeaderMouseDown = (e: MouseEvent) => {
            if (e.button !== 0 || (e.target as HTMLElement).closest('.ant-modal-close')) return;

            param_ref.current.isDragging = true;
            param_ref.current.startX = e.clientX;
            param_ref.current.startY = e.clientY;
            param_ref.current.startPosX = position.x;
            param_ref.current.startPosY = position.y;

            document.body.style.userSelect = 'none';
            document.body.style.cursor = 'grabbing';
        };

        const handleResizeMouseDown = (e: MouseEvent) => {
            if (e.button !== 0) return;

            param_ref.current.isResizing = true;
            param_ref.current.startX = e.clientX;
            param_ref.current.startY = e.clientY;
            param_ref.current.startWidth = modalSize.width;
            param_ref.current.startHeight = modalSize.height;

            document.body.style.userSelect = 'none';
            document.body.style.cursor = 'nwse-resize';
            e.stopPropagation();
        };

        const handleMouseMove = (e: MouseEvent) => {
            if (param_ref.current.isDragging) {
                const dx = e.clientX - param_ref.current.startX;
                const dy = e.clientY - param_ref.current.startY;
                console.log(dx, dy)
                setPosition({
                    x: param_ref.current.startPosX + dx,
                    y: param_ref.current.startPosY + dy
                });
            }

            if (param_ref.current.isResizing) {
                const dx = e.clientX - param_ref.current.startX;
                const dy = e.clientY - param_ref.current.startY;
                setModalSize({
                    width: Math.max(minWidth, param_ref.current.startWidth + dx),
                    height: Math.max(minHeight, param_ref.current.startHeight + dy)
                });
            }
        };

        const handleMouseUp = () => {
            param_ref.current.isDragging = false;
            param_ref.current.isResizing = false;
            document.body.style.userSelect = '';
            document.body.style.cursor = '';
        };

        header.addEventListener('mousedown', handleHeaderMouseDown);
        resizeHandle.addEventListener('mousedown', handleResizeMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        return () => {
            header.removeEventListener('mousedown', handleHeaderMouseDown);
            resizeHandle.removeEventListener('mousedown', handleResizeMouseDown);
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
            document.body.style.userSelect = '';
            document.body.style.cursor = '';
        };
    }, [position, modalSize, minWidth, minHeight, props.open]);

    return (
        <Modal
            {...props}
            title={null}
            width={modalSize.width}
            mask={false}
            closable={false}
            maskClosable={false}
            transitionName=""
            maskTransitionName=""
            styles={{
                body: {
                    height: `${modalSize.height - 100}px`,
                    overflow: 'auto',
                },
            }}
            modalRender={(modal) => (
                <div
                    ref={modalRef}
                    className="draggable-modal"
                    style={{
                        position: 'fixed',
                        top: '50%',
                        left: '50%',
                        transform: `translate(calc(-50% + ${position.x}px), calc(-50% + ${position.y}px)`,
                        width: `${modalSize.width}px`,
                        height: `${modalSize.height}px`,
                        zIndex: 9000,
                    }}
                >
                    <div ref={headerRef} className="draggable-modal-header">
                        {title || '模态框标题'}
                        <span onClick={(e) => props.onCancel ? props.onCancel(e as any) : void (0)} style={{ float: "right", cursor: "pointer" }}>
                            <svg fillRule="evenodd" viewBox="64 64 896 896" focusable="false" data-icon="close" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M799.86 166.31c.02 0 .04.02.08.06l57.69 57.7c.04.03.05.05.06.08a.12.12 0 010 .06c0 .03-.02.05-.06.09L569.93 512l287.7 287.7c.04.04.05.06.06.09a.12.12 0 010 .07c0 .02-.02.04-.06.08l-57.7 57.69c-.03.04-.05.05-.07.06a.12.12 0 01-.07 0c-.03 0-.05-.02-.09-.06L512 569.93l-287.7 287.7c-.04.04-.06.05-.09.06a.12.12 0 01-.07 0c-.02 0-.04-.02-.08-.06l-57.69-57.7c-.04-.03-.05-.05-.06-.07a.12.12 0 010-.07c0-.03.02-.05.06-.09L454.07 512l-287.7-287.7c-.04-.04-.05-.06-.06-.09a.12.12 0 010-.07c0-.02.02-.04.06-.08l57.7-57.69c.03-.04.05-.05.07-.06a.12.12 0 01.07 0c.03 0 .05.02.09.06L512 454.07l287.7-287.7c.04-.04.06-.05.09-.06a.12.12 0 01.07 0z"></path></svg>
                        </span>
                    </div>
                    <div className="draggable-modal-content">
                        {modal}
                    </div>
                    <div
                        ref={resizeHandleRef}
                        className="draggable-modal-resize-handle"
                    />
                </div>
            )}
        >
            {children}
        </Modal>
    );
};

export default DraggableModal;