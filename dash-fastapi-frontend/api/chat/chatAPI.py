from flask import Flask, request, Response
from config.enums import ApiMethod
from utils.request import api_request
import json
import uuid
import time

app = Flask(__name__)

class StreamingApi:
    """
    提供流式响应接口
    """

    @classmethod
    def stream_response(cls, question: str):
        """
        处理流式响应接口
        :param question: 用户提出的问题
        :return: 实时返回推理内容和回答内容
        """

        def _stream():
            # 模拟API请求
            response = api_request(
                url='/deepseek/chat/completions',  # 假设这是流式接口的路径
                method=ApiMethod.POST,
                json={
                    "model": "deepseek-reasoner",
                    "messages": [{"role": "user", "content": question}],
                    "stream": True
                }
            )

            start_time = time.time()
            reasoning_content_chunk = ""
            answer_content_chunk = ""

            # 假设API返回一个流式响应对象，这个流会持续传递数据块
            for chunk in response:
                reasoning_content_chunk += chunk.get('choices', [{}])[0].get('delta', {}).get('reasoning_content', "") or ""
                answer_content_chunk += chunk.get('choices', [{}])[0].get('delta', {}).get('content', "") or ""

                if time.time() - start_time > 0.1:  # 每0.1秒发送一次数据
                    yield "data: {}\n\n".format(
                        json.dumps(
                            {
                                "uuid": str(uuid.uuid4()),
                                "reasoning_content": reasoning_content_chunk.replace("\n", "<换行>"),
                                "answer_content": answer_content_chunk.replace("\n", "<换行>")
                            },
                            ensure_ascii=False,
                        )
                    )
                    start_time = time.time()  # 重置计时器
                    reasoning_content_chunk = ""
                    answer_content_chunk = ""

            # 当数据流结束时，发送最后的数据并标记完成
            time.sleep(0.1)  # 防止快速返回
            yield "data: {}\n\n".format(
                json.dumps(
                    {
                        "uuid": str(uuid.uuid4()),
                        "reasoning_content": reasoning_content_chunk.replace("\n", "<换行>"),
                        "answer_content": answer_content_chunk.replace("\n", "<换行>"),
                        "isFinished": True,
                    },
                    ensure_ascii=False,
                )
            )

        # 返回流式响应
        return Response(_stream(), mimetype="text/event-stream")


@app.route("/StreamingApi")
def streaming_api():
    question = request.args.get("question")
    if not question:
        return "Question is required", 400  # 返回错误信息
    return StreamingApi.stream_response(question)