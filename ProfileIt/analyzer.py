import os
import shutil
import glob
import argparse

import numpy as np
import pylab as pl

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

    def format_data_piechart_js_allproc(self, div='MyDiv'):
        """

        """
        prop_cycle = pl.rcParams['axes.prop_cycle']
        colors = prop_cycle.by_key()['color']

        procs = self.data_time.keys()
        data_time_tot = {i:0 for i in procs}
        for proc in procs:
            for k in self.data_time[proc].keys():
                data_time_tot[proc] += self.data_time[proc][k]['Time spent (s)']

        ## Time plot
        js = ''
        js += 'var data1 = {'
        js += 'values: ['
        for proc in procs:
            js += '%.3f, ' % data_time_tot[proc]
        js += '],'
        js += 'labels: ['
        for proc in procs:
            js += '"Time (s): proc %s", ' % proc
        js += '],'
        js += 'marker: { colors: ['
        for pos_proc, proc in enumerate(procs):
            js += '"%s", ' % colors[int(proc)]
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
        for proc in procs:
            js += 'var data_proc%s = ' % proc
            js += '{'
            js += "type: 'scatter',"
            js += "mode: 'lines',"
            js += 'x: ['
            for k in self.data_memory[proc]['Time (s)']:
                js += '%.3f, ' % (k - self.data_memory[proc]['Time (s)'][0])
            js += '],'
            js += 'y: ['
            for k in self.data_memory[proc]['Memory consumption (Mb)']:
                js += '%.3f, ' % k
            js += '],'
            # js += 'text: ['
            # for pos_k, k in enumerate(
            #     self.data_memory[proc]['Function']):
            #     js += '"%s (%s)", ' % (k, self.data_memory[proc]['Area'][pos_k])
            # js += '],'
            js += 'line: { color: "%s"},' % colors[int(proc)]
            js += "name: 'Memory (Mb): proc %s'," % proc
            js += "xaxis: 'x2',"
            js += "yaxis: 'y2',"
            js += "hoverinfo: 'name+x+y'"
            js += '};\n'

        # js += 'var data = [data1, data2];'
        js += 'var data = [data1, '
        for proc in procs:
            js += 'data_proc%s,' % proc
        js += '];'

        js += 'var layout = {'
        js += 'title: "Summary all processors (%s)",' % (
            len(self.data_time.keys()))
        js += 'xaxis: {domain: [0.0, 0.4],'
        js += 'zeroline: false, '
        js += 'showticklabels: false, '
        js += 'showgrid: false, '
        js += 'showline: false},'
        js += 'yaxis: {domain: [0.0, 1.0], title: "Time spent (s)",'
        js += 'zeroline: false, '
        js += 'showticklabels: false, '
        js += 'showgrid: false, '
        js += 'showline: false},'
        js += "yaxis2: {anchor: 'x2', title: 'Memory consumption (Mb)'},"
        js += 'xaxis2: {domain: [0.6, 1.0], title: "Time (s)"},'
        js += 'height: 450,'
        js += 'width: 1200};'
        js += '\n'
        js += "Plotly.newPlot('%s', data, layout);" % div

        return js

    def format_data_piechart_js_perproc(self, div='MyDiv', proc='0'):
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
        js += 'title: "Processor %d",' % (int(proc))
        js += 'xaxis: {domain: [0.0, 0.4],'
        js += 'zeroline: false, '
        js += 'showticklabels: false, '
        js += 'showgrid: false, '
        js += 'showline: false},'
        js += 'yaxis: {domain: [0.0, 1.0], title: "Time spent (s)",'
        js += 'zeroline: false, '
        js += 'showticklabels: false, '
        js += 'showgrid: false, '
        js += 'showline: false},'
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
        js += self.format_data_piechart_js_allproc(div='allprocs')
        divs += '<div id="allprocs"'
        divs += 'style="width: 950px; height: 450px;"></div>'
        sorted_proc = np.sort(self.data_time.keys())
        for proc in sorted_proc:
            js += self.format_data_piechart_js_perproc(
                div='proc%s' % proc, proc=proc)
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

def time_units(val, output='s'):
    """
    Change units for time. By default time is measured in seconds.
    Available options: hour, min, s (default), ms, us.

    Parameters
    -----------
        * val: float, input time value in seconds.
        * output: string, desired units.
            Available options: hour, min, s (default), ms, us.
    """
    units = {'hour': 1./3600,'min': 1./60, 's': 1, 'ms': 1e3, 'us': 1e6}

    return val * units(output)

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
