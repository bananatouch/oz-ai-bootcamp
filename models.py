# DB를 다루는 모델
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# 굳이 User에 DeclarativaBase를 바로 안넣고 Base에 상속받고 하는이유
# 공식 문서에서 제안하는 방법이기도 하며, 여러 모델이 있을 때 공통적으로 사용할 수 있는 베이스 클래스를 만들어서 상속받는 형태로 사용하는 것이 일반적
class Base(DeclarativeBase):
    pass

# Mapped, mapped_column -> SQLAlchemy에서 컬럼에 type hints를 지정하는 문법
class User(Base):
    __tablename__ = "user"

    # 사용 할 컬럼 정의
    id: Mapped[int] = mapped_column(Integer, primary_key=True) # primary_key: 기본키 -> 하나의 데이터를 식별하는 값
    name: Mapped[str] = mapped_column(String(32))
    age: Mapped[int] = mapped_column(Integer, nullable=True) # nullable: null 허용 여부 -> None 허용 여부
