import os
import shutil
import glob
import argparse
import numpy as np
import pylab as pl
from collections import Counter

class Analyze_Output():
    """ Yo """
    def __init__(self, output):
        """
        """
        self.output = output
        self.input_header = [
            'Processor', 'Number of Processor',
            'Function', 'Time Input (s)', 'Time Output (s)',
            'Memory Input (Mb)', 'Memory Output (Mb)',
            'Area']

        self.output_header = [
            'Area', 'Number of calls', 'Time spent (s)', 'Time (s)',
            'Memory consumption (Mb)']

        if not os.path.isdir(self.output):
            os.makedirs(self.output)
            fns = glob.glob('*.log')
            for fn in fns:
                shutil.move(fn, self.output)

        self.full_stats = self.full_stats_per_processors()
        self.dic_time_per_processor = self.time_per_processor(self.full_stats)
        self.dic_memory_per_processor = self.memory_per_processor(self.full_stats)

    def full_stats_per_processors(self):
        """
        """
        fns = glob.glob(os.path.join(self.output, '*.log'))
        dic = {}
        for fn in fns:
            data = np.loadtxt(fn, dtype=str, delimiter='/').T
            proc = data[0][1]
            dic[proc] = {}
            for pos, k in enumerate(self.input_header):
                dic[proc][k] = data[pos]
        return dic

    def time_per_processor(self, input_dic):
        """
        """
        output_dic = {k:{} for k in input_dic.keys()}
        for proc in input_dic.keys():
            ## Dictionary containing the time spent
            ## per call for all areas, and total number of calls.
            output_dic[proc] = {
                k:{i:j for i,j in zip(
                        ['Number of calls', 'Time spent (s)'], [0, []])}
                        for k in np.unique(input_dic[proc]['Area'])}

            ## Group all times spent per area
            for pos, area in enumerate(input_dic[proc]['Area']):
                output_dic[proc][area]['Number of calls'] += 1

                time_out = float(input_dic[proc]['Time Output (s)'][pos])
                time_in = float(input_dic[proc]['Time Input (s)'][pos])
                output_dic[proc][area]['Time spent (s)'].append(
                    time_out - time_in)

            ## Sum time values per area
            for pos, area in enumerate(output_dic[proc].keys()):
                output_dic[proc][area]['Time spent (s)'] = np.sum(
                    output_dic[proc][area]['Time spent (s)'])

            ## Compute the total amount of time between
            ## the first call and the last call
            total_time_recorded = 0.
            for pos, area in enumerate(output_dic[proc].keys()):
                total_time_recorded += output_dic[
                    proc][area]['Time spent (s)']

            ## Find the leftover: total_time - total_time_recorded
            output_dic[proc]['Others'] = {
                'Time spent (s)': 0., 'Number of calls': 1.}
            output_dic[proc]['Others']['Time spent (s)'] = float(
                input_dic[proc]['Time Output (s)'][-1]) - float(
                    input_dic[proc]['Time Input (s)'][0]) - total_time_recorded

        return output_dic

    def memory_per_processor(self, input_dic):
        """
        """
        output_dic = {k:{} for k in input_dic.keys()}
        for proc in input_dic.keys():
            ## Dictionary containing the memory consumption
            ## per call for all areas, as a function of time
            output_dic[proc] = {i:j for i,j in zip(
                        ['Function',
                        'Area',
                        'Memory consumption (Mb)',
                        'Time (s)'], [[], [], [], []])}

            ## Group all times spent per area
            for pos, function in enumerate(input_dic[proc]['Function']):
                output_dic[proc]['Function'].append(function + ' (in)')
                output_dic[proc]['Function'].append(function + ' (out)')
                output_dic[proc]['Area'].append(input_dic[proc]['Area'][pos])
                output_dic[proc]['Area'].append(input_dic[proc]['Area'][pos])

                output_dic[proc]['Memory consumption (Mb)'].append(
                    float(input_dic[proc]['Memory Input (Mb)'][pos]))
                output_dic[proc]['Memory consumption (Mb)'].append(
                    float(input_dic[proc]['Memory Output (Mb)'][pos]))

                output_dic[proc]['Time (s)'].append(
                    float(input_dic[proc]['Time Input (s)'][pos]))
                output_dic[proc]['Time (s)'].append(
                    float(input_dic[proc]['Time Output (s)'][pos]))

        return output_dic


