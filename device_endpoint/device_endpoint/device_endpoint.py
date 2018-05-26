import asyncio
from pprint import pprint, pformat

from aiohttp import web, ClientSession

from .metrics import DeviceSensorSample

#PROMETHEUS_URL = 'http://pushgateway:9091'
PROMETHEUS_URL = 'http://pushgateway-myproject.cluster.test'
routes = web.RouteTableDef()


async def send_prometheus_metrics(sample):
    # todo: persist client across multiple calls
    async with ClientSession() as session:
        print('== Metrics: Posting ==')
        url = '{}/metrics/job/iot_device_{}'.format(PROMETHEUS_URL, sample.serial)
        data = bytes(sample.to_prometheus_pushmetrics(), 'utf8')
        print(url)
        print(data.decode(), end='')
        async with session.post(url, data=data) as response:
            print('== Metrics: Response ==')
            print(response.status)
            print(await response.text())


@routes.get('/')
async def handle_get(request):
    return web.Response()


@routes.post('/')
async def handle_post(request):
    print('== Device: Request ==')
    data = await request.json()
    pprint(data)
    sample = DeviceSensorSample.from_dict(data)
    await send_prometheus_metrics(sample)
    print('== Device: Responding ==')
    response = {'result': 'ok'}
    print(response)
    return web.json_response(response)


def run():
    app = web.Application()
    app.router.add_routes(routes)
    web.run_app(app, host='0.0.0.0', port=8080)
