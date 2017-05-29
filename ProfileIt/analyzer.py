import os
import shutil
import glob
import argparse
import numpy as np
from collections import Counter

class Analyze_Output():
	""" Yo """
	def __init__(self, output):
		"""
		"""
		self.output = output
		self.input_header = [
			'Processor', 'Number of Processor',
			'Function', 'Time spent (s)',
			'Memory Input (Mb)', 'Memory Output (Mb)',
			'Area']

		self.output_header = [
			'Area', 'Number of calls', 'Time spent (s)', 'Average memory (Mb)']

		if not os.path.isdir(self.output):
			os.makedirs(self.output)
			fns = glob.glob('*.log')
			for fn in fns:
				shutil.move(fn, self.output)

		self.full_stats = self.full_stats_all_processors()
		self.averaged_stats = self.averaged_stats_all_processors(
			self.full_stats)

	def full_stats_all_processors(self):
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

	def averaged_stats_all_processors(self, input_dic):
		"""
		"""
		output_dic = {k:{} for k in input_dic.keys()}
		for proc in input_dic.keys():
			output_dic[proc] = {
				k:{
					i:j for i,j in zip(self.output_header[1:],[0, [], []])}
				for k in np.unique(input_dic[proc]['Area'])}

			for pos, area in enumerate(input_dic[proc]['Area']):
				output_dic[proc][area]['Number of calls'] += 1
				output_dic[proc][area]['Time spent (s)'].append(
					float(input_dic[proc]['Time spent (s)'][pos]))
				output_dic[proc][area]['Average memory (Mb)'].append(
					float(input_dic[proc]['Memory Output (Mb)'][pos]) -
					float(input_dic[proc]['Memory Input (Mb)'][pos]))

			for pos, area in enumerate(output_dic[proc].keys()):
				output_dic[proc][area]['Time spent (s)'] = np.sum(
					output_dic[proc][area]['Time spent (s)'])
				output_dic[proc][area]['Average memory (Mb)'] = np.mean(
					output_dic[proc][area]['Average memory (Mb)'])

		return output_dic


class Plot_Data():
	def __init__(self, data, output):
		"""
		"""
		self.data = data
		self.output = output

	def dic2json():
		"""
		"""
		pass

	def output_json():
		"""
		"""
		pass

	def pie_chart(self):
		proc = '1'
		js = []
		js.append('Time spent (s)')
		for k in self.data[proc].keys():
			js.append(self.data[proc][k]['Time spent (s)'])
			js.append(k)
		js.append('Average memory (Mb)')
		for k in self.data[proc].keys():
			js.append(self.data[proc][k]['Average memory (Mb)'])
			js.append(k)

		with open(os.path.join('./', 'index.html'), 'w') as f:
			f.write("""
			<html>
				<head>
			        <!-- Plotly.js -->
			        <script type="text/javascript" src="https://cdn.plot.ly/plotly-1.27.0.min.js"></script>
			    </head>
				<body>
					<div id="myDiv" style="width: 350px; height: 350px;">
						<!-- Plotly chart will be drawn inside this DIV -->
					</div>

					<div id="myDiv2" style="width: 350px; height: 350px;">
						<!-- Plotly chart will be drawn inside this DIV -->
					</div>

					<div id="myDiv3" style="width: 350px; height: 350px;">
						<!-- Plotly chart will be drawn inside this DIV -->
					</div>

					<script>
						var data = [{
							values: [%.3f, %.3f],
							labels: ["%s", "%s"],
							type: 'pie',
							opacity: 0.9,
							domain: {
								x: [0., 0.48],
								y: [0., 1.0]}
							},
							{
							values: [10,4],
							labels: ["toto", "titi"],
							type: 'pie',
							domain: {
								x: [0.48, 1.0],
								y: [0., 1.0]}}];

						var layout = {
							title: "%s",
							height: 500,
							width: 500};

						Plotly.newPlot('myDiv', data, layout);

						var data = [{
							values: [%.3f, %.3f],
							labels: ["%s", "%s"],
							type: 'pie'}];

						var layout = {
							title: "%s",
							height: 500,
							width: 500};

						Plotly.newPlot('myDiv2', data, layout);

						var data = [{
							values: [10, 40],
							labels: ["toot", "titi"],
							type: 'pie'}];

						var layout = {
							title: "test",
							height: 500,
							width: 500};

						Plotly.newPlot('myDiv3', data, layout);
					</script>
				</body>
			</html>""" % (
				js[1], js[3], js[2], js[4], js[0],
				js[6], js[8], js[7], js[9], js[5],))

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

	plotter = Plot_Data(processor_data.averaged_stats, processor_data.output)
	plotter.pie_chart()
	import SimpleHTTPServer
	import SocketServer
	httpd = SocketServer.TCPServer(
		("", 8001), SimpleHTTPServer.SimpleHTTPRequestHandler)
	httpd.serve_forever()


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