class Plot_Data():
    def __init__(self, data_time, data_memory, output):
        """
        """
        self.data_time = data_time
        self.data_memory = data_memory
        self.output = output

    def format_data_piechart_js_perproc(
        self, areas=['Time spent (s)', 'Average memory (Mb)'],
        div='MyDiv', proc='0'):
        """

        """
        prop_cycle = pl.rcParams['axes.prop_cycle']
        colors = prop_cycle.by_key()['color']

        ## Time plot
        js = ''
        js += 'var data1 = {'
        js += 'values: ['
        for k in self.data_time[proc].keys():
            js += '%.3f, ' % self.data_time[proc][k]['Time spent (s)']
        js += '],'
        js += 'labels: ['
        for k in self.data_time[proc].keys():
            js += '"%s", ' % k
        js += '],'
        js += 'marker: { colors: ['
        for pos_k, k in enumerate(self.data_time[proc].keys()):
            js += '"%s", ' % colors[pos_k]
        js += ']},'
        js += 'domain: {'
        js += 'x: [%.2f, %.2f],' % (0.0, 0.4)
        js += 'y: [0, 1.0],'
        js += '},'
        js += "type: 'pie',"
        js += "hoverinfo: 'label+percent+value',"
        js += 'opacity: 0.9,'
        js += 'hole: 0.2,'
        js += 'pull: 0.05};'
        js += '\n'

        ## Memory consumption plot
        js += 'var data2 = {'
        js += "type: 'scatter',"
        js += "mode: 'lines+markers',"
        js += 'x: ['
        for k in self.data_memory[proc]['Time (s)']:
            js += '%.3f, ' % (k - self.data_memory[proc]['Time (s)'][0])
        js += '],'
        js += 'y: ['
        for k in self.data_memory[proc]['Memory consumption (Mb)']:
            js += '%.3f, ' % k
        js += '],'
        js += 'text: ['
        for pos_k, k in enumerate(
            self.data_memory[proc]['Function']):
            js += '"%s (%s)", ' % (k, self.data_memory[proc]['Area'][pos_k])
        js += '],'
        js += 'line: { color: "%s"},' % colors[-1]
        js += "name: 'Memory consumption (Mb)',"
        js += "xaxis: 'x2',"
        js += "yaxis: 'y2',"
        js += "hoverinfo: 'text+x+y'"
        js += '};\n'

        js += 'var data = [data1, data2];'

        js += 'var layout = {'
        js += 'title: "Processor %d / %d",' % (
            int(proc) + 1, len(self.data_time.keys()))
        js += 'xaxis: {domain: [0.0, 0.4],'
        js += 'zeroline: false, '
        js += 'showticklabels: false, '
        js += 'showgrid: false, '
        js += 'showline: false},'
        js += 'yaxis: {domain: [0.0, 1.0], zeroline: false, showticklabels: false, showgrid: false, showline: false},'
        js += "yaxis2: {anchor: 'x2', title: 'Memory consumption (Mb)'},"
        js += 'xaxis2: {domain: [0.6, 1.0], title: "Time (s)"},'
        js += 'height: 450,'
        js += 'width: 1200};'
        js += '\n'
        js += "Plotly.newPlot('%s', data, layout);" % div

        return js

    def pie_chart(self):
        divs = ''
        js = ''
        sorted_proc = np.sort(self.data_time.keys())
        for proc in sorted_proc:
            js += self.format_data_piechart_js_perproc(
                areas=['Time spent (s)', 'Average memory (Mb)'],
                div='proc%s' % proc,
                proc=proc)
            divs += '<div id="proc%s"' % proc
            divs += 'style="width: 950px; height: 450px;"></div>'
        with open(os.path.join(self.output, 'summary_allproc.html'), 'a') as f:
            f.write("""
            <html>
                <head>
                    <!-- Plotly.js -->
                    <script type="text/javascript" src="https://cdn.plot.ly/plotly-1.27.0.min.js"></script>
                </head>
                <body>
                    %s

                    <script>
                    %s
                    </script>

                </body>
            </html>""" % (divs, js))

def addargs(parser):
    ''' Parse command line arguments '''
    parser.add_argument(
        '--output', dest='output',
        help='Folder to store outputs', required=True)

def grabargs(args_param=None):
    ''' Parse command line arguments '''
    parser = argparse.ArgumentParser(description='Analyze logs from ProfileIt')
    addargs(parser)
    args = parser.parse_args(args_param)
    return args

def main():
    args_param = None
    args = grabargs(args_param)

    processor_data = Analyze_Output(args.output)

    plotter = Plot_Data(
        processor_data.dic_time_per_processor,
        processor_data.dic_memory_per_processor,
        processor_data.output)
    plotter.pie_chart()

if __name__ == "__main__":
        main()

# from plotlyjs import *


