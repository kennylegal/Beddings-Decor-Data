import asyncio
from ayncio_tutorial import AsyncioClient

async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
    ]

    client = AsyncioClient()

    results = await client.fetch_many(urls)

    print(results)

    await client.close_connection()


asyncio.run(main())