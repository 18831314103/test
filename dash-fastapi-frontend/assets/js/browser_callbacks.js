// 在独立js脚本中定义比较长的回调函数
// let myDiagram = null;
let globalEventSource = null;
window.dash_clientside = Object.assign({}, window.dash_clientside, {
        clientside: {
            updateResponse: (data, reasoningContent) => {

                if (globalEventSource) {
                    globalEventSource.close();
                }
                globalEventSource = new EventSource(`http://localhost:9099/streaming?question=${question}`);
                // 监听消息事件（默认事件）
                globalEventSource.onmessage = function(event) {
                    if (event.data) {
                        const data = JSON.parse(event.data);
                        if (data.isFinished) {
                            window.dash_clientside.set_props(
                                'submit', { 'loading': false }
                            )
                            globalEventSource.close();
                        }
                        dash_clientside.set_props("answer-chat", {"data":(reasoningContent || '') + (data.reasoning_content || '').replaceAll('<换行>', '\n')})
                    }
                };
                globalEventSource.onerror = function(error) {
                    console.error('EventSource 错误:', error);
                    if (globalEventSource.readyState === EventSource.CLOSED) {
                        console.log('连接已关闭');
                    }
                };
            },
            render_chart: function () {
                // 根据id初始化绑定图表
                var myChart = echarts.init(document.getElementById('ABN-real-module-chart'));

                const today = new Date();
                const dates = [];
                for (let i = 9; i >= 0; i--) {
                    const date = new Date(today);
                    date.setDate(today.getDate() - i);
                    dates.push(`${date.getMonth() + 1}-${date.getDate().toString().padStart(2, '0')}`);
                }

                const option = {
                    title: {
                        text: '近10天故障报警统计图',
                        left: 'center',
                        top: '10px'
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        data: dates
                    }, yAxis: {
                        type: 'value'
                    },
                    series: [

                        {

                            name: '一般告警',
                            type: 'bar',
                            stack: 'Ad',
                            emphasis: {
                                focus: 'series'
                            },
                            data: [20, 24, 15, 12, 2, 10, 15, 11, 23, 30, 34]
                        },
                        {
                            name: '严重告警',
                            type: 'bar',
                            stack: 'Ad',
                            emphasis: {
                                focus: 'series'
                            },
                            data: [5, 4, 3, 5, 2, 1, 0, 5, 6, 10, 0]
                        },

                    ]
                };
                // 渲染
                myChart.setOption(option);

            },
            render_goChart: (data, dataDesc) => {
                // if(!dataDesc || Object.keys(dataDesc).length == 0) return;
                if(!dataDesc || Object.keys(dataDesc).length == 0) return;
                let allDesc = dataDesc
                console.log(data, allDesc)
                // let allDesc = JSON.parse(dataDesc.faultcriteriondesc)
                console.log("2222",data, allDesc)
//                let fault_name;
//                if (data == null) {
//                    fault_name = '第一条的ABNName，还没传';
//                } else {
//                    fault_name = data['ABNName'];
//                }
                if (this.myDiagram) {
                    this.myDiagram.div = null; // 重新渲染时需清空div,上面的注释掉了 gaosong 2025.1.18
                }

                // if(myDiagram != null) myDiagram.clear();
                myDiagram = new go.Diagram('ABN-real-module-gojs', {
                    validCycle: go.CycleMode.NotDirected, // don't allow loops
                    // For this sample, automatically show the state of the diagram's model on the page
//                      ModelChanged: (e) => {
//                        if (e.isTransactionFinished) showModel();
//                      },
                    'undoManager.isEnabled': true
                });

                myDiagram.layout = new go.TreeLayout({
                    // angle: 90,
                    layerSpacing: 30,
                    nodeSpacing: 20
                });

                const UnselectedBrush = 'transparent'; // item appearance, if not "selected"
                const SelectedBrush = 'dodgerblue'; // item appearance, if "selected"

                function isFieldSelected(item) {
                    return item.background !== UnselectedBrush;
                }

                function setFieldSelected(item, sel) {
                    if (sel) {
                        item.background = SelectedBrush;
                    } else {
                        item.background = UnselectedBrush;
                    }
                }

                function onFieldClick(e, item) {
                    var oldskips = item.diagram.skipsUndoManager;
                    item.diagram.skipsUndoManager = true;
                    if (e.control || e.meta) {
                        setFieldSelected(item, !isFieldSelected(item));
                        item.part.isSelected = item.panel.elements.any(isFieldSelected);
                    } else if (e.shift) {
                        // alternative policy: select all fields between this item and some other one??
                        if (!isFieldSelected(item)) setFieldSelected(item, true);
                        item.part.isSelected = true;
                    } else {
                        if (!isFieldSelected(item)) {
                            // deselect all sibling items
                            item.panel.elements.each((it) => {
                                if (it !== item) setFieldSelected(it, false);
                            });
                            setFieldSelected(item, true);
                        }
                        item.part.isSelected = true;
                    }
                    item.diagram.skipsUndoManager = oldskips;
                }

                // This template is a Panel that is used to represent each item in a Panel.itemArray.
                // The Panel is data bound to the item object.
                var fieldTemplate = new go.Panel('TableRow', { // this Panel is a row in the containing Table
                    background: UnselectedBrush, // so this port's background can be picked by the mouse
                    fromSpot: go.Spot.LeftRightSides, // links only go from the right side to the left side
                    toSpot: go.Spot.LeftRightSides,
                    // allow drawing links from or to this port:
                    fromLinkable: true,
                    toLinkable: true,
                    // select items -- the background indicates "selected" when not UnselectedBrush
                    click: onFieldClick
                })
                    .bind('portId', 'name') // this Panel is a "port"
                    .add(
                        new go.Shape({
                            width: 12,
                            height: 12,
                            column: 0,
                            strokeWidth: 2,
                            margin: 4,
                            // but disallow drawing links from or to this shape:
                            fromLinkable: false,
                            toLinkable: false
                        })
                            .bind('figure')
                            .bind('fill', 'color'),
                        new go.TextBlock({
                            margin: new go.Margin(0, 2),
                            column: 1,
                            font: 'bold 13px sans-serif',
                            // and disallow drawing links from or to this text:
                            fromLinkable: false,
                            textAlign:"left",
                            toLinkable: false
                        })
                            .bind('text', 'name'),
                        new go.TextBlock({margin: new go.Margin(0, 2),alignment: go.Spot.Left, column: 2, font: '13px sans-serif'})
                            .bind('text', 'info')
                    );

                // This template represents a whole "record".
                myDiagram.nodeTemplate = new go.Node('Auto')
                    .bindTwoWay('location', 'loc', go.Point.parse, go.Point.stringify)
                    .add(
                        // this rectangular shape surrounds the content of the node
                        new go.Shape({fill: '#EEEEEE'}),
                        // the content consists of a header and a list of items
                        new go.Panel('Vertical')
                            .add(
                                // this is the header for the whole node
                                new go.Panel('Auto', {stretch: go.Stretch.Horizontal}) // as wide as the whole node
                                    .add(
                                        new go.Shape({fill: '#1570A6', stroke: null}),
                                        new go.TextBlock({
                                            alignment: go.Spot.Center,
                                            margin: 3,
                                            // stroke: 'white',
                                            textAlign: 'center',
                                            font: 'bold 12pt sans-serif'
                                        })
                                            .bind('text', 'key')
                                    ),
                                // this Panel holds a Panel for each item object in the itemArray;
                                // each item Panel is defined by the itemTemplate to be a TableRow in this Table
                                new go.Panel('Table', {
                                    name: 'TABLE',
                                    padding: 2,
                                    minSize: new go.Size(100, 10),
                                    defaultStretch: go.Stretch.Horizontal,
                                    itemTemplate: fieldTemplate
                                })
                                    .bind('itemArray', 'fields')
                            ) // end Vertical Panel
                    ); // end Node

                myDiagram.linkTemplate = new go.Link({
                    relinkableFrom: true,
                    relinkableTo: true,
                    toShortLength: 4
                }) // let user reconnect links
                    .add(
                        new go.Shape({strokeWidth: 1.5}),
                        new go.Shape({toArrow: 'Standard', stroke: null})
                    );
                const nodeDataArray = [];
                if(allDesc.instructions.length != 0){
                    const fields = [];
                    allDesc.instructions.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item;
                        let desc = "";
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                if(index1 != 0 && item1.nodeName != "#text"){
                                    desc += (item1.getAttribute('prefix') || "") + item1.textContent + (item1.getAttribute('stuffix') || "");
                                }
                            }
                        })
                        fields.push({name: `${++index}`, info: desc, color:"#F25022", figure: "Diamond"})
                    })
                    const singleJudge = {
                        key: `触发指令`,
                        fields,
//                       oc: '-200 10'
                    }
                    nodeDataArray.push(singleJudge)
                }
                if(allDesc.params.length != 0){
                    allDesc.params.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item.param;
                        const fields = [];
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                const desc = Array.from(item1.childNodes).reduce((pre, cur,index) => {
                                    if(index != 0 && cur.textContent != " "){
                                        return pre += (cur.attributes[0].value + cur.textContent + cur.attributes[1].value)
                                    }else{
                                        return pre
                                    }

                                } , "");
                                fields.push({name: `${index1}`, info: desc, color:"#F25022", figure: "Diamond"})
                            }

                        })
                        const singleJudge = {
                            key: `触发判据${index == 0 ? "" : index}`,
                            fields,
//                            loc: '0 0'
                        }
                        nodeDataArray.push(singleJudge)
                    })
                }
                if(allDesc.dataTerminate.instruction_Ter.length != 0){
                    const fields = [];
                    allDesc.dataTerminate.instruction_Ter.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item.instruction_Ter;
                        let desc = "";
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                if(index1 != 0 && item1.nodeName != "#text"){
                                    desc += (item1.getAttribute('prefix') || "") + item1.textContent + (item1.getAttribute('stuffix') || "");

                                }
                            }
                        })
                        fields.push({name: `${++index}`, info: desc, color:"#F25022", figure: "Diamond"})
                    })
                    const singleJudge = {
                        key: `指令终止条件`,
                        fields,
                        isColumn:true
//                       loc: '-200 10'
                    }
                    nodeDataArray.push(singleJudge)
                }
                if(allDesc.dataTerminate.params_Ter.length != 0){
                    allDesc.dataTerminate.params_Ter.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item.param;
                        const fields = [];
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                const desc = Array.from(item1.childNodes).reduce((pre, cur,index) => {
                                    if(index != 0 && cur.textContent != " "){
                                        return pre += (cur.attributes[0].value + cur.textContent + cur.attributes[1].value)
                                    }else{
                                        return pre
                                    }

                                } , "");
                                fields.push({name: `${index1}`, info: desc, color:"#F25022", figure: "Diamond"})
                            }

                        })
                        const singleJudge = {
                            key: `参数终止条件${index == 0 ? "" : index}`,
                            fields,
                            isColumn:true
//                            loc: '0 0'
                        }
                        nodeDataArray.push(singleJudge)
                    })
                }
                const linkDataArray = nodeDataArray.reduce((pre,cur,index) => {
                    if(nodeDataArray[index+1]){
                        if(cur.key.includes("终止条件")  && nodeDataArray[index+1].key.includes("终止条件")){
                            return pre;
                        }
                        if(nodeDataArray[index+1].isColumn && nodeDataArray[index+2]){
                            return [
                                ...pre,
                                {from: cur.key, to: nodeDataArray[index+1].key,},
                                {from: cur.key, to: nodeDataArray[index+2].key,},
                            ]
                        }
                        return [
                            ...pre,
                            {from: cur.key, to: nodeDataArray[index+1].key,},
                        ]
                    }else{
                        return pre
                    }

                },[])
