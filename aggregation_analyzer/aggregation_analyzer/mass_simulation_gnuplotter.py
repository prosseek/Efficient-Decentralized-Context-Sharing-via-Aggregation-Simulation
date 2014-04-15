import os
import distutils.spawn
import pprint
import cPickle

from aggregation_simulator.utils_configuration import *
from mass_simulation_analyzer import MassSimulationAnalyzer
from subprocess import Popen, call

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

class MassSimulationGnuplotter(object):
    def __init__(self, network_reports_dir, use_cache=True):

        test_name = os.path.basename(network_reports_dir)
        cache_img = get_configuration("config.cfg","TestDirectory","cache_dir") + os.sep + test_name + ".img"
        dirname = os.path.dirname(cache_img)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if not os.path.exists(cache_img) or not use_cache:
            v = MassSimulationAnalyzer(network_reports_dir)
            reports = v.run()
            with open(cache_img, "w") as f:
                cPickle.dump(reports, f)
                f.close()
        else:
            # os.path.exists and not ignore_cache
            with open(cache_img, "r") as f:
                reports = cPickle.load(f)
                #result = cPickle.load(f.read())
                f.close()

        self.reports = reports

    def get_reports(self):
        print self.reports

    def get_data(self, measurement):
        pprint.pprint(self.reports)

        r = self.reports[measurement]
        keys = sorted(r)

        result = []
        for key in keys:
            values = r[key]
            # 'size': ([81, 70, 11], [81, 70, 11]),
            if measurement == "size":
                #print values
                val1 = values[0][0][0]
                val2 = values[1][0][0]
            elif measurement in ['speed','cohorts']:
                val1 = values[0]
                val2 = values[1]
            else:
                val1 = values[0][0]
                val2 = values[1][0]
            result.append("%d %5.2f %5.2f" % (key, val1, val2))

        return "\n".join(result)

    def get_code(self, config):
        file_path = config["file_path"]

        lines = ["set terminal pngcairo font 'DroidSerif'"]
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

        if ylabel in ["size"]:
            lines.append(r'set y2label "reduction ratio (%)"')
            lines.append(r'unset logscale y2')
            lines.append(r'set ytics nomirror')
            lines.append(r'set y2tics')
            lines.append(r'set logscale y')
            plot = r'plot "{data_file_path}" using 1:2 title "singles" w lp, "" using 1:3 title "aggregates" w lp, ""  using 1:(($2-$3)/$2)*100 axis x1y2 title "reduction ratio" w lp'.format(data_file_path=data_file_path)

        else:
            plot = r'plot "{data_file_path}" using 1:2 title "singles" w lp, "{data_file_path}" using 1:3 title "aggregates" w lp '.format(data_file_path=data_file_path)
        lines.append(plot)
        return "\n".join(lines)

    def write(self, config):
        measurement = config["measurement"]
        #control_variable = config["control_variable"]
        data = self.get_data(measurement)

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


def plot(measure, network_reports_dir, gnuplot_dir):
    v = MassSimulationGnuplotter(network_reports_dir)
    gnuplot_data_dir = gnuplot_dir + os.sep + os.path.basename(network_reports_dir)
    if not os.path.exists(gnuplot_data_dir):
        os.makedirs(gnuplot_data_dir)
    gnuplot_data =  gnuplot_data_dir + os.sep + "%s.txt" % (measure)

    title = (" ".join(os.path.basename(network_reports_dir).split('_')[0:-1])).capitalize()
    xlabel = 'node size'
    ylabel = ('%s %s (%%)' % tuple(measure.split('_'))) if measure.endswith("rate") else measure
    config = {
        "file_path": gnuplot_data,
        'measurement':measure,
        'xlabel':xlabel,
        'ylabel':ylabel,
        'title':title,
        'display':True
    }
    v.execute(config)

def various_plots(network_reports_dir, gnuplot_dir):
    plot('size', network_reports_dir, gnuplot_dir)
    plot('identification_rate', network_reports_dir, gnuplot_dir)
    plot('speed', network_reports_dir, gnuplot_dir)
    plot('cohorts',network_reports_dir,gnuplot_dir)

if __name__ == "__main__":
    network_reports_dir = "/Users/smcho/tmp/reports/dense_meshes_dir"
    gnuplot_dir = "/Users/smcho/tmp/imgs/gnuplot/mass"
    various_plots(network_reports_dir, gnuplot_dir)
    # network_reports_dir = "/Users/smcho/tmp/reports/dense_trees_dir"
    # various_plots(network_reports_dir, gnuplot_dir)
    network_reports_dir = "/Users/smcho/tmp/reports/light_meshes_dir"
    various_plots(network_reports_dir, gnuplot_dir)
    network_reports_dir = "/Users/smcho/tmp/reports/light_trees_dir"
    various_plots(network_reports_dir, gnuplot_dir)
