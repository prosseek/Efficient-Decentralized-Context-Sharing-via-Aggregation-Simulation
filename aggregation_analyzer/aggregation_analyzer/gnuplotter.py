import os
from subprocess import Popen, PIPE
import sys
import os
import re
import distutils.spawn

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
    def new_latex_file(name):
        dir, file = os.path.split(name)
        return os.path.join(dir, "tex_" + file)

    def gnuplotter(names):
        p = Popen([GNUPLOT], shell=False, stdin=PIPE, stdout=PIPE)
        p.stdin.write(r'set terminal latex;')
        p.stdin.write(r'set output "{output_file_name}";'.format(**names))
        p.stdin.write(r'plot "{file_path}" u 1:2 t "{label1}" w line, "{file_path}" u 1:3 t "{label2}" w line'.format(**names))
        out, err = p.communicate()

    def launch_pdf_viewer(name):
        p = Popen(['open','-a','Preview','%s' % name])
        p.communicate()

    def latex_compiler(latex_source):
        p = Popen([PDF_LATEX, latex_source], shell=False)
        p.communicate()

        pdf_file_name = latex_source.replace(".tex",".pdf")
        if os.path.exists(pdf_file_name):
            return pdf_file_name
        else:
            return None