//                if(allDesc.params.length != 0){
//
//                }
                myDiagram.model = new go.GraphLinksModel({
                    copiesArrays: true,
                    copiesArrayObjects: true,
//                      linkFromPortIdProperty: 'fromPort',
//                      linkToPortIdProperty: 'toPort',
                      nodeDataArray,
//                    nodeDataArray: [
//                        {
//                            key: '触发指令',
//                            fields: [
//                                {name: "", info: '00H 11H', color: '#F7B84B', figure: 'Ellipse'},
//                                {name: '指令2', info: '00H 11H', color: '#F25022', figure: 'Ellipse'},
//                                {name: '指令3', info: '00H 11H', color: '#00BCF2'}
//                            ],
//                            loc: '-200 10'
//                        },
//                        {
//                            key: '触发判据',
//                            fields: [
//                                {name: '判据1', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#FFB900', figure: 'Diamond'},
//                                {name: '判据2', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#F25022', figure: 'Rectangle'},
//                                {name: '判据3', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#7FBA00', figure: 'Diamond'},
//                                {name: '判据4', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#00BCF2', figure: 'Rectangle'},
//                            ],
//                            loc: '0 0'
//                        },
//                        {
//                            key: '终止条件',
//                            fields: [
//                                {name: '判据1', info: '30s内，TGXT1861 xxx电压大于0.2', color: '#FFB900', figure: 'Diamond'},
//
//                            ],
//                            loc: '350 30'
//                        }
//                    ],
                    linkDataArray,
//                    linkDataArray: [
//                        {from: '触发指令', to: '触发判据',},
//                        {from: '触发判据', to: '终止条件',},
//                    ]
                });

                // this is a bit inefficient, but should be OK for normal-sized graphs with reasonable numbers of items per node
                function findAllSelectedItems() {
                    var items = [];
                    for (var nit = myDiagram.nodes; nit.next();) {
                        var node = nit.value;
                        var table = node.findObject('TABLE');
                        if (table) {
                            for (var iit = table.elements; iit.next();) {
                                var itempanel = iit.value;
                                if (isFieldSelected(itempanel)) items.push(itempanel);
                            }
                        }
                    }
                    return items;
                }

                // Override the standard CommandHandler deleteSelection behavior.
                // If there are any selected items, delete them instead of deleting any selected nodes or links.
                myDiagram.commandHandler.canDeleteSelection = function () {
                    // method override must be function, not =>
                    // true if there are any selected deletable nodes or links,
                    // or if there are any selected items within nodes
                    return go.CommandHandler.prototype.canDeleteSelection.call(this) || findAllSelectedItems().length > 0;
                };

                myDiagram.commandHandler.deleteSelection = function () {
                    // method override must be function, not =>
                    var items = findAllSelectedItems();
                    if (items.length > 0) {
                        // if there are any selected items, delete them
                        myDiagram.startTransaction('delete items');
                        for (var i = 0; i < items.length; i++) {
                            var panel = items[i];
                            var nodedata = panel.part.data;
                            var itemarray = nodedata.fields;
                            var itemdata = panel.data;
                            var itemindex = itemarray.indexOf(itemdata);
                            myDiagram.model.removeArrayItem(itemarray, itemindex);
                        }
                        myDiagram.commitTransaction('delete items');
                    } else {
                        // otherwise just delete nodes and/or links, as usual
                        go.CommandHandler.prototype.deleteSelection.call(this);
                    }
                };

