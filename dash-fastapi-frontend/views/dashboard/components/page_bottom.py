import feffery_antd_charts as fact
import feffery_antd_components as fac
import feffery_utils_components as fuc
import feffery_markdown_components as fmc
from dash import html


def render_page_bottom():
    return fac.AntdTabs(
        items=[
            {
                'key': 'readme',
                'label': '系统介绍',
                'children': html.Div(
                    [

                        fmc.FefferyMarkdown(
                            imageForceAlignCenter=True,
                            renderHtml=True,
                            style={
                                "color": "rgba(255,255,255,0.85)",
                                "background": "#121212"
                            },
                            h2Style={
                                'color': 'white'
                            },
                            markdownStr=r'''
## 🚀主要功能
  系统主要负责载荷的异常检测、故障诊断和性能评估。
  1. 对载荷异常检测和故障处置规则电子化采集和结构化表达并建立故障知识库；
  2. 对载荷静态固定规则、指令关联动态规则等在线判读；
  3. 对规则内单变量单点异常、聚集异常检测和报警；
  4. 对具有明确判据的故障模式进行实时判读，并协助进行故障的定位，生成相应的处置对策；
  5. 对寿命敏感的器件进行可用性评估和预测。
                     '''
                        ),
                    ]

                )
            },
            {
                'key': 'gxc',
                'label': '光学舱',
                'children': html.Div(
                    [

                        fmc.FefferyMarkdown(
                            imageForceAlignCenter=True,
                            renderHtml=True,
                            style={
                                "color": "rgba(255,255,255,0.85)",
                                "background": "#121212"
                            },
                            h2Style={
                              'color':'white'
                            },
                            markdownStr=r'''
## 🚀任务目标

在CSST任务中，**有效载荷运控管理系统**主要任务目标如下：

1. 具备天文观测任务规划与运行控制能力，统一规划光学设施巡天观测任务和其他后端模块的工作，合理分配能源、存储、上下行、观测时间等资源，准确安排、控制引导星和姿态指向，最大化资源使用效率与观测效率。

2. 具备前端数据接收、数据处理、载荷状态监视、天文图像快视、成像合焦/像质/指向快速评判、载荷异常检测和故障定位处置能力，实施高效、科学、合理的运行管理，确保观测成功率和观测效率最大化。  


## 🚀巡天光学设施任务总体情况

![image](/assets/imgs/CSST-1.png)                

## 🚀观测模式

|序号|名称|代号|说明|
|--|--|--|--|
|1|巡天观测模式|OM1|光学设施执行巡天观测的工作模式|
|2|太赫兹凝视探测模式|OM2-1|光学设施执行太赫兹凝视探测的工作模式|
|3|太赫兹OTF观测模式|OM2-2|光学设施执行太赫兹OTF观测的工作模式|
|4|MCI观测模式|OM3|光学设施执行多通道成像观测的工作模式|
|5|IFS观测模式|OM4|光学设施执行展源目标光谱测量的工作模式|
|6|星冕仪观测模式|OM5|光学设施执行系外行星高对比度成像观测的工作模式|
|7|焦面4联合观测模式|OM6-1|MCI、IFS和星冕仪同时执行观测任务的工作模式|
|8|MCI+IFS联合观测模式|OM6-2|MCI、IFS模块同时执行观测任务的工作模式|
|9|MCI+星冕仪联合观测模式|OM6-3|MCI、星冕仪同时执行观测任务的工作模式|
|10|星冕仪+IFS联合观测模式|OM6-4|IFS、星冕仪同时执行观测任务的工作模式|

## 🚀鉴定件联试

1. 联试现场主要针对 MCI, IFS, CPIC三个模块


                     '''
                        ),
                    ]

                )
            },
        ]
    )
