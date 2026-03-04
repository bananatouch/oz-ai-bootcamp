import asyncio
import time

# await asyncio.sleep(): 다른 코루틴도 동시에 돌림
async def good_task():
    print("Task 시작")
    await asyncio.sleep(5)  # 5초 대기
    print("Task 끝")

# time.sleep(): 다른 모든 것을 링크도 음 (Blocking)
async def bad_task():
    print("BadTask 시작")
    time.sleep(5)  # 중단! 다른 걸 모두 기다렸다가
    print("BadTask 끝")

async def main():
    # 5개를 동시 실행하려고 하지만, bad_task가 전체를 느리게 함
    await asyncio.gather(
        good_task(),
        good_task(),
        good_task(),
        good_task(),
        bad_task()
    )

asyncio.run(main())
