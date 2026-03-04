import asyncio
from contextlib import asynccontextmanager

from llama_cpp import Llama
from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 실행 전, 준비되어야 하는 작업을 여기에 작성
    # FastAPI 객체 안에 임시 저장소 (app.state)을 만들어 Llama 모델을 저장
    app.state.llm = Llama(
        model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",  # 모델 경로
        n_ctx=4096,  # 컨텍스트 크기
        n_threads=2,  # CPU 스레드 수
        verbose=False,  # 로그 출력을 간단하게 -> True로 설정하면 더 자세한 로그가 출력됩니다.
        chat_format="llama-3"  # 응답 생성 포맷 
    )   
    yield
    # 서버 종료 시, 정리해야 하는 작업을 여기에 작성


def get_llm(app: FastAPI) -> Llama:
    """FastAPI 앱 상태에서 Llama 객체를 반환합니다."""
    return app.state.llm
