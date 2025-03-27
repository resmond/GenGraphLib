from typing import Self

import asyncio

class RobotManager:
    def __init__(self: Self) -> None:
        self.cmd = ["/bin/journalctl -n 50 -o json"]
        self.robot = None

    async def start(self: Self) -> None:
        print('RobotManager.start')
        self.robot = await asyncio.create_subprocess_exec(*self.cmd, stdout=asyncio.subprocess.PIPE )
        print('RobotManager.stop')

    async def stop(self):
        if self.robot:
            self.robot.kill()
            stdout = await self.robot.stdout.readline()
            print(stdout)
            await self.robot.wait()
        self.robot = None

async def main():
    robot: RobotManager = RobotManager()
    print('created')
    print(f'{robot}')
    print()
    await robot.start()
    print('created')
    await asyncio.sleep(60)
    print('done sleeping')
    await robot.stop()
    print('stopped')

if __name__ == "__main__":
    print('main')
    try:
        asyncio.run(main())

    except Exception as e:
        print(f'Exception: {e}')
        

    print('done')