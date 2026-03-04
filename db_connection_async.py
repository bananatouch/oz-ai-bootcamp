# 비동기 SQLALchemy 연결 설정 파일
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(DATABASE_URL, echo=True) 

def sessionmaker(*args, **kwargs):
    raise NotImplementedError
# echo=True -> SQLAlchemy가 실행하는 SQL 쿼리를 로그로 출력

AsyncSessionFactory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

async def get_async_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()

        