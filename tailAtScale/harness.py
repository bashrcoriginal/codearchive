import asyncio
import aiohttp
import logging
import time
import itertools
import random
import math

logging.basicConfig(level=logging.INFO)

def get_endpoints_with_timeout(timeout, n):
    default_url = "https://www.httpbin.org/"
    default_query = "delay/"
    return n * [default_url + default_query + str(random.random()+timeout)]

async def get_endpoints(n=1000, default_timeout=5, outlier_timeout=10, outlier_ration=0.1):
    normal_count = int(n * (1 - outlier_ration))
    outlier_ration = n - normal_count
    return itertools.chain(get_endpoints_with_timeout(default_timeout, normal_count), get_endpoints_with_timeout(outlier_timeout, outlier_ration))

async def fetch_data(session, url):
    start_time = time.time()
    async with session.get(url) as response:
        latency = time.time() - start_time
        #logging.info(f"Latency for {url}: {latency} seconds")
        return await response.text(), latency, url
async def fetch(session, url, jitter_timeout=0.3, default_timeout=0.5, outlier_timeout=10):
    fetch_task = asyncio.create_task(fetch_data(session, url))
    done, pending = await asyncio.wait([fetch_task], timeout=jitter_timeout)
    if len(done) == 0:
        #logging.info(f"Timeout for {url} after {jitter_timeout} seconds passed. Now trying jittering")
        jitter_task = asyncio.create_task(fetch_data(session, get_endpoints_with_timeout(default_timeout, 1)[0]))
        done, pending = await asyncio.wait([jitter_task, fetch_task], return_when=asyncio.FIRST_COMPLETED)
        finishedTask = await done.pop()
        return [finishedTask[0], finishedTask[1], finishedTask[2] + "Jittered"]
    return await done.pop()
async def fetch_all(urls):
        connector = aiohttp.TCPConnector(limit=None)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [asyncio.create_task(fetch(session, url)) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                try:
                    response, latency, url = result
                    #logging.info(f"Successful response from {url} after {latency} seconds")
                    for task in tasks:
                        if not task.done():
                            pass #task.cancel()
                    #return response
                except Exception as e:
                    logging.error(str(e))
start_time = time.time()
endpoints = asyncio.run(get_endpoints(1000, outlier_ration=0.1, outlier_timeout=10, default_timeout=1))
response = asyncio.run(fetch_all(endpoints))
logging.info(f"Total time taken: {time.time() - start_time} seconds")