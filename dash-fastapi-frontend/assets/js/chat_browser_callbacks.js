
let message_temp = ""
const uuid_dict = {}
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    chat_clientside: {
        handleChatContainerFullscreen: (nClicks, icon) => {
            return [
                icon === 'antd-full-screen' ? 'antd-full-screen-exit' : 'antd-full-screen',
                (
                    icon === 'antd-full-screen' ?
                        {
                            width: '100vw',
                            height: '100vh'
                        } :
                        {
                            width: '90vw',
                            height: '90vh',
                            maxWidth: 1200,
                            borderRadius: 16,
                            border: '1px solid #dedede'
                        }
                )
            ];
        },
        handleOperationButtonGroupVisible: (isHovering, originStyle) => {
            if (isHovering) {
                delete (originStyle.transform)
                return {
                    ...originStyle,
                    opacity: 1,
                    transform: 'scale(1) translateY(0)'
                }
            }
            return {
                ...originStyle,
                opacity: 0,
                transform: 'scale(0.8) translateY(10px)'
            }
        },
        handleUserNewMessageSend: (_, __, ___, value) => {
//            console.log(value)
            // 判断问题是否为空
            if (!value) {
                return window.dash_clientside.no_update;
            }

            // 若本次回调由shift+enter组合触发
            if (window.dash_clientside.callback_context.triggered_id === 'shift-enter-keypress') {
                return [
                    window.dash_clientside.no_update,
                    `${value}\n` // 为value追加换行符
                ]
            }
            // 否则，视作独立enter触发，执行新内容发送
            return [
                value,
                '' // 重置输入框内容
            ];
        },
        handleStreamResponse: (data) => {
            if(data.message_id in  uuid_dict){
                   return window.dash_clientside.no_update;
            }
            uuid_dict[data.message_id] = data;
            console.log(data)
            message_temp = "";
            const source = new EventSource(`http://10.2.28.65:9099/streaming?model_name=${data.model_name}&sub_model_name=${data.sub_model_name}
            &temperature=${data.temperature}&max_tokens=${data.max_tokens}&session_id=${data.session_id}&message_id=${data.message_id}&message=${data.user_input_text}&mode=${data.mode}`);
            console.log(data.message_id)
            source.onmessage = function(event) {
                    const eventData = JSON.parse(event.data)
                    if ("isFinished" in eventData) {
                        window.dash_clientside.set_props('input-text', { disabled: false })
                        window.dash_clientside.set_props('send-input-text', { loading: false })
                        source.close();
                    }else{
                        message_temp = message_temp+eventData.content.replaceAll("<换行符>", "\n")
                        window.dash_clientside.set_props({'type': "assistant-output-markdown", 'index': data.message_id},{markdownStr:message_temp})
                    }
            };
//            if (data) {
//                data = JSON.parse(data)
//                if (data.type === "<出现错误>") {
//                     return [
//                         null,
//                         {
//                             namespace: 'feffery_antd_components',
//                             type: 'AntdAlert',
//                             props: {
//                                 type: 'info',
//                                 message: data.content,
//                                 showIcon: true
//                             }
//                         }
//                     ]
//                }
//                if ("isFinished" in data) {
//                    // 还原输入框、发送按钮的状态
//                    window.dash_clientside.set_props('input-text', { disabled: false })
//                    window.dash_clientside.set_props('send-input-text', { loading: false })
//                    return [markdownStr, null]
//
//                } else {
//                    return [
//                        markdownStr + data.content.replaceAll("<换行符>", "\n"),
//                        null
//                    ];
//                }
//            }
            return window.dash_clientside.no_update;
        },
        handleChatAreaScroll: (height, checked) => {

            if (checked) {
                // 自动滚动到底部操作
                let scrollTarget = document.getElementById('chat-area')
                // 执行滚动到底部操作
                scrollTarget.scrollTo({
                    top: scrollTarget.scrollHeight
                });
            }
        },
        handleChatAreaToTopBottom: (nClicksTop, nClicksBottom) => {
            if (window.dash_clientside.callback_context.triggered_id === 'chat-area-to-top') {
                let scrollTarget = document.getElementById('chat-area')
                // 执行滚动到顶部操作
                scrollTarget.scrollTo({
                    top: 0
                });
            } else {
                let scrollTarget = document.getElementById('chat-area')
                // 执行滚动到底部操作
                scrollTarget.scrollTo({
                    top: scrollTarget.scrollHeight
                });
            }
        },
        handleAssistantOutputStop: (nClicks) => {
            // 更新输入框、发送按钮的状态
            window.dash_clientside.set_props('input-text', { disabled: false })
            window.dash_clientside.set_props('send-input-text', { loading: false })
            return 'close'
        },
        handleAssistantOutputRetry: (nClicks) => {
            // 更新输入框、发送按钮的状态
            window.dash_clientside.set_props('input-text', { disabled: true })
            window.dash_clientside.set_props('send-input-text', { loading: true })
            return ['', null, Date.now().toString()]
        },
        handleAssistantOutputCopy: (nClicks, markdownStr) => {
            // 写入当前内容到粘贴板
            navigator.clipboard.writeText(markdownStr);

            window.dash_clientside.set_props(
                'global-message',
                {
                    children: {
                        namespace: 'feffery_antd_components',
                        type: 'AntdMessage',
                        props: {
                            content: '复制成功！',
                            type: 'success'
                        }
                    }
                }
            )

            return window.dash_clientside.no_update;
        },
        showCurrentModel: (value) => {
            // 若value中含有“|”
            if (value.includes('|')) {
                return '当前模型：' + value.split('|')[1]
            }
            return '当前模型：' + value;
        }
    }
});