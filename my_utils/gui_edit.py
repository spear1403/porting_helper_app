import os,shutil
from tkinter.filedialog import askopenfilename

def indent_finder(line):
    indent_nr = len(line)-len(line.lstrip())
    indent = indent_nr * " "
    return indent

def hash_out(line):
    indent = indent_finder(line)
    new_line = "{0}# {1}".format(indent, line.lstrip())
    return new_line

def parse_block(block):
    new_block = []
    match = ['gui.text_size','gui.name_text_size','gui.notify_text_size','gui.interface_text_size',
                'gui.button_text_size','gui.label_text_size','gui.navigation_spacing',
                'gui.pref_button_spacing','if renpy.variant("small"):']
    for item in block:
        if any(x in item for x in match) or item.lstrip().startswith('#'):
            new_block.append(item)
            continue
        if any(s in item for s in ['gui.text_xpos','gui.text_width']):
            item = item.replace("text","dialogue")
        if not item.strip() == '':
            print(item)
            item = hash_out(item)
        new_block.append(item)
    return new_block

def open_gui_for_edit(file):
    if os.path.isfile(file + "_orig.bak") == False:
        block_list = []
        #backup orig file
        shutil.copy(file, file + "_orig.bak")
        temp_file = file+'.temp'
        with open(file, 'r',encoding="utf8") as in_file:
            with open(temp_file, 'w',encoding="utf8") as out_file:
                for line in in_file:

                    if block_list:
                        if len(line)-len(line.lstrip()) > indent:
                            block_list.append(line)
                            continue
                        else:
                            print('Block list1: {}'.format(block_list))
                            if not len(block_list) == 1 and not block_list[0].lstrip().startswith('#'):
                                print("Parsing: ???")
                                block_list = parse_block(block_list)
                            for l in block_list:
                                out_file.write(l)
                            block_list.clear()
                            block_list.append(line)
                            continue

                    if 'if renpy.variant("small"):' in line:
                        indent = len(line)-len(line.lstrip())
                        block_list.append(line)
                        continue
                        
                    out_file.write(line)

                if block_list:
                    print('Block list2: {}'.format(block_list))
                    parsed_list = parse_block(block_list)
                    for l in parsed_list:
                        out_file.write(l)

        shutil.copyfile(temp_file, file)
        os.remove(temp_file )

if __name__ == "__main__":
    file = askopenfilename(filetypes=[('Renpy rpy files', '*.rpy'), ('All files', '*,*')])
    open_gui_for_edit(file)
