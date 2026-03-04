import asyncio
from contextlib import asynccontextmanager

from llama_cpp import Llama
from fastapi import FastAPI, Request, Body
from fastapi.responses import StreamingResponse


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



app =  FastAPI(lifespan=lifespan)


# 결국에는  압도적인 데이터량을 가진 대형llm 거 끌어와서 활용하지 않을까요?
# 대형 모델 쓰려면 GPU가 필요할텐데, GPU는 비싸니까 작은 모델로 시작하는게 좋을 것 같아요.
# 그리고 스타트업의 경우에는 자원이 제한적이기 때문에 작은 모델로 시작해서 점차적으로 확장하는 전략이 더 현실적일 수 있습니다.
# 허깅페이스의 경우는 모델을 쉽게 다운로드하고 사용할 수 있도록 다양한 도구와 라이브러리를 제공하기 때문에, 
# 작은 모델로 시작해서 필요에 따라 더 큰 모델로 전환하는 것이 가능합니다.






# LLM에게 시스템 프롬프트를 설정하여 모델의 행동과 응답 스타일을 정의
SYSTEN_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)


@app.post("/chat")
async def generate_chat_handler(
    request: Request,
    user_input: str = Body(..., embed=True),
):  # 사용자 입력을 요청 본문에서 받음
    
    # embed = False -> user_input이 단일 문자열로 전달됨 "python이 뭐야?"
    # embed = True -> user_input이 딕셔너리 형태로 전달됨 {"user_input": "python이 뭐야?"}

    async def event_generator():
        llm = request.app.state.llm  # FastAPI의 상태에서 Llama 모델을 가져옴
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEN_PROMPT},  # 시스템 프롬프트 설정
                {"role": "user", "content": user_input}  # 사용자 입력을 모델에게 전달
            ],
            max_tokens=256,  # 최대 토큰 수
            temperature=0.7,  # 응답의 창의성 조절
            stream=True  # 스트리밍 모드 활성화
        )
        
        # response = [{c1}, {c2}, {c3}, ...] -> 모델이 생성하는 응답을 스트리밍으로 받아옴
        for chunk in response:  # 모델의 응답을 스트리밍으로 받아옴
            token = chunk["choices"][0]["delta"].get("content", "")  # 응답에서 새로 생성된 토큰을 추출
            if token:
                yield token  # 새로 생성된 토큰을 클라이언트로 스트리밍
                await asyncio.sleep(0)  # 작은 지연을 추가하여 스트리밍이 원활하게 이루어지도록 함

    # 스트리밍리스폰스란 응답을 한 번에 모두 보내는 것이 아니라, 데이터가 생성되는 대로 클라이언트로 전송하는 방식
    return StreamingResponse(
        event_generator(),   # 제너레이터
        media_type="text/event-stream",
    )  # 스트리밍 응답 반환






# [요점 정리]
# - LLM: 자연어 처리 작업 수행
# - 프롬프트: LLM에게 작업을 지시하는 입력 텍스트
# - LLM (Large Language Model): 텍스트 이해·생성 가능, 언어 관련 작업 활용
# - 구조: 프롬프트 → LLM → 모델의 응답

# - role
#   system: 모델의 규칙, 행동방식, 성격 / 작업 맥락 및 지침 제공
#   user: 사용자의 질문, 요청
#   assistant: 이전 모델 답변 / 대화 흐름 유지

# - Llama vs FastAPI 실행 순서
#   Llama: 모델 초기화·응답 생성
#   FastAPI: 웹 서버 구축·클라이언트 요청 처리
#   → Llama가 먼저 실행 (메모리 로드, 리소스 할당)
#   → 모델 준비 후 FastAPI에서 API 요청 처리 가능

# - Python generator
#   yield 키워드로 값 반환하는 함수
#   일반 함수와 달리 한 번에 하나의 값 반환
#   호출될 때마다 이전 상태 유지
#   메모리 효율적 사용, 대용량 데이터셋 처리·무한 시퀀스 생성 가능
#   for 루프·next() 함수로 순차적 값 추출

# [2026-03-04]
# 현대 컴퓨터의 기본 구조
# 조립 PC -> CPU, RAM, GPU, 저장장치 등 개별 부품으로 구성 
# 또 는 랩탑 -> CPU, RAM, GPU, 저장장치 등이 통합된 형태로 제공
# 램의 약자 RAM (Random Access Memory) -> 컴퓨터의 주기억장치, CPU가 데이터를 빠르게 읽고 쓸 수 있도록 지원
# CPU (Central Processing Unit) -> 컴퓨터의 중앙 처리 장치, 명령어
# GPU (Graphics Processing Unit) -> 그래픽 처리 장치, 병렬 처리 능력으로 대규모 데이터 처리에 유리
# 하드 드라이브 (HDD) / 솔리드 스테이트 드라이브 (SSD) -> 데이터 저장 장치, SSD는 빠른 읽기/쓰기 속도 제공
# 램의 주 역할 - CPU가 데이터를 빠르게 읽고 쓸 수 있도록 지원

# 비동기 프로그래밍
# 동기 프로그래밍: 작업이 순차적으로 실행, 각 작업이 완료될 때까지 다음 작업 대기
# 비동기 프로그래밍: 작업이 동시에 실행, 하나의 작업이 완료될 때까지 다른 작업이 대기하지 않고 실행 가능
# 비동기 프로그래밍은 I/O 작업 (예: 네트워크 요청, 파일 읽기/쓰기)에서 특히 유용, CPU가 다른 작업을 수행하는 동안 대기 시간 활용 가능


# FastAPI는 비동기 프로그래밍을 지원하여 높은 성능과 확장성을 제공

