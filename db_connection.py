# SQLAlchemy 사용에 필요한 기본 설정

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB 접속 정보(DB 종류, 주소, 포트, DB 이름, 사용자 이름, 비밀번호)

DATABASE_URL = "sqlite:///./test.db"  # SQLite 예시, 다른 DB를 사용할 경우 URL 형식에 맞게 변경

# Engine: DB와 연결을 제공하는 객체
engine = create_engine(DATABASE_URL)

# Session: DB의 작업단위
# SessionFactory: DB 세션을 생성하는 팩토리 함수(클래스)
SessionFactory = sessionmaker(
    bind= engine, # 엔진을 연결

    # 기본 옵션
    autocommit=False, # 자동 커밋 비활성화
    autoflush=False, # 자동 플러시 비활성화
    expire_on_commit=False # 커밋 후 객체의 상태 유지
)


# return -> 값 반환 & 함수 종료
# yield -> 값 반환 & 함수 일시 중지 -> 다음에 다시 함수 실행하면 yield 다음 코드부터 실행
def get_session():
    with SessionFactory() as session:
        try:
            yield session # session 객체를 반환하면서 함수 일시 중지
        finally:
            session.close() # 세션 닫기