#!/usr/bin/env python
##############################################################################
# Copyright (c) 2019 spear1403<spear1403@gmail.com>
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
#
# A helper application for porting Ren'py games to android.
##############################################################################
import os
import configparser
import shutil
import subprocess
import time
import platform
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
from gui_window import GuiWindow
from imagebutton import Imagebutton
from my_utils import archives,media,screens_edit,gui_edit
from my_utils.status import Status
from my_utils.my_defs import Definitions
from unrpa import UnRPA
from PIL import Image, ImageTk

class MainApp:

    def open_dir():
        app.reset_all()
        app.patched.set(False)
        if config.has_option('Paths','Default Path'):
            default_path = config['Paths']['Default Path']
        else:
            default_path = os.getcwd()
        app.baseDir.set(askdirectory(initialdir = default_path))
        if os.path.exists(os.path.join(app.baseDir.get(), 'game')):
            app.gameName.set(os.path.basename(app.baseDir.get()))
            app.gameDir.set(os.path.join(app.baseDir.get(), "game"))
            print("##################################################################################\n")
            print('>>>OS:' + app.OS)
            print('>>>gameName:' + app.gameName.get())
            print('>>>gameDir:' + app.gameDir.get())
            app.left.config(font='Helvetica 12 bold', text=app.gameName.get())
            app.left.update()
            print('>>>dirOpen:' + app.baseDir.get())
            if os.path.dirname(app.baseDir.get()) != default_path:
                config['Paths'] = {'Default Path' : os.path.dirname(app.baseDir.get())}
                print(f">>>default directory set to {config['Paths']['Default Path']}")
                with open('app_config.ini','w') as configfile:
                    config.write(configfile)

            if os.path.isfile(os.path.join(app.baseDir.get(),'android-icon.png')):
                app.icon_found = True
                print("Icon already there")
                MainApp.set_icon_image(os.path.join(app.baseDir.get(),'android-icon.png'))
            global file_count
            file_count = app.set_stats(Status.count_files(app.gameDir.get()))


            app.button2.config(state=tk.ACTIVE)
            app.button6.config(state=tk.ACTIVE)
            app.button14.config(state=tk.ACTIVE)
            app.dirTrue.set(1)

            print("\n##################################################################################\n")
        else:
            print('No valid game directory!')
            app.left.config(text='No valid game directory!', font='Helvetica 12')
            app.left.update()

    def set_icon_image(img):
        my_image = Image.open(img)
        my_image = my_image.resize((144, 144), Image.ANTIALIAS)
        new_icon_image = ImageTk.PhotoImage(my_image)
        app.icon_image.config(image=new_icon_image)
        app.icon_image.image = new_icon_image

    def go():
        if app.dirTrue.get()==1:
            start = time.time()
            global file_count

            if app.CheckVar5.get() == 1:
                if not file_count[4] == file_count[5]:
                    rpyc_files = Definitions.listing_files(app.gameDir.get(), '.rpyc')
                    if rpyc_files:
                        for index,rpyc in enumerate(rpyc_files):
                            app.set_percent(int(index+1)/len(rpyc_files)*100)
                            app.set_progress_text('Processing---{0}({1}/{2})'.format(os.path.basename(rpyc), int(index+1), len(rpyc_files)))
                            if os.path.isfile(os.path.splitext(rpyc)[0] + ".rpy"):
                                continue
                            else:
                                print(rpyc)
                                if app.OS == 'Windows':
                                    unrpyc_my = os.path.join("tools","win_unrpyc.exe")
                                    cmd = subprocess.Popen(f'{unrpyc_my} "{rpyc}"')
                                    cmd.wait()
                                else:
                                    unrpyc_my = os.path.join("tools","linux_unrpyc")
                                    os.popen(f'./{unrpyc_my} "{rpyc}"')

                app.set_checkmark(5)

            if app.CheckVar3.get() == 1:
                # q = 65
                q = app.image_quality_slider.get()
                image_files = Definitions.listing_files(app.gameDir.get(), '.png', '.bmp', '.jpg', '.jpeg', '.webp', '.pic')
                if image_files:
                    for index,image in enumerate(image_files):
                        app.set_percent(int(index+1)/len(image_files)*100)
                        app.set_progress_text('Processing---{0}({1}/{2})'.format(os.path.basename(image), int(index+1), len(image_files)))
                        media.compress_media(image, quality=q, image=True, OS=app.OS)
                print("Done")
                app.set_checkmark(6)

            if app.CheckVar4.get() == 1:
                # crf = 44 # Max's Life, Solvalley School
                # crf = 23 # Default
                crf = app.video_quality_slider.get()
                video_files = Definitions.listing_files(app.gameDir.get(), '.ogv','.mpg','.m4v', '.avi', '.webm', '.mp4', '.mkv')
                if video_files:
                    for index,video in enumerate(video_files):
                        app.set_percent(int(index+1)/len(video_files)*100)
                        app.set_progress_text('Processing---{0}({1}/{2})'.format(os.path.basename(video), int(index+1), len(video_files)))
                        print('Processing---{0}({1}/{2})'.format(os.path.basename(video), int(index+1), len(video_files)))
                        media.compress_media(video, quality=crf, video=True, OS=app.OS)
                print("Done")
                app.set_checkmark(8)

            if app.CheckVar6.get() == 1:
                aq = app.audio_quality_slider.get()
                audio_files = Definitions.listing_files(app.gameDir.get(), '.mp3','.ogg', '.wav', '.opus')
                if audio_files:
                    for index,audio in enumerate(audio_files):
                        app.set_percent(int(index+1)/len(audio_files)*100)
                        app.set_progress_text('Processing---{0}({1}/{2})'.format(os.path.basename(audio), int(index+1), len(audio_files)))
                        media.compress_media(audio, quality=aq, audio=True, OS=app.OS)
                print("Done")
                app.set_checkmark(7)

            if app.CheckVar1.get() == 1:
                archive_files = archives.get_archive_files(app.gameDir.get())
                if archive_files:
                    # print(files)
                    for index,archive in enumerate(archive_files):
                        app.set_percent(int(index+1)/len(archive_files)*100)
                        app.set_progress_text('Extracting------{0}'.format(archive))
                        extractor = UnRPA(filename=archive, path=app.gameDir.get(), mkdir=True, continue_on_error=True)
                        extractor.extract_files()
                        if app.CheckVar2.get() == 1:
                            app.set_progress_text("Deleting------{0}".format(archive))
                            os.remove(archive)
                    print("Done")
                app.set_checkmark(3)
                app.set_checkmark(4)
            file_count = app.set_stats(Status.count_files(app.gameDir.get()))

        if os.path.isfile(os.path.join(app.baseDir.get(),'android-presplash.jpg')):
            print("Presplash image already there")
        else:
            app.set_progress_text('>>>Copying android presplash image to game directory')
            shutil.copy(os.path.join('spear1403', 'android-presplash.jpg'), app.baseDir.get())
            if app.icon_found == False:
                app.set_progress_text('>>>Copying android icon to game directory')
                new_icon_image = Definitions.icon_copy(app.gameDir.get())
                MainApp.set_icon_image(new_icon_image)
        end = time.time()
        totalTime = end - start
        print(totalTime)
        minute, sekunde = divmod(int(totalTime), 60)
        print(minute, sekunde)
        app.set_progress_text('Completed in {0}:{1:0=2d} minutes'.format(minute, sekunde))
        app.button16.config(state=tk.NORMAL)

    def finish_up():
        print("##################################################################################\n")



        if os.path.isfile(os.path.join(app.gameDir.get(),'spear1403.rpy')):
            print("spear1403.rpy already there")
        else:
            app.set_progress_text('>>>Copying the >spear1403.rpy< file to the game directory')
            shutil.copy(os.path.join('spear1403', 'spear1403.rpy'), app.gameDir.get())
        app.set_progress_text('>>>Copying choice buttons to the phone folder')
        Definitions.hover_button_copy(app.gameDir.get())

        app.set_progress_text('>>>Deleting lib and renpy folders from base directory')
        Definitions.delete_lib_renpy(app.gameDir.get())

        if  app.patched.get():
            print("Screens and Gui already patched")
        else:
            print('patching screens and gui file')
            if os.path.isfile(os.path.join(app.gameDir.get(),'screens.rpy')):
                screens_file = os.path.join(app.gameDir.get(),'screens.rpy')
            elif os.path.isfile(os.path.join(app.gameDir.get(),'scripts','screens.rpy')):
                screens_file = os.path.join(app.gameDir.get(),'scripts','screens.rpy')
            else:
                screens_file = None
            if screens_file is not None:
                screens_edit.open_screens_for_edit(screens_file)
                app.patched.set(True)

            if os.path.isfile(os.path.join(app.gameDir.get(),'gui.rpy')):
                gui_file = os.path.join(app.gameDir.get(),'gui.rpy')
            elif os.path.isfile(os.path.join(app.gameDir.get(),'scripts','gui.rpy')):
                gui_file = os.path.join(app.gameDir.get(),'scripts','gui.rpy')
            else:
                gui_file = None
            if gui_file is not None:
                gui_edit.open_gui_for_edit(gui_file)
                app.patched.set(True)

        print("\n###################################################################################")

if __name__ == '__main__':
    root = tk.Tk()
    app = GuiWindow(root)
    root.title('spear1403\'s Ren\'py porting app')
    # root.minsize(620, 400)

    config = configparser.ConfigParser()
    config.read('app_config.ini')

    app.dirTrue = tk.IntVar()
    app.gameName = tk.StringVar()
    app.gameDir = tk.StringVar()
    app.baseDir = tk.StringVar()
    app.patched = tk.BooleanVar()
    app.button1.config(command = MainApp.open_dir)
    app.button6.config(command=lambda:Definitions.open_rpy_for_edit(app.gameDir.get(),app.OS))
    app.button14.config(command=lambda:Imagebutton.automatika(app.gameDir.get(),app.gameName.get()))
    app.button15.config(command=Imagebutton.single_imagebutton)
    app.button16.config(command=MainApp.finish_up)
    app.button2.config(command=MainApp.go)

    root.mainloop()
