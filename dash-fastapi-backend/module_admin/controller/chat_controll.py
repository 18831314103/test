# alarm_record_controller.py
from datetime import datetime

from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import StreamingResponse
from uuid import uuid4
from typing import AsyncGenerator
from ollama import Client
import time
import json
import uuid
from typing import Generator, Tuple
import requests


class MultiUserChatbot:
    def __init__(self, api_key: str, workspace_name: str):
        self.api_key = api_key
        self.workspace_name = workspace_name
        self.base_url = "http://10.2.28.168:3001/api/v1/workspace"

    def stream_chat(self, message: str, mode: str = "chat", session_id: str = None) -> Generator[str, None, None]:
        session_id = session_id or str(uuid.uuid4())
        url = f"{self.base_url}/{self.workspace_name}/stream-chat"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream; charset=utf-8",
        }

        try:
            with requests.post(
                    url,
                    headers=headers,
                    json={
                        "message": message,
                        "mode": mode,
                        "sessionId": session_id,
                        "max_tokens": 1024
                    },
                    stream=True,
            ) as response:
                response.raise_for_status()
                for chunk in response.iter_lines():
                    now = datetime.now()
                    if chunk.startswith(b'data:'):
                        try:
                            data = json.loads(chunk.decode().split('data:', 1)[-1])
                            textResponse = data.get("textResponse", "")
                            if textResponse == None:
                                yield "data: %s\n\n" % json.dumps(
                                    dict(
                                        type="<出现错误>",
                                        timestamp=time.time(),
                                        content="服务器出错",
                                    ),
                                    ensure_ascii=False,
                                )
                                break
                            text_chunk = textResponse.replace('</think>', '')
                            sources = data.get("sources", [])
                            if text_chunk.strip():
                                # print(text_chunk)
                                # yield f"data: {json.dumps({'text': text_chunk, 'sources': sources}, ensure_ascii=False)}\n\n"
                                # yield f"data: {json.dumps({'text': text_chunk,'uuid': str(uuid.uuid4()),'timestamp':time.time()}, ensure_ascii=False)}\n\n"
                                yield "data: %s\n\n" % json.dumps(
                                    dict(
                                        type="<正在回答>",
                                        timestamp=time.time(),
                                        content=text_chunk,
                                    ),
                                    ensure_ascii=False,
                                )
                            print(datetime.now() - now)
                            time.sleep(0.1)
                        except json.JSONDecodeError:
                            continue

                # 结束时发送 isFinished 标志
                yield f"data: {json.dumps({'isFinished': True,'type':'<回复结束>','content':''},ensure_ascii=False,)}\n\n"

        except requests.exceptions.RequestException as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"


# 创建聊天机器人实例
chatbot = MultiUserChatbot(api_key="CWQZJBT-EF7MTB9-PP96TCE-WTQ8QD3",
                           workspace_name="phm-assistant")

chatControll = APIRouter()


@chatControll.get("/streaming", response_class=StreamingResponse)
async def stream_alarm_record(
        request: Request,
        message: str = Query(..., description="用户消息"),
        mode: str = Query("chat", description="聊天模式"),
        session_id: str = Query(None, description="会话ID")
):
    return StreamingResponse(
        chatbot.stream_chat(message=message, mode=mode, session_id=session_id),
        media_type="text/event-stream; charset=utf-8"
    )
