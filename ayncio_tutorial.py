import httpx
import asyncio
from typing import List, Optional
import logging
import random


def log():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("asyncio_logger.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

class AsyncioClient:
    def __init__(self,
        timeout: int = 10,
        max_retries: int = 5,
        max_connection: int = 100,
        max_keepalive_connections: int = 20,
        proxies: Optional[List[str]] = None,
    ):
        limits = httpx.Limits(
            max_connections=max_connection,
            max_keepalive_connections=max_keepalive_connections
        )
        self.max_retires = max_retries
        self.client = httpx.AsyncClient(
            timeout=timeout,
            limits=limits
        )
        self.proxies = proxies or []
        self.logger = log()

        self.semaphore = asyncio.Semaphore(10)

    def get_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    async def fetch(self, url: str):
        async with self.semaphore:
            proxy = self.get_proxy()
            for attempt in range(1, self.max_retires + 1):
                self.logger.info(f"Attempting to fetch data from {url}, attempt {attempt} of {self.max_retires + 1}")
                try:
                    response = await self.client.get(url=url, headers=proxy)
                    if response.status_code == 429:
                        retry_after = int(response.headers.get("Retry-After", 2))
                        self.logger.warning(f"Rate limited, retry after {retry_after}")
                        await asyncio.sleep(retry_after)
                        continue
                    response.raise_for_status()
                    self.logger.info(f"Data for {url}, fetched with response code {response.status_code}")
                    return response.json()
                except httpx.RequestError as e:
                    self.logger.error(f"Request failed {e}")
                except httpx.HTTPStatusError as e:
                    self.logger.error(f"An error occured: {e}")
                backoff = 2** attempt
                self.logger.warning(f"Backing off for {backoff} seconds")
                await asyncio.sleep(backoff)
            
    
    async def fetch_many(self, url_list: List[str]):
        tasks = [self.fetch(url) for url in url_list]
        return await asyncio.gather(*tasks)
    
    async def close_connection(self):
        await self.client.aclose()