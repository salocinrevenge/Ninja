from motor import Motor
import asyncio

if __name__ == "__main__":
    motor = Motor()
    asyncio.run(motor.run())

    # Set-ExecutionPolicy RemoteSigned -Scope Process
    # .\venv\Scripts\activate