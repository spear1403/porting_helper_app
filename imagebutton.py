from line_split import LineSplitter
from block_buster import BlockBuster
import get_hotspot
from tkinter import filedialog
import tkinter as tk
import os
import shutil

class Imagebutton:

    def replace_imagebuttons(rpy_file, hotspot_dict):
        game_path = rpy_file.split('game')[0] + 'game'
        print(game_path)
        images_path = os.path.join(game_path,"images")
        print(images_path)
        #backup orig file
        shutil.copy(rpy_file,rpy_file+'.bak')
        temp_file = rpy_file+'.temp'
        found_file = None
        with open(rpy_file, 'r',encoding="utf8") as in_file:
            with open(temp_file, 'w',encoding="utf8") as out_file:
                dont_skip_if_in_block = ["xpos 0", "ypos 0"]
                block_status = False
                block_list = []
                a = ['imagebutton:','imagebutton :']
                file_count = 0
                hash_count = 0
                for line in in_file:
                    if block_status:
                        block_indent = len(line) - len(line.lstrip(' '))
                        if block_indent <= indent:
                            block_eval = BlockBuster.block_handler(game_path, block_list, hotspot_dict)
                            if block_eval:
                                for b in block_eval:
                                    out_file.write(b)
                            else:
                                for item in block_list:
                                    print(item)
                                    out_file.write(item)
                            block_status = False
                            block_list.clear()

                        else:
                            block_list.append(line)
                            continue


                    if any(x in line for x in a):
                    # if "imagebutton:" in line :
                        print("it's an imagebutton block")
                        space_before = line.split('imagebutton')[0]
                        if "#" in space_before:
                            hash_count += 1
                            print('Imagebutton commented out')
                            continue
                        indent = len(line) - len(line.lstrip(' '))
                        block_status = True
                        file_count +=1
                        #line.replace("imagebutton","imagemap")
                        block_list.append(line)
                        continue

                    if "imagebutton" in line:
                        print("it's an imagebutton line")
                        file_count +=1
                        if not "#" in line:
                            print('found imagebutton in this line:\n\n')
                            print('##########################################################################################\n')
                            print('  {}'.format(line))
                            print('##########################################################################################\n')

                            indent, idle, hover, action = LineSplitter.line_splitter(line)

                            if action:

                                file_dir = os.path.dirname(os.path.abspath(rpy_file))
                                print (file_dir)
                                print(hover)
                                print(action)

                                gamedirs = next(os.walk(game_path))[1]
                                print(gamedirs)

                                for g in gamedirs:
                                    if g in hover:
                                        found_file = os.path.join(game_path, hover)
                                    else:
                                        found_file = os.path.join(game_path, "images", hover)

                                # if "/" in hover:
                                #     hover = hover.split("/")[-1]

                                for root, dirs, files in os.walk(file_dir):
                                    for file in files:
                                        if hover.lower() in file.lower():
                                            found_file = os.path.join(root,file)

                                print(found_file)

                                if found_file in hotspot_dict:
                                    hotspot = hotspot_dict.get(found_file)

                                else:
                                    if found_file is not None:
                                        hotspot = get_hotspot.main(found_file, line)
                                        hotspot_dict[found_file] = hotspot
                                        # print(hotspot_dict)
                                    else:
                                        hotspot = None

                                print(hotspot)

                                if hotspot is not None:
                                    tab = "    "
                                    hotspot_block = '\n{0}{1}{1}'.format(indent,tab).join(action)
                                    newline = '{0}imagemap:\n{0}{5}idle "{1}"\n{0}{5}hover "{2}"\n{0}{5}hotspot{3}:\n{0}{5}{5}{4}\n'.format(indent, idle, hover, hotspot, hotspot_block, tab)
                                    print(newline)
                                    line = newline
                        else:
                            hash_count += 1
                            print('found a hashtag. Skipping this one')

                    out_file.write(line)
                if block_list:
                    block_eval = BlockBuster.block_handler(game_path,block_list,hotspot_dict)
                    if block_eval:
                        for b in block_eval:
                            out_file.write(b)
                    else:
                        for item in block_list:
                            print(item)
                            out_file.write(item)
        shutil.copyfile(temp_file, rpy_file)
        os.remove(temp_file )
        print ("#################################     End of file reached...   #######################################")

    def open_file():
        rpy = tk.Tk()
        rpy.withdraw()
        global rpy_file
        rpy_file = filedialog.askopenfilename(filetypes=[('Renpy rpy files', '*.rpy'), ('All files', '*,*')])
        print('File path: {}'.format(rpy_file))



if __name__ == '__main__':
    hotspot_dict = {}
    count_list = []
    root = tk.Tk()
    root.title('Cool App')
    button_open = tk.Button(root, text='Open File', width=25, command=Imagebutton.open_file)
    button_open.pack()
    button_edit = tk.Button(root, text='Edit File', width=25, command=lambda: Imagebutton.replace_imagebuttons(rpy_file, hotspot_dict))
    button_edit.pack()

    root.mainloop()