//                    showModel(); // show the diagram's initial model
//
//                    function showModel() {
//                      document.getElementById('mySavedModel').innerHTML = myDiagram.model.toJson();
//                      if (window.Prism) window.Prism.highlightAll();
//                    }
            },
            render_goChart_ABN_real_record:  (active_key, data) => {
                if (data.length == 0 || active_key !== '故障模式全局监控') return "点击上方查看判读流程";

                const data_dict_json = typeof data[0] === 'string' ? JSON.parse(data[0]) : data[0];
                const data_dict = data_dict_json.PROCESSOR_INFO.reduce((pre, cru, index) => {
                    if (index == 0) {
                        return [
                            ...pre,
                            {
                                key: 0,
                                gender: data_dict_json.STATUS_INFO["结果"] == "False" ? "no_satisfy" : "satisfy",
                                kanjiName: `结果：${data_dict_json.STATUS_INFO["结果"]}`,
                            },
                            {
                                key: 1,
                                parent: 0,
                                gender: "",
                                kanjiName: `状态：${data_dict_json.STATUS_INFO["状态"]}`,
                            },
                            {
                                key: 2,
                                parent: 1,
                                gender: cru.info["结果"] == "False" ? "no_heat" : "heat",
                                kanjiName: `状态：${cru.info["状态"]};\n结果：${cru.info["结果"]};\n判据类型：${cru.type}`,
                            },
                        ];
                    } else {
                        return [
                            ...pre,
                            {
                                key: Number(cru.index) + 1,
                                parent: 1,
                                gender: cru.info["结果"] == "False" ? "no_heat" : "heat",
                                kanjiName: `状态：${cru.info["状态"]};\n结果：${cru.info["结果"]};\n判据类型：${cru.type}`,
                            },
                        ];
                    }
                }, []);

                console.log(data_dict);
                if (this.myDiagram_record) {
                    this.myDiagram_record.div = null; // 重新渲染时需清空div
                }
                this.myDiagram_record = new go.Diagram('ABN_real_record_gojs', {
                    allowCopy: false,
                    layout: new go.TreeLayout({angle: 90, nodeSpacing: 3}),
                });

                this.myDiagram_record.animationManager.isEnabled = false;
                // var bluegrad = new go.Brush('Linear', {0: 'rgb(60, 204, 254)', 1: 'rgb(70, 172, 254)'});
                // var pinkgrad = new go.Brush('Linear', {0: 'rgb(255, 192, 203)', 1: 'rgb(255, 142, 203)'});
                // var greengrad = new go.Brush('Linear', {0: 'rgb(60, 204, 254)', 1: 'rgb(70, 172, 254)'});
                // var redgrad = new go.Brush('Linear', {0: 'rgb(255, 192, 203)', 1: 'rgb(255, 142, 203)'});
                const heatGrad = new go.Brush("Linear", { 0: "rgba(22,119,255,0.2)", 1: "rgba(22,119,255,0.35)" });      // heat
                const noHeatGrad = new go.Brush("Linear", { 0: "rgba(255,77,79,0.25)", 1: "rgba(255,77,79,0.35)" });      // no_heat
                const satisfyGrad = new go.Brush("Linear", { 0: "rgba(0,185,107,0.25)", 1: "rgba(0,185,107,0.35)" });     // satisfy
                const noSatisfyGrad = new go.Brush("Linear", { 0: "rgba(255,77,79,0.25)", 1: "rgba(255,77,79,0.35)" });

                this.myDiagram_record.add(
                  new go.Part("Table", {
                      layerName: "ViewportBackground",
                      alignment: new go.Spot(0, 0, 20, 20),
                      background: "rgba(0,0,0,0.15)",      // 添加柔和暗背景
                      padding: 6,
                      cornerRadius: 4
                  }).add(
                      new go.TextBlock("图例", { row: 0, stroke:"#ddd", font:"bold 13px sans-serif", margin:4 }),
                      new go.Panel("Horizontal", { row: 1, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:heatGrad, margin:4 }),
                               new go.TextBlock("已触发",{ stroke:"#ccc", font:"12px sans-serif"})),
                      new go.Panel("Horizontal", { row: 2, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:noHeatGrad, margin:4 }),
                               new go.TextBlock("未触发",{ stroke:"#ccc", font:"12px sans-serif"})),
                      new go.Panel("Horizontal", { row: 3, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:satisfyGrad, margin:4 }),
                               new go.TextBlock("已满足",{ stroke:"#ccc", font:"12px sans-serif"})),
                      new go.Panel("Horizontal", { row: 4, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:noSatisfyGrad, margin:4 }),
                               new go.TextBlock("未满足",{ stroke:"#ccc", font:"12px sans-serif"}))
                  )
                );




                function genderBrushConverter(gender) {
                    if (gender === 'heat') return heatGrad;
                    if (gender === 'no_heat') return noHeatGrad;
                    if (gender === 'satisfy') return satisfyGrad;
                    if (gender === 'no_satisfy') return noSatisfyGrad;
                    return "#2d2d2d"; // default block
                }

                this.myDiagram_record.nodeTemplate = new go.Node('Auto', {
                    deletable: false,
                    mouseEnter: (e,node)=>{
                        node.findObject("RECT").stroke = "#4096ff";
                        node.findObject("RECT").strokeWidth = 2;
                        node.findObject("RECT").shadowBlur = 10;
                        node.findObject("RECT").shadowColor = "rgba(64,150,255,0.4)";
                      },
                     mouseLeave: (e,node)=>{
                        node.findObject("RECT").stroke = "#555";
                        node.findObject("RECT").strokeWidth = 1;
                        node.findObject("RECT").shadowBlur = 0;
                     }

                })
                    .add(
                        new go.Shape('Rectangle', {
                            stroke: "#555",
                            strokeWidth: 1,
                            fill: "#2d2d2d",  // default if no gender
                            cornerRadius: 6,
                            stretch: go.Stretch.Fill,
                            alignment: go.Spot.Center
                        })
                            .bind('fill', 'gender', genderBrushConverter),
                        new go.Panel('Vertical')
                            .add(
                                new go.TextBlock({
                                    alignment: go.Spot.Center,
                                    padding: 10,
                                    margin: 8,
                                    font: "13px sans-serif",
                                    stroke: "#eee",
                                })
                                    .bind('text', 'kanjiName'),
                            )
                    );

                this.myDiagram_record.linkTemplate = new go.Link({
                    routing: go.Routing.Orthogonal,
                    corner: 6, selectable: false
                })
                    .add(
                        new go.Shape({ stroke: "#444", strokeWidth: 1.2 })
                    );
                this.myDiagram_record.background = "#1f1f1f";
                this.myDiagram_record.model = new go.TreeModel(data_dict);
            },
            render_modal_chart:(data) => {
                if(Object.keys(data).length == 0) return
                var myChart = echarts.init(document.getElementById("ABN-Check-YC-Modal-Chart-Container"));
                option = {
                      title: {
                            // 可以隐藏默认的标题
                            show: false
                      },
                      xAxis: {
                        type: 'time',
                      },
                      tooltip: {
                          trigger: 'axis',
//                          showContent: false
                      },
                      legend:{
                        type: 'scroll', // 启用滚动翻页功能
                        orient: 'horizontal',
                        pageButtonPosition: 'end',
                        pageFormatter: '{current}/{total}',
                        data:Object.keys(data)
                      },
                      yAxis: {
                        type: 'value'
                      },
                      legend:{

                      },
                      toolbox: {
                        show: true,
                        orient: 'vertical',
                        right: '5%',
                        top:'20%',
                        feature: {
                          mark: { show: true },
                          dataView: { show: true, readOnly: false },
                          magicType: { show: true, type: ['line', 'bar'] },
                          restore: { show: true },
                          saveAsImage: { show: true }
                        }
                      },
                      dataZoom: [
                            {
                                type: 'slider', // 使用滑动条进行缩放
                                xAxisIndex: 0, // 控制第一个x轴
                                start: 0, // 数据窗口范围的起始百分比
                                end: 100 // 数据窗口范围的结束百分比
                                // 其他可选配置...
                            },
                            {
                                type: 'inside', // 内置于坐标系中，可以通过鼠标滚轮进行缩放
                                xAxisIndex: 0, // 控制第一个x轴
                                // 其他可选配置...
                            }
                      ],
                      series: Object.keys(data).reduce((pre,cru) => {
                            return [
                                ...pre,
                                {
                                  name:cru,
                                  data: data[cru].sort((a,b) => a[0]-b[0]),
                                  type: 'line',
                                  smooth: true,
                                }
                            ]
                      },[])
                };
                myChart.setOption(option)
            }

        },
        clientsideKjz: {
            render_chart_kjz: function () {
                // 根据id初始化绑定图表
                var myChart = echarts.init(document.getElementById('ABN-real-module-chart-kjz'));

                const today = new Date();
                const dates = [];
                for (let i = 9; i >= 0; i--) {
                    const date = new Date(today);
                    date.setDate(today.getDate() - i);
                    dates.push(`${date.getMonth() + 1}-${date.getDate().toString().padStart(2, '0')}`);
                }

                const option = {
                    title: {
                        text: '近10天故障报警统计图',
                        left: 'center',
                        top: '10px'
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        data: dates
                    }, yAxis: {
                        type: 'value'
                    },
                    series: [

                        {

                            name: '一般告警',
                            type: 'bar',
                            stack: 'Ad',
                            emphasis: {
                                focus: 'series'
                            },
                            data: [20, 24, 15, 12, 2, 10, 15, 11, 23, 30, 34]
                        },
                        {
                            name: '严重告警',
                            type: 'bar',
                            stack: 'Ad',
                            emphasis: {
                                focus: 'series'
                            },
                            data: [5, 4, 3, 5, 2, 1, 0, 5, 6, 10, 0]
                        },

                    ]
                };
                // 渲染
                myChart.setOption(option);

            },
            render_goChart_kjz: (data, dataDesc) => {
                if(!dataDesc || Object.keys(dataDesc).length == 0) return;
                let allDesc = dataDesc
                console.log(data, allDesc)
//                let fault_name;
//                if (data == null) {
//                    fault_name = '第一条的ABNName，还没传';
//                } else {
//                    fault_name = data['ABNName'];
//                }
                if (this.myDiagram) {
                    this.myDiagram.div = null; // 重新渲染时需清空div,上面的注释掉了 gaosong 2025.1.18
                }

                // if(myDiagram != null) myDiagram.clear();
                myDiagram = new go.Diagram('ABN-real-module-gojs-kjz', {
                    validCycle: go.CycleMode.NotDirected, // don't allow loops
                    // For this sample, automatically show the state of the diagram's model on the page
//                      ModelChanged: (e) => {
//                        if (e.isTransactionFinished) showModel();
//                      },
                    'undoManager.isEnabled': true
                });

                myDiagram.layout = new go.TreeLayout({
                    // angle: 90,
                    layerSpacing: 30,
                    nodeSpacing: 20
                });

                const UnselectedBrush = 'transparent'; // item appearance, if not "selected"
                const SelectedBrush = 'dodgerblue'; // item appearance, if "selected"

                function isFieldSelected(item) {
                    return item.background !== UnselectedBrush;
                }

                function setFieldSelected(item, sel) {
                    if (sel) {
                        item.background = SelectedBrush;
                    } else {
                        item.background = UnselectedBrush;
                    }
                }

                function onFieldClick(e, item) {
                    var oldskips = item.diagram.skipsUndoManager;
                    item.diagram.skipsUndoManager = true;
                    if (e.control || e.meta) {
                        setFieldSelected(item, !isFieldSelected(item));
                        item.part.isSelected = item.panel.elements.any(isFieldSelected);
                    } else if (e.shift) {
                        // alternative policy: select all fields between this item and some other one??
                        if (!isFieldSelected(item)) setFieldSelected(item, true);
                        item.part.isSelected = true;
                    } else {
                        if (!isFieldSelected(item)) {
                            // deselect all sibling items
                            item.panel.elements.each((it) => {
                                if (it !== item) setFieldSelected(it, false);
                            });
                            setFieldSelected(item, true);
                        }
                        item.part.isSelected = true;
                    }
                    item.diagram.skipsUndoManager = oldskips;
                }

                // This template is a Panel that is used to represent each item in a Panel.itemArray.
                // The Panel is data bound to the item object.
                var fieldTemplate = new go.Panel('TableRow', { // this Panel is a row in the containing Table
                    background: UnselectedBrush, // so this port's background can be picked by the mouse
                    fromSpot: go.Spot.LeftRightSides, // links only go from the right side to the left side
                    toSpot: go.Spot.LeftRightSides,
                    // allow drawing links from or to this port:
                    fromLinkable: true,
                    toLinkable: true,
                    // select items -- the background indicates "selected" when not UnselectedBrush
                    click: onFieldClick
                })
                    .bind('portId', 'name') // this Panel is a "port"
                    .add(
                        new go.Shape({
                            width: 12,
                            height: 12,
                            column: 0,
                            strokeWidth: 2,
                            margin: 4,
                            // but disallow drawing links from or to this shape:
                            fromLinkable: false,
                            toLinkable: false
                        })
                            .bind('figure')
                            .bind('fill', 'color'),
                        new go.TextBlock({
                            margin: new go.Margin(0, 2),
                            column: 1,
                            font: 'bold 13px sans-serif',
                            // and disallow drawing links from or to this text:
                            fromLinkable: false,
                            textAlign:"left",
                            toLinkable: false
                        })
                            .bind('text', 'name'),
                        new go.TextBlock({margin: new go.Margin(0, 2),alignment: go.Spot.Left, column: 2, font: '13px sans-serif'})
                            .bind('text', 'info')
                    );

                // This template represents a whole "record".
                myDiagram.nodeTemplate = new go.Node('Auto')
                    .bindTwoWay('location', 'loc', go.Point.parse, go.Point.stringify)
                    .add(
                        // this rectangular shape surrounds the content of the node
                        new go.Shape({fill: '#EEEEEE'}),
                        // the content consists of a header and a list of items
                        new go.Panel('Vertical')
                            .add(
                                // this is the header for the whole node
                                new go.Panel('Auto', {stretch: go.Stretch.Horizontal}) // as wide as the whole node
                                    .add(
                                        new go.Shape({fill: '#1570A6', stroke: null}),
                                        new go.TextBlock({
                                            alignment: go.Spot.Center,
                                            margin: 3,
                                            // stroke: 'white',
                                            textAlign: 'center',
                                            font: 'bold 12pt sans-serif'
                                        })
                                            .bind('text', 'key')
                                    ),
                                // this Panel holds a Panel for each item object in the itemArray;
                                // each item Panel is defined by the itemTemplate to be a TableRow in this Table
                                new go.Panel('Table', {
                                    name: 'TABLE',
                                    padding: 2,
                                    minSize: new go.Size(100, 10),
                                    defaultStretch: go.Stretch.Horizontal,
                                    itemTemplate: fieldTemplate
                                })
                                    .bind('itemArray', 'fields')
                            ) // end Vertical Panel
                    ); // end Node

                myDiagram.linkTemplate = new go.Link({
                    relinkableFrom: true,
                    relinkableTo: true,
                    toShortLength: 4
                }) // let user reconnect links
                    .add(
                        new go.Shape({strokeWidth: 1.5}),
                        new go.Shape({toArrow: 'Standard', stroke: null})
                    );
                const nodeDataArray = [];
                if(allDesc.instructions.length != 0){
                    const fields = [];
                    allDesc.instructions.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item;
                        let desc = "";
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                if(index1 != 0 && item1.nodeName != "#text"){
                                    desc += (item1.getAttribute('prefix') || "") + item1.textContent + (item1.getAttribute('stuffix') || "");
                                }
                            }
                        })
                        fields.push({name: `${++index}`, info: desc, color:"#F25022", figure: "Diamond"})
                    })
                    const singleJudge = {
                        key: `触发指令`,
                        fields,
//                       oc: '-200 10'
                    }
                    nodeDataArray.push(singleJudge)
                }
                if(allDesc.params.length != 0){
                    allDesc.params.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item.param;
                        const fields = [];
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                const desc = Array.from(item1.childNodes).reduce((pre, cur,index) => {
                                    if(index != 0 && cur.textContent != " "){
                                        return pre += (cur.attributes[0].value + cur.textContent + cur.attributes[1].value)
                                    }else{
                                        return pre
                                    }

                                } , "");
                                fields.push({name: `${index1}`, info: desc, color:"#F25022", figure: "Diamond"})
                            }

                        })
                        const singleJudge = {
                            key: `触发判据${index == 0 ? "" : index}`,
                            fields,
//                            loc: '0 0'
                        }
                        nodeDataArray.push(singleJudge)
                    })
                }
                if(allDesc.dataTerminate.instruction_Ter.length != 0){
                    const fields = [];
                    allDesc.dataTerminate.instruction_Ter.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item.instruction_Ter;
                        let desc = "";
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                if(index1 != 0 && item1.nodeName != "#text"){
                                    desc += (item1.getAttribute('prefix') || "") + item1.textContent + (item1.getAttribute('stuffix') || "");

                                }
                            }
                        })
                        fields.push({name: `${++index}`, info: desc, color:"#F25022", figure: "Diamond"})
                    })
                    const singleJudge = {
                        key: `指令终止条件`,
                        fields,
                        isColumn:true
//                       loc: '-200 10'
                    }
                    nodeDataArray.push(singleJudge)
                }
                if(allDesc.dataTerminate.params_Ter.length != 0){
                    allDesc.dataTerminate.params_Ter.forEach((item,index) => {
                        const virele = document.createElement("div");
                        virele.innerHTML = item.param;
                        const fields = [];
                        virele.childNodes.forEach((item1,index1) => {
                            if(item1.className == "logic"){
                                fields.unshift({name: '逻辑关系', info: item1.textContent, color: '#FFB900', figure: 'Rectangle'})
                            }else{
                                const desc = Array.from(item1.childNodes).reduce((pre, cur,index) => {
                                    if(index != 0 && cur.textContent != " "){
                                        return pre += (cur.attributes[0].value + cur.textContent + cur.attributes[1].value)
                                    }else{
                                        return pre
                                    }

                                } , "");
                                fields.push({name: `${index1}`, info: desc, color:"#F25022", figure: "Diamond"})
                            }

                        })
                        const singleJudge = {
                            key: `参数终止条件${index == 0 ? "" : index}`,
                            fields,
                            isColumn:true
//                            loc: '0 0'
                        }
                        nodeDataArray.push(singleJudge)
                    })
                }
                const linkDataArray = nodeDataArray.reduce((pre,cur,index) => {
                    if(nodeDataArray[index+1]){
                        if(cur.key.includes("终止条件")  && nodeDataArray[index+1].key.includes("终止条件")){
                            return pre;
                        }
                        if(nodeDataArray[index+1].isColumn && nodeDataArray[index+2]){
                            return [
                                ...pre,
                                {from: cur.key, to: nodeDataArray[index+1].key,},
                                {from: cur.key, to: nodeDataArray[index+2].key,},
                            ]
                        }
                        return [
                            ...pre,
                            {from: cur.key, to: nodeDataArray[index+1].key,},
                        ]
                    }else{
                        return pre
                    }

                },[])
