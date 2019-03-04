import os
import rrdtool
from netatmo import formatter
import logging

class Graph:
    source = None
    graph_dir = os.getenv('GRAPH_DIR', '.')

    def __init__(self, source):
        self.source = source

    def generate_all(self, params):

        for data_source in self.get_data_sources():
            output = self.graph_dir + os.path.sep + os.path.splitext(os.path.basename(self.source))[0] + '_' + data_source.lower() + ".png"
            symbol = formatter.format_symbol(data_source).replace('%', '%%')

            logging.info("Generating graph for %s from %s in %s" % (data_source, os.path.basename(self.source), output))
            rrdtool.graph(
                output,
                '--width', str(params.width),
                '--height', str(params.height),
                '--imgformat', 'PNG',
                '--slope-mode',
                '--start', str(params.start),
                '--end', str(params.end),
                '--font', 'DEFAULT:7:',
                '--title', self.get_title(data_source, symbol),
                '--vertical-label', formatter.format_name(data_source) + ' (' + symbol.replace('%%', '%') + ')',
                '--alt-y-grid',
                '--rigid',
                '--units-exponent', '0',
                'DEF:data_source=' + self.source + ':' + data_source + ':MAX',
                'LINE1:data_source#0000FF:' + data_source,
                'GPRINT:data_source:LAST:"Cur\: %5.2lf ' + symbol,
                'GPRINT:data_source:AVERAGE:"Avg\: %5.2lf ' + symbol,
                'GPRINT:data_source:MAX:"Max\: %5.2lf ' + symbol,
                'GPRINT:data_source:MIN:"Min\: %5.2lf ' + symbol + '\t\t\t'
            )

    def get_data_sources(self):
        logging.info("Extracing data sources from %s..." % os.path.basename(self.source))
        data_sources = []

        for key in rrdtool.info(self.source).keys():
            try:
                if key[:3] == 'ds[' and key.index(']', 3):
                    data_source = key[3:key.index(']', 3)]
                    if not data_source in data_sources:
                        data_sources.append(data_source)
            except ValueError:
                pass

        return data_sources

    def get_title(self, data_source, symbol):
        return os.path.splitext(os.path.basename(self.source.title()))[0] + ' ' + data_source.title()
