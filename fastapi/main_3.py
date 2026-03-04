import anyio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Path, Query, Body, status, HTTPException, Depends, BackgroundTasks
from sqlalchemy import select
from db_connection import SessionFactory, get_session
from models import User
from schema import UserSignUpRequest, UserResponse, UserUpdateRequest

def send_email(name: str):
    import time
    time.sleep(5)  # 5초 대기
    print(f"{name}님에게 이메일을 보냈습니다.")

@asynccontextmanager
async def lifespan(_):
    # 앱 시작 시 실행되는 블록
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200  # 스레드 풀을 200개로 늘림
    yield
    # 앱 종료 시 정리할 작업이 있으면 여기서

# lifespan: 서버 시작/종료 시 리소스를 관리하는 기능
app = FastAPI(lifespan=lifespan)

# 임시 인메모리 사용자 데이터 (DB 사용 시 불필요)
# users = [
#     {"id": 1, "name": "alex", "age": 20},
#     {"id": 2, "name": "tom", "age": 30},
#     {"id": 3, "name": "hank", "age": 40},
#     {"id": 4, "name": "jane", "age": 50},
#     {"id": 5, "name": "mike", "age": 60},
# ]

# 전체 사용자 조회 API
@app.get("/users",
        response_model=list[UserResponse],
        status_code=status.HTTP_200_OK)
def get_users_handlers(
    session = Depends(get_session)
):
    stmt = select(User)
    result = session.execute(stmt)
    users = result.scalars().all()
    return users

# 회원 검색 API
# @app.get("/users/search")
# def search_user_handler():
#     return {"msg": "Welcome"}

# Path 매개변수: URL의 일부를 변수로 받는 방식
# 예: /users/{user_id} -> user_id 값을 매개변수로 받음
# type hint로 타입 검사, ge/gt/le/lt로 값 제약 설정 가능

# @app.get("/users/{user_id}")
# def get_user_handler(user_id: int):
#     if user_id < 1:
#         return {"msg": "잘못된 user_id 값입니다."}
#     return users[user_id - 1]

# Path 제약 조건 사용
# @app.get("/users/{user_id}")
# def get_user_handler(
#     user_id: int = Path(..., ge=1, description="user_id는 1이상")
# ):
#     return users[user_id - 1]

# 아이템 조회 예시
# item_name: 문자열, 최대 6글자 제약
items = [
    {"id": 1, "name": "apple"},
    {"id": 2, "name": "banana"},
    {"id": 3, "name": "cherry"},
]

@app.get("/items")
def get_item_handlers():
    return items

@app.get("/items/{item_name}")
def get_item_handler(
    item_name: str = Path(..., max_length=6, description="item_name는 문자형식이고 최대6자까지 가능")
):
    return {"item_name": item_name}


# Query 파라미터
# URL 뒤에 ?key=value 형태로 붙는 값
# 예: /users/search?name=alice&age=30
# 용도: 검색, 필터링, 정렬, 페이지네이션 등

@app.get("/users/search",
        response_model=list[UserResponse],
        status_code=status.HTTP_200_OK
        )
def search_user_handler(
    name: str = Query(..., min_length=2), # default=... 이랑 같은 의미
    age: int = Query(None, ge=1) # 선택적(optional)
):
    #name이라는 key로 넘어오는 Query Parameter 값을 사용하겠다.
    return {"id": 0, "name": name, "age": age}

# ?field=id => id값만 반환
# ?field=name => name 값만 반환
@app.get("/users/{user_id}",
        response_model=UserResponse,
        status_code=status.HTTP_200_OK
        )
def get_user_handler(
    user_id: int = Path(..., ge=1, description="user_id는 1이상"),
    session = Depends(get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar_one_or_none() # scalar_one_or_none() -> 결과가 하나면 User 객체 반환, 결과가 없으면 None 반환, 결과가 여러 개면 에러 발생
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자의 ID입니다.")
    
    return user


##################################################################################

#FastAPI의 핵심 동작이 Type Hints 위에 설계되어 있음

# 회원가입 API
# 회원가입에 필요한 데이터
# 휴대폰 번호 -> 토스
# 소셜 로그인 ->
# 하나의 계정 -> 두 가지 인증 (비밀번호 기반 / 간편 로그인)
@app.post(
    "/users/sign-up",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def sign_up_handler(
    body: UserSignUpRequest,
    background_tasks: BackgroundTasks,
    session = Depends(get_session)
):
    new_user = User(name=body.name, age=body.age)
    session.add(new_user)
    session.commit()
    
    # 가입 직후 이메일을 백그라운드에서 비동기 발송
    background_tasks.add_task(send_email, body.name)
    return new_user
    


################################################################################################

# 사용자 정보 수정
# PUT: 리소스 전체 교체 (모든 필드 필수)
# PATCH: 일부만 수정 (선택적)
@app.patch(
        "/users/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=UserResponse
        )
def update_user_handler(
    user_id: int = Path(..., ge=1),
    body: UserUpdateRequest = Body(...),
    session = Depends(get_session)
):
    if body.name is None and body.age is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name과 age 중 하나는 필수로 입력해야 합니다.")

    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자의 ID입니다.")

    if body.name is not None:
        user.name = body.name
    if body.age is not None:
        user.age = body.age

    session.commit()
    return user


# 회원 탈퇴
@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 사용자의 ID입니다.")

    session.delete(user)
    session.commit()
    return {"message": f"사용자 ID {user_id}가 성공적으로 삭제되었습니다."}