import httpx
import asyncio
from typing import List


class AsyncioClient:
    def __init__(self,
        timeout: int = 10,
        max_connection: int = 100,
        max_keepalive_connections: int = 20,
    ):
        limits = httpx.Limits(
            max_connections=max_connection,
            max_keepalive_connections=max_keepalive_connections
        )
        self.client = httpx.AsyncClient(
            timeout=timeout,
            limits=limits
        )

        self.semaphore = asyncio.Semaphore(10)

    async def fetch(self, url:str):
        async with self.semaphore:
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                print(f"Request failed {e}")
            except httpx.HTTPStatusError as e:
                print(f"An error occured: {e}")
            finally:
                print("Done with the work")
            return None
    
    async def fetch_many(self, url_list: List[str]):
        tasks = [self.fetch(url) for url in url_list]
        return await asyncio.gather(*tasks)
    
    async def close_connection(self):
        await self.client.aclose()