//                if(allDesc.params.length != 0){
//
//                }
                myDiagram.model = new go.GraphLinksModel({
                    copiesArrays: true,
                    copiesArrayObjects: true,
//                      linkFromPortIdProperty: 'fromPort',
//                      linkToPortIdProperty: 'toPort',
                      nodeDataArray,
//                    nodeDataArray: [
//                        {
//                            key: '触发指令',
//                            fields: [
//                                {name: "", info: '00H 11H', color: '#F7B84B', figure: 'Ellipse'},
//                                {name: '指令2', info: '00H 11H', color: '#F25022', figure: 'Ellipse'},
//                                {name: '指令3', info: '00H 11H', color: '#00BCF2'}
//                            ],
//                            loc: '-200 10'
//                        },
//                        {
//                            key: '触发判据',
//                            fields: [
//                                {name: '判据1', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#FFB900', figure: 'Diamond'},
//                                {name: '判据2', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#F25022', figure: 'Rectangle'},
//                                {name: '判据3', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#7FBA00', figure: 'Diamond'},
//                                {name: '判据4', info: '30s内，TGXT1860 xxx电流大于0.2', color: '#00BCF2', figure: 'Rectangle'},
//                            ],
//                            loc: '0 0'
//                        },
//                        {
//                            key: '终止条件',
//                            fields: [
//                                {name: '判据1', info: '30s内，TGXT1861 xxx电压大于0.2', color: '#FFB900', figure: 'Diamond'},
//
//                            ],
//                            loc: '350 30'
//                        }
//                    ],
                    linkDataArray,
//                    linkDataArray: [
//                        {from: '触发指令', to: '触发判据',},
//                        {from: '触发判据', to: '终止条件',},
//                    ]
                });

                // this is a bit inefficient, but should be OK for normal-sized graphs with reasonable numbers of items per node
                function findAllSelectedItems() {
                    var items = [];
                    for (var nit = myDiagram.nodes; nit.next();) {
                        var node = nit.value;
                        var table = node.findObject('TABLE');
                        if (table) {
                            for (var iit = table.elements; iit.next();) {
                                var itempanel = iit.value;
                                if (isFieldSelected(itempanel)) items.push(itempanel);
                            }
                        }
                    }
                    return items;
                }

                // Override the standard CommandHandler deleteSelection behavior.
                // If there are any selected items, delete them instead of deleting any selected nodes or links.
                myDiagram.commandHandler.canDeleteSelection = function () {
                    // method override must be function, not =>
                    // true if there are any selected deletable nodes or links,
                    // or if there are any selected items within nodes
                    return go.CommandHandler.prototype.canDeleteSelection.call(this) || findAllSelectedItems().length > 0;
                };

                myDiagram.commandHandler.deleteSelection = function () {
                    // method override must be function, not =>
                    var items = findAllSelectedItems();
                    if (items.length > 0) {
                        // if there are any selected items, delete them
                        myDiagram.startTransaction('delete items');
                        for (var i = 0; i < items.length; i++) {
                            var panel = items[i];
                            var nodedata = panel.part.data;
                            var itemarray = nodedata.fields;
                            var itemdata = panel.data;
                            var itemindex = itemarray.indexOf(itemdata);
                            myDiagram.model.removeArrayItem(itemarray, itemindex);
                        }
                        myDiagram.commitTransaction('delete items');
                    } else {
                        // otherwise just delete nodes and/or links, as usual
                        go.CommandHandler.prototype.deleteSelection.call(this);
                    }
                };

