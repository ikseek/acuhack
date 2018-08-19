from datetime import datetime
import logging

import aiohttp
from aiohttp.web import Application, Response, RouteTableDef, HTTPNotFound, run_app

from acuhack.reading import Message

logger = logging.getLogger(__name__)

data = []


async def forward_request(request):
    async with aiohttp.request(request.method, request.url, headers=request.headers) as response:
        return Response(text=await response.text(), headers=response.headers)


app = Application()
routes = RouteTableDef()


@routes.get('/weatherstation/updateweatherstation')
async def measurement(request):
    data.append(Message.from_dict(dict(request.query)))
    return await forward_request(request)


@routes.get('/log')
def log(_):
    return Response(text="\n".join(str(m) for m in data))


@routes.route('*', '/{tail:.*}')
async def catch_all(request):
    logger.warning('Unexpected request %s', request)
    raise HTTPNotFound()


app.add_routes(routes)


def run(host, port):
    return run_app(app, host=host, port=port)
