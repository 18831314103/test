/**
 * time: 2025-03-26
 * author: XJ
 * description: 用于所有Page最外层,设置统一的字号,颜色,最外层布局
 */

import { PageContainer } from "@ant-design/pro-components"
import { ReactNode } from "react"

const PageContainerComp = ({ children }: { children: ReactNode }) => {
    return (
        <PageContainer
            title={false}
            style={{
                height:window.innerHeight - 66,
                overflowY:"auto"
            }}
        >
            {children}
        </PageContainer>)
}

export default PageContainerComp;
