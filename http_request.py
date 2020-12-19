import aiohttp, asyncio, json
from typing import List, Dict, Union

def request(urls: Union[str, List[str]]):
    if not isinstance(urls, list): urls = [urls]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(request_many_aiohttp(urls))
    if len(results) == 1: results = results[0]
    return results

async def request_many_aiohttp(urls: List[str]):
    conn = aiohttp.TCPConnector(limit=100)
    results = []

    async with aiohttp.ClientSession(connector=conn, auth=None) as session:
        for i in range(len(urls)):
            res = await asyncio.create_task(fetch_many_aiohttp(session, urls[i]))
            results.append(res)

    return results

async def fetch_many_aiohttp(session: aiohttp.ClientSession, url: str):
    async with session.get(url=url) as response:
        if response.status==200:
            if response.content_type=='application/json':
                result = await response.json()
            else:
                content = await response.content.read()
                result = json.loads(content)
        else:
            raise AssertionError((
                f'response received: {response.status}, ' +
                f'{response.reason}; URL: {url}'))

    return result