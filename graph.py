#!/usr/bin/env python3

import os
import logging
from glob import glob
from rrd import graph
import argparse

class App:
    args = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        parser = argparse.ArgumentParser()

        # see https://oss.oetiker.ch/rrdtool/doc/rrdfetch.en.html#AT-STYLE_TIME_SPECIFICATION for more information regarding ways of expressing the time
        parser.add_argument('--start', type=int, default=-86400, help='Specify the starting time of the graph (expressed in seconds from end)')
        parser.add_argument('--end', type=str, default='now', help='Specify the end time of the graph (can be expressed in a natural way)')

        parser.add_argument('--width', type=int, default=785, help='Width of the graph')
        parser.add_argument('--height', type=int, default=120, help='Height of the graph')
        self.args = parser.parse_args()

    def generate_all(self):
        logging.info("Generating all graphs")
        for rrdfile in glob(os.getenv('DATA_DIR', '.') + os.path.sep + '*.rrd'):
            gr = graph.Graph(rrdfile)
            gr.generate_all(self.args)

if __name__ == "__main__":
    app = App()
    app.generate_all()
