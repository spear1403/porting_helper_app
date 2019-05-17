class Tools():

    def indent_finder(line):
        indent_nr = len(line)-len(line.lstrip())
        indent = indent_nr * " "
        return indent

    def hash_out(line):
        indent = Tools.indent_finder(line)
        new_line = "{0}# {1}".format(indent, line.lstrip())
        return new_line
