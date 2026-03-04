# await: 대기 시간에 실행권을 다른 코루틴에게 넘기는 키워드
import asyncio
import time

# 순차적 실행 (차근차근 한 번에 하나씩)
def task_a():
    print("Task A 시작")
    time.sleep(3)  # 3초 대기
    print("Task A 끝")

def task_b():
    print("Task B 시작")
    time.sleep(3)  # 3초 대기
    print("Task B 끝")

# 동시 실행 (여러 일을 동시에)
async def coro_a():
    print("Coro A 시작")
    await asyncio.sleep(3)  # 대기하는 동안 다른 것도 돌아감
    print("Coro A 끝")

async def coro_b():
    print("Coro B 시작")
    await asyncio.sleep(3)  # 대기하는 동안 다른 것도 돌아감
    print("Coro B 끝")

async def main():
    # 두 코루틴을 동시에 실행
    await asyncio.gather(coro_a(), coro_b())

print("===== 순차 실행 =====\n")
sync_start = time.time()
task_a()  # Task A 끝날 때까지 기다림
task_b()  # 그 다음 Task B 끝날 때까지 기다림
sync_end = time.time()
print(f"총 소요 시간: {sync_end - sync_start:.2f}초\n")

print("===== 동시 실행 =====\n")
async_start = time.time()
asyncio.run(main())  # 두 코루틴을 동시에 실행
async_end = time.time()
print(f"총 소요 시간: {async_end - async_start:.2f}초\n")

# 결론
# • await는 대기 시간에 실행권을 넘겨서 다른 코루틴을 돌리는 키워드다.
# • await가 있는 코드 앞에 await를 붙여야 다른 작업도 동시에 실행된다.
# • 결과: 3초 + 3초 = 6초 대기를 3초로 줄일 수 있다.
#
# 순차 실행: 3 + 3 = 6초
# 동시 실행: max(3, 3) = 3초