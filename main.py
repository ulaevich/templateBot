import app.__main__ as app
import asyncio

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(app.main())
    loop.run_forever()