import asyncio
from pprint import pprint


from aiohttp import web


async def handler(request):
    pprint(vars(request))
    return web.Response(text="OK")


async def main(loop):
    server = web.Server(handler)
    await loop.create_server(server, "0.0.0.0", 8080)
    print("======= Serving on http://0.0.0.0:8080/ ======")

    # pause here for very long time by serving HTTP requests and
    # waiting for keyboard interruption
    await asyncio.sleep(100*3600)


def run():
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main(loop))
    except KeyboardInterrupt:
        pass
    loop.close()
