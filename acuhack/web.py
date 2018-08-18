from datetime import datetime
import logging
import json
from wsgiref.util import is_hop_by_hop

from bottle import route, request, response, run
import requests

log = logging.getLogger(__name__)

data = {}


def forward_request():
    remote = requests.request(request.method, request.url, headers=request.headers)
    headers = {k: v for k, v in remote.headers.items() if not is_hop_by_hop(k)}
    response.headers.update(headers)
    return remote.text


@route('/weatherstation/updateweatherstation')
def measurement():
    measurement = dict(request.params)
    measurement['dateutc'] = datetime.utcnow()
    station = data.setdefault(measurement.pop('id'), {})
    sensor_data = station.setdefault(measurement.pop('sensor'), [])
    sensor_data.append(measurement)
    return forward_request()


@route('/log')
def log():
    return json.dumps(data, indent=4, sort_keys=True, default=str)


@route('/<:re:.*>')
def catch_all():
    log.warning('Unexpected request %s', request)
