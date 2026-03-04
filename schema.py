from pydantic import BaseModel

# 회원가입 요청 부분(Request Body)의 데이터 형태
class UserSignUpRequest(BaseModel):
    name: str # 필수값(required)
    age: int | None = None # 선택값(optional) -> default 값이 None

# 회원가입 응답 부분(Response Body)의 데이터 형태
class UserResponse(BaseModel):
    id: int
    name: str
    age: int | None


class UserUpdateRequest(BaseModel):
    name: str | None = None
    age: int | None = None