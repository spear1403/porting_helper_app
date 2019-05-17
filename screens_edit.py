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

def parse_block_list(block_list):
    global quick_block, quick_menu, set_default, append_screens
    if any('if renpy.variant("pc"):' in s for s in block_list) and any('if renpy.variant("pc"):' in s for s in block_list):
        for index,item in enumerate(block_list):
            if 'if renpy.variant("pc"):' in item:
                indent = indent_finder(item)
                first_index = index
            if 'textbutton _("Quit")'in item:
                block_list[index] = "{0}{1}".format(indent,block_list[index].lstrip())
                del block_list[first_index:index]
        return block_list
    elif any('variant "small"' in s for s in block_list) or any('variant "touch"' in s for s in block_list):
        new_block = []
        for item in block_list:
            if not item == '\n':
                item = hash_out(item)
            new_block.append(item)
        return new_block
    elif any('screen quick_menu():' in s for s in block_list):
        quick_menu = True
        new_block = quick_block
        return new_block
    elif any('default quick_menu =' in s for s in block_list):
        set_default = True
        new_block = ['default quick_menu = False\n','default quick_menu2 = True\n','\n']
        return new_block
    for index,line in enumerate(block_list):
        if 'if not renpy.variant("small"):' in line:
            print("side_image part")
            indent = indent_finder(line)
            block_list[index] = '\n'
            block_list[index+1] = "{0}{1}".format(indent,block_list[index+1].lstrip())
            break
        if 'variant "medium"' in line:
            block_list[index] = block_list[index].replace('"medium"','"small"')
        if 'substitute False' in line:
            block_list[index] = hash_out(block_list[index])
            if 'text what' in block_list[index-1]:
                block_list[index-1] = block_list[index-1].replace(':','')
        if 'config.overlay_screens.append("quick_menu")' in line:
            append_screens = True
    return block_list

def open_screens_for_edit(file):
    global quick_block, quick_menu, set_default, append_screens
    quick_block = ['screen quick_menu():\n',
                        '   zorder 100\n',
                        '   hbox:\n',
                        '       style_prefix "quick"\n',
                        '       xalign 0.5\n',
                        '       yalign 1.0\n',
                        '       if quick_menu:\n',
                        '           textbutton _("Quick1") action ShowMenu()\n',
                        '       if quick_menu2:\n',
                        '           textbutton _("Quick2") action ShowMenu()\n',]
    quick_menu = False
    set_default = False
    append_screens = False
    block_list = []
    #backup orig file
    shutil.copy(file,file+'.bak')
    temp_file = file+'.temp'
    with open(file, 'r',encoding="utf8") as in_file:
        with open(temp_file, 'w',encoding="utf8") as out_file:
            for line in in_file:

                if block_list:
                    if len(line)-len(line.lstrip()) > 0:
                        block_list.append(line)
                    else:
                        print('Block list: {}'.format(block_list))
                        if not len(block_list) == 1 and not block_list[0].lstrip().startswith('#'):
                            print("Parsing: ???")
                            block_list = parse_block_list(block_list)
                        for l in block_list:
                            out_file.write(l)
                        block_list.clear()
                        block_list.append(line)
                        continue

                if len(line)-len(line.lstrip()) == 0:
                    block_list.append(line)
                    continue
                    # print('Both lists are empty, You fucked something up')

            if block_list:
                print('Block list: {}'.format(block_list))
                parsed_list = parse_block_list(block_list)
                for l in parsed_list:
                    out_file.write(l)

            if quick_menu == False:
                for w in quick_block:
                    out_file.write(w)
            if append_screens == False:
                out_file.write('\ninit python:\n    config.overlay_screens.append("quick_menu")\n')
            if set_default == False:
                out_file.write('\ndefault quick_menu = False\ndefault quick_menu2 = True\n')

    shutil.copyfile(temp_file, file)
    os.remove(temp_file )

if __name__ == "__main__":
    file = askopenfilename(filetypes=[('Renpy rpy files', '*.rpy'), ('All files', '*,*')])
    open_screens_for_edit(file)
