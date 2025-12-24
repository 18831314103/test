from ollama import Client


class MultiUserChatbot:
    def __init__(self, host='http://localhost:11434', model='qwen2.5-20250402:latest', headers=None):
        # 初始化Chatbot对象
        self.client = Client(
            host=host,
            headers=headers if headers else {'x-some-header': 'some-value'}
        )
        self.model = model
        self.users_conversations = {}  # 用于存储每个用户的对话历史

    def add_message(self, user_id, role, content):
        """将用户或模型的消息添加到指定用户的对话历史"""
        if user_id not in self.users_conversations:
            self.users_conversations[user_id] = []

        self.users_conversations[user_id].append({'role': role, 'content': content})

    def get_response(self, user_id, prompt=None, stream=True):
        """获取指定用户的模型回应，并支持传入自定义prompt"""
        # 获取该用户的对话历史
        messages = self.users_conversations.get(user_id, [])

        # 如果有自定义的 prompt, 可以在对话历史的基础上传递该指令
        if prompt:
            # 在对话历史前添加用户的自定义prompt
            messages.insert(0, {'role': 'system', 'content': prompt})

        # 请求模型生成回应
        response = self.client.chat(
            model=self.model,
            messages=messages,
            stream=stream
        )

        # 处理流式响应
        if stream:
            return response
        else:
            return response['message']['content']

    def chat(self, user_id):
        """与指定用户进行多轮对话"""
        print(f"开始与用户 {user_id} 的对话...")
        while True:
            # 获取用户输入
            user_input = input(f"用户 {user_id} 输入: ")
            if user_input.lower() == "exit":
                print(f"用户 {user_id} 退出对话")
                break

            # 添加用户消息到对话历史
            self.add_message(user_id, 'user', user_input)

            # 获取模型回应并打印
            bot_response = self.get_response(user_id, stream=False)
            print(f"模型回应: {bot_response}")

            # 添加模型回应到对话历史
            self.add_message(user_id, 'assistant', bot_response)

    def start_chat(self, user_id, prompt=None):
        """启动指定用户的对话，并支持传递prompt"""
        print(f"开始与用户 {user_id} 的对话")
        self.chat(user_id)

    def set_custom_prompt(self, user_id, prompt):
        """为指定用户设置一个全局的自定义指令（prompt）"""
        print(f"为用户 {user_id} 设置自定义指令: {prompt}")
        self.users_conversations[user_id] = [{'role': 'system', 'content': prompt}]  # 清空历史并设置系统级prompt