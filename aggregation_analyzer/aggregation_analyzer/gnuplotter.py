import os
from subprocess import Popen, PIPE
import sys
import os
import argparse
import distutils.spawn
import math

latex_template=r"""\documentclass{article}
\begin{document}
%s
\end{document}
"""

# http://stackoverflow.com/questions/5226958/which-equivalent-function-in-python
GNUPLOT=distutils.spawn.find_executable('gnuplot')
PDF_LATEX=distutils.spawn.find_executable('pdflatex')

def error(message):
    print >> sys.stderr, message
    sys.exit(0)

if GNUPLOT is None:
    error("No GNUPLOT")

if PDF_LATEX is None:
    error("No PDF_LATEX")

home = os.path.expanduser("~")
output_dirname = os.path.join(home, "tmp")
if not os.path.exists(output_dirname):
    os.makedirs(output_dirname)

output_file_path = os.path.abspath("hello.tex")
#tmp_directory =

class Gnuplotter(object):

    @staticmethod
    def new_latex_file(name):
        dir, file = os.path.split(name)
        return os.path.join(dir, "tex_" + file)

    @staticmethod
    def gnuplotter(config, contents):
        config["label1"] = "L1"
        config["label2"] = "L2"
        p = Popen([GNUPLOT], shell=False, stdin=PIPE, stdout=PIPE)
        #p.stdin.write(r'set terminal latex;')
        p.stdin.write(r'set terminal gif;')

        output_dirname = os.path.dirname(config["output_file_path"])
        if not os.path.exists(output_dirname):
            os.makedirs(output_dirname)

        p.stdin.write(r'set output "{output_file_path}";'.format(**config))

        if config["img"]:
            p.stdin.write(contents)
            out, err = p.communicate()
            p.wait()
        else:
            p.stdin.write(r'plot "{file_path}" u 1:2 t "{label1}" w line, "{file_path}" u 1:3 t "{label2}" w line'.format(**config))

            out, err = p.communicate()

            with open(config["output_file_path"], "r") as f:
                latex_content_from_file = f.read()

            latex_content = latex_template % latex_content_from_file

            latex_src_file = Gnuplotter.new_latex_file(config["output_file_path"])
            with open(latex_src_file, "w") as f:
                f.write(latex_content)

            pdf_file = Gnuplotter.latex_compiler(latex_src_file)
            Gnuplotter.launch_pdf_viewer(pdf_file)

    @staticmethod
    def launch_pdf_viewer(name):
        p = Popen(['open','-a','Preview','%s' % name])
        p.communicate()

    @staticmethod
    def latex_compiler(latex_source):
        p = os.path.dirname(latex_source)
        p2 = os.getcwd()

        os.chdir(p)
        p = Popen([PDF_LATEX, latex_source], shell=False)
        p.communicate()

        os.chdir(p2)

        pdf_file_name = latex_source.replace(".tex",".pdf")
        if os.path.exists(pdf_file_name):
            return pdf_file_name
        else:
            return None

    @staticmethod
    def gen_image_content(tempatures, x, y, min_val=None, max_val=None):

        if min_val is None:
            min_val = min(tempatures)
        if max_val is None:
            max_val = max(tempatures)

        result = "set xrange [-0.5:%4.1f]\nset yrange [-0.5:%4.1f]\n" % (x -.5,y-.5)
        result += "set cbrange [%d:%d]\n" % (min_val, max_val)
        result += "set palette rgbformula -7,2,-7\nset view map\nunset key\nset tic scale 0\nunset cbtics\n"
        result += "set cblabel \"Temp\"\n"

        result += "splot '-' matrix with image\n"

        count = x # if 3 -> 2,1,0 (3)
        for l in tempatures:
            result += "%4.2f " % l
            count -= 1
            if count == 0:
                result += "\n"
                count = x
        for i in range(count):
            result += "0 "
        result +="\ne\ne\n"
        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser() # prog='gp', usage='%(prog)s [options]')

    parser.add_argument('-m','--img', action="store_true", default=False, help='result in image format')
    parser.add_argument('-f', action="store", dest="file_path")
    parser.add_argument('-o', action="store", dest="output_file_name")
    # parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()

    #print args

    if args.file_path is None or args.output_file_name is None:
        parser.print_help()
        sys.exit()

    if not os.path.exists(args.file_path):
        print >> sys.stderr, "No file exists %s" % args.file_path

    #print args.img

    config=vars(args)
    print config

    g = Gnuplotter()
    g.gnuplotter(config)

    if os.path.exists(output_file_path):
        print "%s exists" % output_file_path
        with open(output_file_path, "r") as f:
            buf = f.read()
            result = latex_template % buf
            global latex_src
            latex_src = g.new_latex_file(output_file_path)

            with open(latex_src, "w") as f2:
                f2.write(result)
                f2.close()
            f.close()

        generated_pdf_file = g.latex_compiler(latex_src)
        if generated_pdf_file:
            g.launch_pdf_viewer(generated_pdf_file)