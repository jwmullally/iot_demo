class DeviceSensorSample(object):
    # Poor man's serialization. This should be done with schemas
    def __init__(self, serial, sensors):
        self.serial = int(serial)
        self.sensors = {str(k): float(v) for k,v in dict(sensors).items()}

    @classmethod
    def from_dict(cls, data):
        data = data.copy()
        obj = cls(
                serial = data.pop('serial'),
                sensors = data.pop('sensors'))
        if data:
            raise ValueError('Unknown keys: {}'.format(data.keys()))
        return obj

    def to_prometheus_pushmetrics(self):
        lines = []
        for k,v in self.sensors.items():
            lines.append('iot_device{{serial="{}", sensor="{}"}} {}'.format(self.serial, k, v))
        return '\n'.join(lines)+'\n'
