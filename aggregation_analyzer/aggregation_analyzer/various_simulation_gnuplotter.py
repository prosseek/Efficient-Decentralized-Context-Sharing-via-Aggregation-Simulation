import os
import distutils.spawn
from various_simulation_analyzer import VariousSimulationAnalyzer
from subprocess import Popen, call
import pprint

GNUPLOT=distutils.spawn.find_executable('gnuplot')

"""
{'disconnection_rate': {'cohorst': {10: ([0.0, 0, 0], [2.2375, 3, 0]),
                                    20: ([0.0, 0, 0], [1.975, 1, 0]),
                                    ...
                                    80: ([0.0, 0, 0], [0.1, 0, 0]),
                                    90: ([0.0, 0, 0], [0.0, 0, 0])},
                        'identification_rate': {10: ([97.1875,
                                                      7,
                                                      8,
                                                      97.1875,
                                                      7,
                                                      8],
                                                     [97.8125,
                                                      7,
                                                      8,
                                                      54.6875,
                                                      3,
                                                      8]),
                                                20: ([95.9375,
                                                        ...
                                                      8])},
                        'size': {10: (([54, 54, 0], [54, 54, 0]),
                                      ([38, 14, 24], [38, 14, 24])),
                                 20: (([53, 53, 0], [53, 53, 0]),
                                      ([36, 14, 22], [36, 14, 22])),
                                 ...
                                 90: (([2, 2, 0], [2, 2, 0]),
                                      ([2, 2, 0], [2, 2, 0]))},
                        'speed': {10: ([5.2, 4, 6], [5.075, 4, 5]),
                                  20: ([5.325, 4, 6], [4.725, 3, 6]),
                                  ...
                                  90: ([1.3, 1, 2], [1.3, 1, 2])}},
"""

class VariousSimulationGnuplotter(object):
    def __init__(self, network_reports_dir):
        v = VariousSimulationAnalyzer(network_reports_dir)
        self.reports = v.run()

    def get_reports(self):
        print self.reports

    def get_data(self, control_variable, measurement):
        pprint.pprint(self.reports)

        r = self.reports[control_variable][measurement]
        keys = sorted(r)

        result = []
        for key in keys:
            values = r[key]
            # 'size': ([81, 70, 11], [81, 70, 11]),
            if measurement == "size":
                print values
                val1 = values[0][0][0]
                val2 = values[1][0][0]
            else:
                val1 = values[0][0]
                val2 = values[1][0]
            result.append("%d %5.2f %5.2f" % (key, val1, val2))

        return "\n".join(result)

    def get_code(self, config):
        lines = ["set terminal pngcairo"]
        png_name = config.get("png_name", config["file_path"] + ".png")
        config["png_name"] = png_name

        lines.append(r'set output "%s"' % png_name)
        xlabel = config.get("xlabel", "x")
        lines.append(r'set xlabel "%s"' % xlabel)
        ylabel = config.get("ylabel", "y")
        lines.append(r'set ylabel "%s"' % ylabel)
        title = config.get("title", "title")
        lines.append(r'set title "%s"' % title)
        data_file_path = config["data_file_path"]
        plot = r'plot "{data_file_path}" using 1:2 title "singles", "{data_file_path}" using 1:3 title "aggregates"'.format(data_file_path=data_file_path)
        lines.append(plot)
        return "\n".join(lines)

    def write(self, config):
        measurement = config["measurement"]
        control_variable = config["control_variable"]
        data = self.get_data(control_variable, measurement)

        file_path = config["file_path"]
        data_file_path = file_path + ".data"
        with open(data_file_path, "w") as f:
            f.write(data)
        config["data_file_path"] = data_file_path

        code = self.get_code(config)

        with open(file_path, "w") as f:
            f.write(code)

    def execute(self, config):
        self.write(config)
        my_env = os.environ
        my_env["GDFONTPATH"] = os.path.join(my_env['HOME'], 'fonts')
        p = Popen([GNUPLOT, config["file_path"]], shell=False, env=my_env)
        p.communicate()
        png_file_path = config["png_name"]

        if config.get('display', True):
            p = Popen(['open','-a','Preview','%s' % png_file_path])
            p.communicate()


def plot(control, measure, network_reports_dir, gnuplot_dir):
    v = VariousSimulationGnuplotter(network_reports_dir)
    gnuplot_data_dir = gnuplot_dir + os.sep + os.path.basename(network_reports_dir)
    if not os.path.exists(gnuplot_data_dir):
        os.makedirs(gnuplot_data_dir)
    gnuplot_data =  gnuplot_data_dir + os.sep + "%s_%s.txt" % (control, measure)

    xlabel = ('%s %s (%%)' % tuple(control.split('_'))) if control.endswith("rate") else control
    ylabel = ('%s %s (%%)' % tuple(measure.split('_'))) if measure.endswith("rate") else measure
    config = {
        "file_path": gnuplot_data,
        'control_variable':control,
        'measurement':measure,
        'xlabel':xlabel,
        'ylabel':ylabel,
        'title':'',
        'display':True
    }
    v.execute(config)

def various_plots(network_reports_dir, gnuplot_dir):
    plot('drop_rate', 'size', network_reports_dir, gnuplot_dir)
    plot('disconnection_rate', 'size', network_reports_dir, gnuplot_dir)
    plot('drop_rate', 'identification_rate', network_reports_dir, gnuplot_dir)
    plot('disconnection_rate', 'identification_rate', network_reports_dir, gnuplot_dir)

if __name__ == "__main__":
    network_reports_dir = "/Users/smcho/tmp/reports/test_network1"
    gnuplot_dir = "/Users/smcho/tmp/imgs/gnuplot"
    various_plots(network_reports_dir, gnuplot_dir)
