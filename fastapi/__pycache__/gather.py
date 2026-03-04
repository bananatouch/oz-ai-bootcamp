# gater =  모으다
import asyncio
# 코루틴 = 동시에 실행되는 함수들

async def hello():
    print("Hello")


coro1 = hello()  # 코루틴 객체 생성
coro2 = hello()  # 코루틴 객체 생성

async def main():
    await asyncio.gather(coro1, coro2)  # coro1, coro2 동시에 실행


asyncio.run(main())  # main 실행

# 핵심 요점
# • 코루틴은 여러 개를 동시에 실행해야 효율이 나온다.
# • 하나의 코루틴만 필요하면 비동기로 할 필요가 없다.
# • 코루틴 문법을 써도 실제 동작이 순차적일 수 있으니 주의해야 한다.
# • gather()는 여러 코루틴을 동시에 실행하는 핵심 도구다.