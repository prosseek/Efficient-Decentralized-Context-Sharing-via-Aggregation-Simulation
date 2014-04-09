"""Analysis of simulation and genration of gnuplot file

"""
from gnuplotter import Gnuplotter

from read_reports import *
from utils_location import get_img_report_dir
from get_processed_information import GetProcessedInformation
from get_information import GetInformation

class GenerateGifs(object):
    def __init__(self, dir_name = "tmp"):
        self.dir_name = dir_name

    def generate_diff_gif(self, ref_value, value, gif_name, config=None):
        """Generate one giff given values as a list, the gif_name is the target file path for the gif geneerated
        >>> config = {"x":7, "y":8, "min_val":-1, "max_val":1}
        >>> ref_value = [23.64, 23.50, 23.28, 23.48, 22.86, 22.86, 22.73, 22.50, 22.65, 22.50, 21.30, 21.30, 21.30, 22.49, 23.39, 23.39, 23.39, 23.39, 23.39, 23.99, 24.24, 24.53, 24.93, 24.53, 24.93, 25.25, 25.25, 25.10, 25.10, 25.10, 24.52, 24.52, 24.21, 24.52, 24.92, 24.78, 24.78, 24.78, 24.78, 25.10, 25.25, 24.93, 25.10, 25.25, 25.25, 24.93, 24.93, 24.53, 24.24, 24.13, 24.13, 24.24, 22.65, 22.65]
        >>> value = [23.64, 23.50, 23.28, 23.48, 22.86, 22.86, 22.73, 22.50, 22.66, 22.50, 21.52, 21.03, 21.36, 22.49, 22.76, 23.34, 23.60, 23.23, 24.01, 23.87, 24.07, 24.42, 24.59, 25.00, 25.20, 24.95, 25.19, 25.24, 24.95, 25.06, 24.53, 24.38, 24.21, 24.64, 24.92, 25.22, 24.91, 24.40, 24.57, 25.05, 25.05, 25.21, 25.18, 26.25, 24.79, 23.88, 25.77, 24.17, 24.79, 24.30, 23.96, 23.87, 23.16, 22.11]
        >>> GenerateGifs(dir_name="experiments/hello").generate_diff_gif(ref_value, value, "hello_dif.gif", config)
        """
        diff_value = [abs(value[i] - val) for i, val in enumerate(ref_value)]
        self.generate_gif(diff_value, os.path.splitext(gif_name)[0] + ".diff.gif", config)

    def generate_gif(self, value, gif_name, config = None):
        """Generate one giff given values as a list, the gif_name is the target file path for the gif geneerated
        >>> param = {"min_val":20, "max_val":30}
        >>> value = [23.64, 23.50, 23.28, 23.48, 22.86, 22.86, 22.73, 22.50, 22.66, 22.50, 21.52, 21.03, 21.36, 22.49, 22.76, 23.34, 23.60, 23.23, 24.01, 23.87, 24.07, 24.42, 24.59, 25.00, 25.20, 24.95, 25.19, 25.24, 24.95, 25.06, 24.53, 24.38, 24.21, 24.64, 24.92, 25.22, 24.91, 24.40, 24.57, 25.05, 25.05, 25.21, 25.18, 26.25, 24.79, 23.88, 25.77, 24.17, 24.79, 24.30, 23.96, 23.87, 23.16, 22.11]
        >>> GenerateGifs(dir_name="experiments").generate_gif(value, "hello.gif")
        >>> GenerateGifs(dir_name="experiments").generate_gif(value, "hello2.gif", param)
        """
        size = len(value)
        v, x, y = get_approx_xy(size)
        max_val = min(value)
        min_val = max(value)

        root_dir = get_img_report_dir()
        tmp_dir = os.path.join(root_dir, self.dir_name)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        output_file_path = os.path.join(tmp_dir, gif_name)
        if config is None:
            contents = Gnuplotter.gen_image_content(value, x = x, y = y, min_val= min_val, max_val= max_val)
        else:
            if "x" not in config or "y" not in config:
                config["x"] = x
                config["y"] = y
            if "max_val" not in config: config["max_val"] = max_val
            if "min_val" not in config: config["min_val"] = min_val
            contents = Gnuplotter.gen_image_content(value, **config)

        config = {"img":True, "output_file_path":output_file_path}
        Gnuplotter.gnuplotter(config=config, contents=contents)


    @staticmethod
    def generate_gifs_for_one_host(output_dir_name, host, correct_value, values):
        max_val = max(correct_value)
        min_val = min(correct_value)

        g = GenerateGifs("%s/abs" % output_dir_name)
        param = {"max_val":max_val, "min_val":min_val}
        for i, value in enumerate(values):
            g.generate_gif(value, host + "_%04d.gif" % i, param)

        g = GenerateGifs("%s/diffs" % output_dir_name)
        max_val = GetProcessedInformation.get_diff_max(correct_value, values)
        param = {"max_val":max_val, "min_val":0}
        for i, value in enumerate(values):
            g.generate_diff_gif(correct_value, value, host + "_%04d.gif" % i, param)

    @staticmethod
    def generate_gifs(network_dir, condition, sub_name):
        r = ReadReports(network_dir)
        get_info = GetInformation(r, use_cache=True)
        hosts = get_info.get_hosts()
        network_name = os.path.basename(network_dir)
        correct_value = get_info.get_correct_values(condition)

        for host in hosts:
            values = get_info.get_iterations(condition, sub_name, host, "Estimated values")
            output_dir_name = network_name + os.sep + condition + os.sep + sub_name + os.sep + host
            GenerateGifs.generate_gifs_for_one_host(output_dir_name, host, correct_value, values)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
