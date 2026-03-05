from fastapi import FastAPI         # FastAPI 프레임워크 로드
from sqlalchemy import text          # SQL 구문 텍스트 처리 도구
from database import SessionFactory  # DB 연결 세션 생성 도구 호출

app = FastAPI()                      # FastAPI 앱 인스턴스 생성

@app.get("/")                        # 루트 경로(/) 접속 시 GET 요청 처리
async def root_handler():            # 비동기 핸들러 함수 정의
    # DB 세션 시작 (with문 종료 시 자동 세션 반납)
    with SessionFactory() as session:
        # 실행할 SQL 쿼리문 작성 (users 테이블 전체 조회)
        stmt = text("SELECT * FROM users;")
        
        # 쿼리 실행(execute) 및 결과 전체 가져오기(fetchall)
        result = session.execute(stmt).mappings().all()
    
    # 최종 결과를 JSON 형태로 반환
    return {"result": result}