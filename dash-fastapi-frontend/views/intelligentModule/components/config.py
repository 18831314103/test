class AppConfig:
    # 初始化系统提示语
    initial_system_prompt = "我是工号9527，为您解答世间万物~"

    # 应用title
    app_title = "DashChat"

    # 版本号
    version = "0.0.1"


class ModelsConfig:
    # 构造内置支持模型列表信息，用于供用户选择及使用，每个子项表示一家大模型厂商，必填字段解释：
    # name: 模型厂商名称
    # logo: 模型厂商logo图片在assets中的对应路径
    # api_key: 模型厂商接口key
    # base_url: 模型厂商接口地址
    # sub_models: 模型列表，每个子项表示一种模型，字段解释：
    #     name: 模型名称或模型显示名称，当endpoint不为空时，在实际大模型服务调用接口中使用
    #     endpoint: 针对如豆包大模型的特殊模型名称传入要求，代替name，在实际大模型服务调用接口中使用

    # 示例配置参数，其中api_key自行替换为你的有效值
    models = [
        {
            "name": "moonshot",
            "logo": "assets/imgs/models-logo/moonshot.png",
            "api_key": None,
            "base_url": "https://api.moonshot.cn/v1",
            "sub_models": [
                {"name": "moonshot-v1-8k"},
                {"name": "moonshot-v1-32k"},
                {"name": "moonshot-v1-128k"},
            ],
        },
        {
            "name": "deepseek",
            "logo": "assets/imgs/models-logo/deepseek.png",
            "api_key": None,
            "base_url": "https://api.deepseek.com",
            "sub_models": [
                {"name": "deepseek-chat"},
            ],
        },
        {
            "name": "doubao",
            "logo": "assets/imgs/models-logo/doubao.png",
            "api_key": None,
            "base_url": "https://ark.cn-beijing.volces.com/api/v3",
            "sub_models": [
                # 针对豆包大模型中，需要自行创建模型的情况，此处的name仅用作标题展示，实际调用使用endpoint
                {"name": "doubao-lite-4k", "endpoint": "ep-20240614132802-kkwk2"},
                {"name": "doubao-lite-32k", "endpoint": "ep-20240614132934-2rgjj"},
                {"name": "doubao-lite-128k", "endpoint": "ep-20240614132952-rjzvh"},
                {"name": "doubao-pro-4k", "endpoint": "ep-20240614132921-f2z2d"},
                {"name": "doubao-pro-32k", "endpoint": "ep-20240614132853-j6xhj"},
                {"name": "doubao-pro-128k", "endpoint": "ep-20240614133041-9gjlb"},
            ],
        },
        {
            "name": "智谱",
            "logo": "assets/imgs/models-logo/智谱.png",
            "api_key": None,
            "base_url": "https://open.bigmodel.cn/api/paas/v4/",
            "sub_models": [
                {"name": "glm-4-0520"},
                {"name": "glm-4"},
                {"name": "glm-4-air"},
                {"name": "glm-4-airx"},
                {"name": "glm-4-flash"},
                {"name": "glm-3-turbo"},
            ],
        },
        {
            "name": "百川",
            "logo": "assets/imgs/models-logo/baichuan.png",
            "api_key": None,
            "base_url": "https://api.baichuan-ai.com/v1/",
            "sub_models": [
                {"name": "Baichuan4"},
                {"name": "Baichuan3-Turbo"},
                {"name": "Baichuan3-Turbo-128k"},
                {"name": "Baichuan2-Turbo"},
                {"name": "Baichuan2-Turbo-192k"},
                {"name": "Baichuan2-53B"},
            ],
        },
    ]
