import os
import io
import subprocess

from optparse import OptionParser

from pycparser import c_parser

import my_visitor


def read_source(pp, filename):
    text = ""
    with open(filename) as f:
        text = f.read()
    code = ""
    system_include_list = []
    for line in text.splitlines():
        if line.strip().startswith("#include") and '<' in line:
            code += "/* CONVERTER_TEMP_COMMENTOUT " + line + "*/" + "\n"
            system_include_list.append(line)
        else:
            code += line + "\n"
    res = subprocess.run(
        [pp, "-xc", "-E", "-"], stdout=subprocess.PIPE, input=code.encode()
    )
    text = res.stdout.decode("utf-8")
    code = ""
    for line in text.splitlines():
        if len(line) > 0 and line[0] != "#":
            code += line + "\n"
    basename = os.path.basename(filename)
    with open(basename + ".E", "w") as f:
        print(code, file=f)
    return code, system_include_list


def parse(pp, filename):
    code, system_include_list = read_source(pp, filename)
    parser = c_parser.CParser()
    ast = parser.parse(code)
    basename = os.path.basename(filename)
    with open(basename + ".ast", "w") as f:
        print(ast, file=f)
    output = io.StringIO()
    visitor = my_visitor.MyVisitor(output)
    visitor.visit(ast)
    ret = output.getvalue()
    for stmt in system_include_list:
        print(stmt + "\n")
    print(ret)


if __name__ == "__main__":
    usage = "Usage: %prog C-sources"
    p = OptionParser(usage)
    p.add_option("", "--pp", dest="pp", help="specify preprocessor")
    opts, args = p.parse_args()
    pp = "gcc"

    if opts.pp is not None:
        pp = opts.pp

    for arg in args:
        src = arg
        name, ext = os.path.splitext(src)
        parse(pp, src)
