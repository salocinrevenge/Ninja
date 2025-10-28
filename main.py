from motor import Motor
import asyncio

if __name__ == "__main__":
    motor = Motor()
    asyncio.run(motor.run())

    # Set-ExecutionPolicy RemoteSigned -Scope Process
    # .\pypyvenv\Scripts\activate
    # python main.py

    # .\venv_old\Scripts\activate
    # python old/coracao.py