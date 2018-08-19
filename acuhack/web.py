from datetime import datetime
import logging
from json import dumps

import aiohttp
from aiohttp.web import Application, Response, RouteTableDef, HTTPNotFound, json_response, run_app

logger = logging.getLogger(__name__)

data = {}


async def forward_request(request):
    async with aiohttp.request(request.method, request.url, headers=request.headers) as response:
        return Response(text=await response.text(), headers=response.headers)


app = Application()
routes = RouteTableDef()


@routes.get('/weatherstation/updateweatherstation')
async def measurement(request):
    measurement = dict(request.query)
    measurement['dateutc'] = datetime.utcnow()
    station = data.setdefault(measurement.pop('id'), {})
    sensor_data = station.setdefault(measurement.pop('sensor'), [])
    sensor_data.append(measurement)
    return await forward_request(request)


@routes.get('/log')
def log(_):
    return json_response(text=dumps(data, default=str))


@routes.route('*', '/{tail:.*}')
async def catch_all(request):
    logger.warning('Unexpected request %s', request)
    raise HTTPNotFound()


app.add_routes(routes)


def run(host, port):
    return run_app(app, host=host, port=port)