# def analyze_file(fname, port):
#     with open(fname, 'r') as f:
#         lines = [json.loads(line) for line in f]
#     macs_to_add = []
#     for data in lines:
#         for c in data['cellphones']:
#             if c['rssi'] > -80 and c['mac'] not in macs_to_add:
#                 macs_to_add.append(c['mac'])
#     mac_data = {mac: {'y': []} for mac in macs_to_add}
#     num = {'x': [], 'y': []}
#     for data in lines:
#         rssi = {}
#         for mac in macs_to_add:
#             rssi[mac] = -100
#             for c in data['cellphones']:
#                 if c['mac'] in rssi:
#                     rssi[c['mac']] = c['rssi']
#         for mac in mac_data:
#             mac_data[mac]['y'].append(str(rssi[mac] + 100))
#         num['x'].append("'" + datetime.datetime.fromtimestamp(
#             data['time']).isoformat().split('.')[0].replace('T', ' ') + "'")
#         num['y'].append(str(len(data['cellphones'])))
#
#     mac_names = copy.deepcopy(macs_to_add)
#     for i, mac in enumerate(mac_names):
#         mac_names[i] = 'mac' + mac.replace(':', '')
#
#     # remove pings
#     for mac in mac_data:
#         for i, y in enumerate(mac_data[mac]['y']):
#             if y == "0" and i > 2:
#                 if mac_data[mac]['y'][i - 3] == "0" and (mac_data[mac]['y'][i - 1] != "0" or mac_data[mac]['y'][i - 2] != "0"):
#                     mac_data[mac]['y'][i - 1] = "0"
#                     mac_data[mac]['y'][i - 2] = "0"
#
#     js = ""
#     js += ('timex = [%s]' % ', '.join(num['x']))
#     for i, mac in enumerate(macs_to_add):
#         js += ('\nvar %s = {' % mac_names[i])
#         js += ('\n  x: timex,')
#         js += ('\n  y: [%s],' % ', '.join(mac_data[mac]['y']))
#         js += ("\n name: '%s', mode: 'lines', type:'scatter' };\n\n" % mac)
#     js += ('\n\nvar data = [%s];' % ', '.join(mac_names))
#     js += ("\n\nPlotly.newPlot('myDiv',data,layout2);")
#     js += ('\nvar num_cellphones = {')
#     js += ('\n  x: timex,')
#     js += ('\n  y: [%s],' % ', '.join(num['y']))
#     js += ("\n name: 'N', mode: 'lines', type:'scatter' };\n\n")
#     js += ("\n\nPlotly.newPlot('myDiv2',[num_cellphones],layout1);")
#
#     with open('index.html', 'w') as f:
#         f.write("""<html><head>
#         <!-- Plotly.js -->
#         <script type="text/javascript" src="https://cdn.plot.ly/plotly-1.27.0.min.js"></script>
#     </head>
#     <body>
#         <div id="myDiv2" style="width: 950px; height: 350px;">
#             <!-- Plotly chart will be drawn inside this DIV -->
#         </div>
#         <div id="myDiv" style="width: 950px; height: 350px;">
#             <!-- Plotly chart will be drawn inside this DIV -->
#         </div>
#         <script>
# var layout1 = {
#   title: 'Total Count',
#   xaxis: {
#     title: 'date',
#     titlefont: {
#       family: 'Courier New, monospace',
#       size: 18,
#       color: '#7f7f7f'
#     }
#   },
#   yaxis: {
#     title: 'number',
#     titlefont: {
#       family: 'Courier New, monospace',
#       size: 18,
#       color: '#7f7f7f'
#     }
#   }
# };
# var layout2 = {
#   title: 'Individual traces',
#   xaxis: {
#     title: 'date',
#     titlefont: {
#       family: 'Courier New, monospace',
#       size: 18,
#       color: '#7f7f7f'
#     }
#   },
#   yaxis: {
#     title: 'rssi',
#     titlefont: {
#       family: 'Courier New, monospace',
#       size: 18,
#       color: '#7f7f7f'
#     }
#   }
# };
#     %s
#         </script>
#     </body></html>""" % (js))
#     print("Wrote index.html")
#     print("Open browser to http://localhost:" + str(port))
#     print("Type Ctl+C to exit")
#     if sys.version_info >= (3, 0):
#         # Python 3 code in this block
#         from http.server import HTTPServer, SimpleHTTPRequestHandler
#         httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
#         httpd.serve_forever()
#     else:
#         # Python 2 code in this block
#         import SimpleHTTPServer
#         import SocketServer
#         httpd = SocketServer.TCPServer(("", port), SimpleHTTPServer.SimpleHTTPRequestHandler)
# httpd.serve_forever()
