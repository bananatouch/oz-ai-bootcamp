from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    yield

app = FastAPI(lifespan=lifespan)


# 원하는 응답의 형식을 고정
class ResultSchema(BaseModel):
    result: str = Field(..., description="질문에 대한 답변")
    confidence: float = Field(..., description="답변의 신뢰도 (0.0 ~ 1.0)")


@app.post(
    "/gpt"
)
async def call_gpt_handler(
    request: Request, # 요청에 대한 메타 정보를 넘겨 받을수 있음
    user_input: str = Body(..., embed=True),
): # 요청의 body에서 user_input을 추출
    client = request.app.state.openai_client

    # # FastAPI -> OpenAI 서버 요청(네트워크) 3~5초
    # response = await client.responses.parse(
    #     model="gpt-4.1-mini",
    #     input = user_input,
    #     text_format=ResultSchema,
    # ) 
    

    async def event_generator():
        # 1) OpenAI 서버에 요청을 보내고,
        async with client.responses.stream(
            model="gpt-4.1-mini",
            input = user_input,
            text_format=ResultSchema,
        ) as stream:
            # 2) OpenAI 서버에서 응답이 도착할 때마다 이벤트를 발생시키는 제너레이터
            async for event in stream:
                # 3-1) event 값이 delta면, 그 안의 값(token)을 꺼낸다
                if event.type == "response.output_text.delta":
                    yield event.delta
                # 3-2) event 값이 completed면, 제너레이터를 종료한다
                elif event.type == "response.completed":
                    break

        
    return StreamingResponse(
        # generator로 응답을 스트리밍
        event_generator(),
        media_type="text/event-stream",
    )