//                    showModel(); // show the diagram's initial model
//
//                    function showModel() {
//                      document.getElementById('mySavedModel').innerHTML = myDiagram.model.toJson();
//                      if (window.Prism) window.Prism.highlightAll();
//                    }
            },
            render_goChart_ABN_real_record_kjz: (active_key, data) => {
                if (data.length == 0 || active_key !== '故障模式全局监控') return "点击上方查看判读流程";

                const data_dict_json = typeof data[0] === 'string' ? JSON.parse(data[0]) : data[0];
                const data_dict = data_dict_json.PROCESSOR_INFO.reduce((pre, cru, index) => {
                    if (index == 0) {
                        return [
                            ...pre,
                            {
                                key: 0,
                                gender: data_dict_json.STATUS_INFO["结果"] == "False" ? "no_satisfy" : "satisfy",
                                kanjiName: `结果：${data_dict_json.STATUS_INFO["结果"]}`,
                            },
                            {
                                key: 1,
                                parent: 0,
                                gender: "",
                                kanjiName: `状态：${data_dict_json.STATUS_INFO["状态"]}`,
                            },
                            {
                                key: 2,
                                parent: 1,
                                gender: cru.info["结果"] == "False" ? "no_heat" : "heat",
                                kanjiName: `状态：${cru.info["状态"]};\n结果：${cru.info["结果"]};\n判据类型：${cru.type}`,
                            },
                        ];
                    } else {
                        return [
                            ...pre,
                            {
                                key: Number(cru.index) + 1,
                                parent: 1,
                                gender: cru.info["结果"] == "False" ? "no_heat" : "heat",
                                kanjiName: `状态：${cru.info["状态"]};\n结果：${cru.info["结果"]};\n判据类型：${cru.type}`,
                            },
                        ];
                    }
                }, []);

                console.log(data_dict);
                if (this.myDiagram_record) {
                    this.myDiagram_record.div = null; // 重新渲染时需清空div
                }
                this.myDiagram_record = new go.Diagram('ABN_real_record_gojs-kjz', {
                    allowCopy: false,
                    layout: new go.TreeLayout({angle: 90, nodeSpacing: 3}),
                });

                this.myDiagram_record.animationManager.isEnabled = false;
                // var bluegrad = new go.Brush('Linear', {0: 'rgb(60, 204, 254)', 1: 'rgb(70, 172, 254)'});
                // var pinkgrad = new go.Brush('Linear', {0: 'rgb(255, 192, 203)', 1: 'rgb(255, 142, 203)'});
                // var greengrad = new go.Brush('Linear', {0: 'rgb(60, 204, 254)', 1: 'rgb(70, 172, 254)'});
                // var redgrad = new go.Brush('Linear', {0: 'rgb(255, 192, 203)', 1: 'rgb(255, 142, 203)'});
                const heatGrad = new go.Brush("Linear", { 0: "rgba(22,119,255,0.2)", 1: "rgba(22,119,255,0.35)" });      // heat
                const noHeatGrad = new go.Brush("Linear", { 0: "rgba(255,77,79,0.25)", 1: "rgba(255,77,79,0.35)" });      // no_heat
                const satisfyGrad = new go.Brush("Linear", { 0: "rgba(0,185,107,0.25)", 1: "rgba(0,185,107,0.35)" });     // satisfy
                const noSatisfyGrad = new go.Brush("Linear", { 0: "rgba(255,77,79,0.25)", 1: "rgba(255,77,79,0.35)" });

                this.myDiagram_record.add(
                  new go.Part("Table", {
                      layerName: "ViewportBackground",
                      alignment: new go.Spot(0, 0, 20, 20),
                      background: "rgba(0,0,0,0.15)",      // 添加柔和暗背景
                      padding: 6,
                      cornerRadius: 4
                  }).add(
                      new go.TextBlock("图例", { row: 0, stroke:"#ddd", font:"bold 13px sans-serif", margin:4 }),
                      new go.Panel("Horizontal", { row: 1, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:heatGrad, margin:4 }),
                               new go.TextBlock("已触发",{ stroke:"#ccc", font:"12px sans-serif"})),
                      new go.Panel("Horizontal", { row: 2, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:noHeatGrad, margin:4 }),
                               new go.TextBlock("未触发",{ stroke:"#ccc", font:"12px sans-serif"})),
                      new go.Panel("Horizontal", { row: 3, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:satisfyGrad, margin:4 }),
                               new go.TextBlock("已满足",{ stroke:"#ccc", font:"12px sans-serif"})),
                      new go.Panel("Horizontal", { row: 4, alignment: go.Spot.Left })
                          .add(new go.Shape("Rectangle",{ desiredSize:new go.Size(20,20), fill:noSatisfyGrad, margin:4 }),
                               new go.TextBlock("未满足",{ stroke:"#ccc", font:"12px sans-serif"}))
                  )
                );




                function genderBrushConverter(gender) {
                    if (gender === 'heat') return heatGrad;
                    if (gender === 'no_heat') return noHeatGrad;
                    if (gender === 'satisfy') return satisfyGrad;
                    if (gender === 'no_satisfy') return noSatisfyGrad;
                    return "#2d2d2d"; // default block
                }

                this.myDiagram_record.nodeTemplate = new go.Node('Auto', {
                    deletable: false,
                    mouseEnter: (e,node)=>{
                        node.findObject("RECT").stroke = "#4096ff";
                        node.findObject("RECT").strokeWidth = 2;
                        node.findObject("RECT").shadowBlur = 10;
                        node.findObject("RECT").shadowColor = "rgba(64,150,255,0.4)";
                      },
                     mouseLeave: (e,node)=>{
                        node.findObject("RECT").stroke = "#555";
                        node.findObject("RECT").strokeWidth = 1;
                        node.findObject("RECT").shadowBlur = 0;
                     }

                })
                    .add(
                        new go.Shape('Rectangle', {
                            stroke: "#555",
                            strokeWidth: 1,
                            fill: "#2d2d2d",  // default if no gender
                            cornerRadius: 6,
                            stretch: go.Stretch.Fill,
                            alignment: go.Spot.Center
                        })
                            .bind('fill', 'gender', genderBrushConverter),
                        new go.Panel('Vertical')
                            .add(
                                new go.TextBlock({
                                    alignment: go.Spot.Center,
                                    padding: 10,
                                    margin: 8,
                                    font: "13px sans-serif",
                                    stroke: "#eee",
                                })
                                    .bind('text', 'kanjiName'),
                            )
                    );

                this.myDiagram_record.linkTemplate = new go.Link({
                    routing: go.Routing.Orthogonal,
                    corner: 6, selectable: false
                })
                    .add(
                        new go.Shape({ stroke: "#444", strokeWidth: 1.2 })
                    );
                this.myDiagram_record.background = "#1f1f1f";
                this.myDiagram_record.model = new go.TreeModel(data_dict);
            },
            render_modal_chart_kjz:(data) => {
                if(Object.keys(data).length == 0) return
                var myChart = echarts.init(document.getElementById("ABN-Check-YC-Modal-Chart-Container-kjz"));
                option = {
                      title: {
                            // 可以隐藏默认的标题
                            show: false
                      },
                      xAxis: {
                        type: 'time',
                      },
                      tooltip: {
                          trigger: 'axis',
//                          showContent: false
                      },
                      legend:{
                        type: 'scroll', // 启用滚动翻页功能
                        orient: 'horizontal',
                        pageButtonPosition: 'end',
                        pageFormatter: '{current}/{total}',
                        data:Object.keys(data)
                      },
                      yAxis: {
                        type: 'value'
                      },
                      legend:{

                      },
                      toolbox: {
                        show: true,
                        orient: 'vertical',
                        right: '5%',
                        top:'20%',
                        feature: {
                          mark: { show: true },
                          dataView: { show: true, readOnly: false },
                          magicType: { show: true, type: ['line', 'bar'] },
                          restore: { show: true },
                          saveAsImage: { show: true }
                        }
                      },
                      dataZoom: [
                            {
                                type: 'slider', // 使用滑动条进行缩放
                                xAxisIndex: 0, // 控制第一个x轴
                                start: 0, // 数据窗口范围的起始百分比
                                end: 100 // 数据窗口范围的结束百分比
                                // 其他可选配置...
                            },
                            {
                                type: 'inside', // 内置于坐标系中，可以通过鼠标滚轮进行缩放
                                xAxisIndex: 0, // 控制第一个x轴
                                // 其他可选配置...
                            }
                      ],
                      series: Object.keys(data).reduce((pre,cru) => {
                            return [
                                ...pre,
                                {
                                  name:cru,
                                  data: data[cru].sort((a,b) => a[0]-b[0]),
                                  type: 'line',
                                  smooth: true,
                                }
                            ]
                      },[])
                };
                myChart.setOption(option)
            }

        }
    }
)
