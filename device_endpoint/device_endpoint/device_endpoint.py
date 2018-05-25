import asyncio
from pprint import pprint, pformat

from aiohttp import web, ClientSession

from .metrics import DeviceSensorSample

PROMETHEUS_URL = 'http://pushgateway:9091'
routes = web.RouteTableDef()


async def send_prometheus_metrics(sample):
    # todo: persist client across multiple calls
    url = '{}/metrics/job/iot_device_{}'.format(PROMETHEUS_URL, sample.serial)
    data = bytes(sample.to_prometheus_pushmetrics(), 'utf8')
    print(url)
    print(data)
    async with ClientSession(raise_for_status=True) as session:
        await session.post(url, data=data)


@routes.get('/')
async def handle_get(request):
    return web.Response()


@routes.post('/')
async def handle_post(request):
    data = await request.json()
    pprint(data)
    sample = DeviceSensorSample.from_dict(data)
    await send_prometheus_metrics(sample)
    return web.json_response({'result': 'ok'})


def run():
    app = web.Application()
    app.router.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=8080)
