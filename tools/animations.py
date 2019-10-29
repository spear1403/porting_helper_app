from tkinter import filedialog
import tkinter as tk
import os
import shutil

class Animation(object):

    def main(block):
        pass

    def find_images(rpy_file):
        #backup orig file
        shutil.copy(rpy_file,rpy_file+'.bak')
        temp_file = rpy_file+'.temp'
        with open(rpy_file, 'r',encoding="utf8") as in_file:
            with open(temp_file, 'w',encoding="utf8") as out_file:
                block_status = False
                block_list = []
                a = ['image ',':']
                for line in in_file:
                    if block_status:
                        block_indent = len(line) - len(line.lstrip(' '))
                        if len(block_list) == 2:
                            space_x = block_indent*' '
                        if block_indent <= indent:
                            print (len(block_list))

                            if len(block_list) > 400:
                                for i in range(10,len(block_list),10):
                                    if not '"' in block_list[i-8]:
                                        block_list[i-8] = "{0}{1}{2}".format(space_x, float(block_list[i-8].replace("pause","").strip()) * 5, "\n")
                                    block_list[i] = space_x + "# " + block_list[i].lstrip()
                                    block_list[i-1] = space_x + "# " + block_list[i-1].lstrip()
                                    block_list[i-2] = space_x + "# " + block_list[i-2].lstrip()
                                    block_list[i-3] = space_x + "# " + block_list[i-3].lstrip()
                                    block_list[i-4] = space_x + "# " + block_list[i-4].lstrip()
                                    block_list[i-5] = space_x + "# " + block_list[i-5].lstrip()
                                    block_list[i-6] = space_x + "# " + block_list[i-6].lstrip()
                                    block_list[i-7] = space_x + "# " + block_list[i-7].lstrip()
                            elif len(block_list) > 300:
                                for i in range(8,len(block_list),8):
                                    if not '"' in block_list[i-6]:
                                        block_list[i-6] = "{0}{1}{2}".format(space_x, float(block_list[i-6].replace("pause","").strip()) * 4, "\n")
                                    block_list[i] = space_x + "# " + block_list[i].lstrip()
                                    block_list[i-1] = space_x + "# " + block_list[i-1].lstrip()
                                    block_list[i-2] = space_x + "# " + block_list[i-2].lstrip()
                                    block_list[i-3] = space_x + "# " + block_list[i-3].lstrip()
                                    block_list[i-4] = space_x + "# " + block_list[i-4].lstrip()
                                    block_list[i-5] = space_x + "# " + block_list[i-5].lstrip()
                            elif len(block_list) > 200:
                                for i in range(6,len(block_list),6):
                                    if not '"' in block_list[i-4]:
                                        block_list[i-4] = "{0}{1}{2}".format(space_x, float(block_list[i-4].replace("pause"," ").strip()) * 3, "\n")
                                    block_list[i] = space_x + "# " + block_list[i].lstrip()
                                    block_list[i-1] = space_x + "# " + block_list[i-1].lstrip()
                                    block_list[i-2] = space_x + "# " + block_list[i-2].lstrip()
                                    block_list[i-3] = space_x + "# " + block_list[i-3].lstrip()
                            elif len(block_list) > 58:
                                for i in range(4,len(block_list),4):
                                    if not '"' in block_list[i-2]:
                                        block_list[i-2] = "{0}{1}{2}".format(space_x, float(block_list[i-2].replace("pause"," ").strip()) * 2, "\n")
                                    block_list[i] = space_x + "# " + block_list[i].lstrip()
                                    block_list[i-1] = space_x + "# " + block_list[i-1].lstrip()
                            elif len(block_list) > 42:
                                for i in range(4,len(block_list),6):
                                    if not '"' in block_list[i-2]:
                                        block_list[i-2] = "{0}{1}{2}".format(space_x, float(block_list[i-2].replace("pause"," ").strip()) * 2, "\n")
                                    block_list[i] = space_x + "# " + block_list[i].lstrip()
                                    block_list[i-1] = space_x + "# " + block_list[i-1].lstrip()

                            for x in block_list:
                                out_file.write(x)

                            block_status = False
                            block_list.clear()

                        else:
                            block_list.append(line)
                            continue


                    if all(x in line for x in a):
                        print("it's an animation block")
                        if line.lstrip().startswith("#"):
                            print('Image commented out')
                            out_file.write(line)
                            continue
                        indent = len(line) - len(line.lstrip())
                        block_status = True
                        line_count = 0
                        block_list.append(line)
                        continue

                    out_file.write(line)
                if block_list:

                    print (len(block_list))

                    if len(block_list) > 58:
                        for i in range(4,len(block_list),4):
                            if not '"' in block_list[i-2]:
                                block_list[i-2] = "{0}{1}{2}".format(space_x, float(block_list[i-2].replace("pause"," ").strip()) * 2, "\n")
                            block_list[i] = space_x + "# " + block_list[i].lstrip()
                            block_list[i-1] = space_x + "# " + block_list[i-1].lstrip()
                    elif len(block_list) > 42:
                        for i in range(6,len(block_list),6):
                            if not '"' in block_list[i-2]:
                                block_list[i-2] = "{0}{1}{2}".format(space_x, float(block_list[i-2].replace("pause"," ").strip()) * 2, "\n")
                            block_list[i] = space_x + "# " + block_list[i].lstrip()
                            block_list[i-1] = space_x + "# " + block_list[i-1].lstrip()
                    for x in block_list:
                        out_file.write(x)

                    block_status = False
                    block_list.clear()
                    out_file.write(line)

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
    root = tk.Tk()
    root.title('Cool App')
    button_open = tk.Button(root, text='Open File', width=25, command=Animation.open_file)
    button_open.pack()
    button_edit = tk.Button(root, text='Start', width=25, command=lambda: Animation.find_images(rpy_file))
    button_edit.pack()

    root.mainloop()
