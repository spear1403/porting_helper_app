import fnmatch
import os
import tkinter as tk
from tkinter import filedialog


class Functions:

    def find_files(hover, root_path, pattern):
        image_list = []

        for root, dirs, files in os.walk(root_path):
            for filename in files:
                if pattern in filename:
                    image_list.append(os.path.join(root, filename))

        print(image_list)
        if not image_list:
            found_image = filedialog.askopenfilename(filetypes=[('Png files', '*.png'), ('All files', '*,*')])
        if len(image_list) > 1:
            print('there are multiple matches')
            index = Functions.multiple_matches(parent,hover,image_list)
            found_image = image_list[index]
        elif len(image_list)==1:
            print('found it!')
            found_image = image_list[0]

        return found_image

    def onClick(i):
        global chooser, choice
        print('clicked button nr. {}'.format(i))
        choice = i
        chooser.destroy()

    def multiple_matches(parent,hover,image_list):
        global chooser,choice
        chooser =  tk.Toplevel()
        chooser.title(hover)
        image_count = 0
        items = tk.Text(chooser)
        buttons = []
        for i in range(len(image_list)):
            print('{0}.{1}'.format(i, image_list[i]))
            b = tk.Button(chooser,text=image_list[i].split('game')[-1], width=100, command=lambda i=i: Functions.onClick(i))
            b.pack()
            buttons.append(b)

        print('waiting...')
        chooser.wait_window(chooser)
        return choice
