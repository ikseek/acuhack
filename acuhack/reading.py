from datetime import datetime
from dataclasses import dataclass

from pint import UnitRegistry

ur = UnitRegistry()


@dataclass
class Reading:
    timestamp: datetime
    temperature: ur.Quantity
    humidity_rel: float
    pressure: ur.Quantity

    def __str__(self):
        return f"{self.timestamp}, {self.temperature:P~.1f}, {self.pressure:P~.1f}, {self.humidity_rel:.0%}"

    def to_metric(self):
        return Reading(self.timestamp, self.temperature.to('celsius'), self.humidity_rel, self.pressure.to('hPa'))

    @classmethod
    def from_dict(cls, data):
        return cls(timestamp=datetime.utcnow(),
                   temperature=ur.Quantity(float(data['tempf']), 'degF'),
                   humidity_rel=float(data['humidity']) / 100,
                   pressure=ur.Quantity(float(data['baromin']), 'in_Hg'))


@dataclass
class Message:
    station: int
    sensor: int
    signal_strength: float
    battery_low: bool
    reading: Reading

    def __str__(self):
        return f"{self.sensor:04}: {self.reading}"

    @classmethod
    def from_dict(cls, data):
        return cls(station=int(data['id'], 16),
                   sensor=int(data['sensor'], 10),
                   signal_strength=1 / (5 - int(data['rssi'])),
                   battery_low=data['battery'] != 'normal',
                   reading=Reading.from_dict(data))
