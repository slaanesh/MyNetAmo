import rrdtool
import logging
import os
from pathlib import Path

def add_new_data(name, data_points, timestamp):
    rrd = DataCollector(name, data_points.keys(), timestamp)
    rrd.add(data_points, timestamp)

class DataCollector:
    name = None
    keys = None
    data_dir = os.getenv('DATA_DIR', './')
    rrd_file = None
    step = 300
    heartbeat = 1800

    def __init__(self, name, data_keys, timestamp):
        self.name = name.replace(' ', '_').lower()
        self.keys = data_keys

        self.rrd_file = Path(self.data_dir + os.sep + self.get_name())

        if not self.rrd_file.exists():
            self.create(timestamp)

    def get_name(self):
        return self.name + '.rrd'

    def get_ds_name(self, data_name):
        return data_name.replace(' ', '_')[:19]

    def create(self, timestamp):
        logging.info("Creating RRD file into %s..." % str(self.rrd_file))

        data_sources = []

        for source in self.keys:
            ds_name = self.get_ds_name(source)
            data_sources.append('DS:' + ds_name + ':GAUGE:' + str(self.heartbeat) + ':U:U')

        rrdtool.create(
            str(self.rrd_file),
            '--start', str(timestamp - self.step), # so we can insert our first data right away
            '--step', str(self.step),
            data_sources,
            'RRA:AVERAGE:0.5:1:1440',
            'RRA:MIN:0.5:1:1440',
            'RRA:MAX:0.5:1:1440',
            'RRA:LAST:0.5:1:1440'
        )

    def add(self, data_points, timestamp):
        last_update = rrdtool.last(str(self.rrd_file))

        if timestamp < last_update + self.step:
            logging.info("Ignoring data point, last update was last then %d minutes ago" % (self.step / 60))
            return

        logging.info("Updating RRD file...")
        rrdtool.update(
            str(self.rrd_file),
            '-t', ':'.join(self.get_ds_name(x) for x in data_points.keys()),
            str(timestamp) + ':' + ':'.join(str(x) for x in data_points.values())
        )
