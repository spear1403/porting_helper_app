import os
import shutil
import time
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
import my_utils.unpack_rpyc
import my_utils.archives
import my_utils.media
from gui_window import GuiWindow
from my_utils.status import Status
from my_utils.my_defs import Definitions

class MainApp:

    def open_dir():
        app.reset_all()
        dir_open = askdirectory()
        if os.path.exists(os.path.join(dir_open, 'game')):
            gameName = os.path.basename(dir_open)
            app.gameDir.set(os.path.join(dir_open, "game"))
            archive_count,image_count,audio_count,video_count = Status.check_status(app.gameDir.get())
            app.status_text.config(text="Status:            archives: {0}   images: {1}   audio files: {2}   videos: {3}".format(archive_count,image_count,audio_count,video_count))
            print("##################################################################################\n")
            print('>>>gameName:' + gameName)
            print('>>>gameDir:' + app.gameDir.get())
            app.left.config(font='Helvetica 12 bold', text=gameName)
            app.left.update()
            print('>>>dirOpen:' + dir_open)
            print("\n##################################################################################\n")
            app.button2.config(state=tk.ACTIVE)
            app.button6.config(state=tk.ACTIVE)
            app.button14.config(state=tk.ACTIVE)
            app.dirTrue.set(1)
        else:
            print('No valid game directory!')
            app.left.config(text='No valid game directory!', font='Helvetica 12')
            app.left.update()

    def go():
        if app.dirTrue.get()==1:
            start = time.time()
            if app.CheckVar1.get() == 1:
                archive_files = my_utils.archives.get_archive_files(app.gameDir.get())
                if archive_files:
                    # print(files)
                    for index,archive in enumerate(archive_files):
                        app.set_percent(int(index+1)/len(archive_files)*100)
                        app.set_progress_text('Extracting------{0}'.format(archive))
                        my_utils.archives.extract_archives(archive)
                        if app.CheckVar2.get() == 1:
                            app.set_progress_text("Deleting------{0}".format(archive))
                            os.remove(archive)
                    print("Done")
                app.set_checkmark(3)
                app.set_checkmark(4)
                archive_count,image_count,audio_count,video_count = Status.check_status(app.gameDir.get())
                app.status_text.config(text="Status:            archives: {0}   images: {1}   audio files: {2}   videos: {3}".format(archive_count,image_count,audio_count,video_count))

            if app.CheckVar5.get() == 1:
                my_utils.unpack_rpyc.decompile_rpyc_files(app.gameDir.get())
                app.set_checkmark(8)

            if app.CheckVar3.get() == 1:
                q = app.quality_slider.get()
                image_files = Definitions.listing_files(app.gameDir.get(), '.png', '.bmp', '.jpg', '.jpeg', '.webp', '.pic')
                if image_files:
                    for index,image in enumerate(image_files):
                        app.set_percent(int(index+1)/len(image_files)*100)
                        app.set_progress_text('Processing---{0}({1}/{2})'.format(os.path.basename(image), int(index+1), len(image_files)))
                        my_utils.media.compress_media(image, quality=q, image=True)
                print("Done")
                app.set_checkmark(5)

            if app.CheckVar4.get() == 1:
                crf = app.video_quality_slider.get()
                video_files = Definitions.listing_files(app.gameDir.get(), '.ogv','.mpg','.m4v', '.avi', '.webm', '.mp4', '.mkv')
                if video_files:
                    for index,video in enumerate(video_files):
                        app.set_percent(int(index+1)/len(video_files)*100)
                        app.set_progress_text('Processing---{0}({1}/{2})'.format(os.path.basename(video), int(index+1), len(video_files)))
                        my_utils.media.compress_media(video, quality=crf, video=True)
                print("Done")
                app.set_checkmark(7)

            if app.CheckVar6.get() == 1:
                audio_files = Definitions.listing_files(app.gameDir.get(), '.mp3','.ogg', '.wav', '.opus')
                if audio_files:
                    for index,audio in enumerate(audio_files):
                        app.set_percent(int(index+1)/len(audio_files)*100)
                        app.set_progress_text('Processing---{0}({1}/{2})'.format(os.path.basename(audio), int(index+1), len(audio_files)))
                        my_utils.media.compress_media(audio, audio=True)
                print("Done")
                app.set_checkmark(6)



        print("##################################################################################\n")

        print('>>>Copying android splashscreen to game directory')
        app.set_progress_text('>>>Copying android splashscreen to game directory')
        shutil.copy('android-presplash.jpg', app.gameDir.get().split("game")[0])
        print('>>>Copying the >spear1403.rpy< file to the game directory')
        app.set_progress_text('>>>Copying the >spear1403.rpy< file to the game directory')
        shutil.copy('spear1403.rpy', app.gameDir.get())
        app.set_progress_text('>>>Copying choice buttons to the phone folder')
        Definitions.hover_button_copy(app.gameDir.get())
        app.set_progress_text('>>>Copying android icon to game directory')
        Definitions.icon_copy(app.gameDir.get())
        app.set_progress_text('>>>Deleting lib and renpy folders from base directory')
        Definitions.delete_lib_renpy(app.gameDir.get())

        print("\n###################################################################################")
        end = time.time()
        totalTime = end - start
        print(totalTime)
        minute, sekunde = divmod(int(totalTime), 60)
        print(minute, sekunde)
        app.set_progress_text('Completed in {0}:{1:0=2d} minutes'.format(minute, sekunde))

if __name__ == '__main__':
    root = tk.Tk()
    app = GuiWindow(root)
    root.title('spear1403\'s Ren\'py porting app')
    root.title('spear1403\'s Ren\'py porting app')
    # root.minsize(620, 400)

    app.dirTrue = tk.IntVar()
    app.gameDir = tk.StringVar()
    app.button1.config(command = MainApp.open_dir)
    app.button6.config(command=lambda:Definitions.open_rpy_for_edit(app.gameDir.get()))
    app.button14.config(command=lambda:Definitions.automatika(app.gameDir.get()))
    app.button15.config(command=Definitions.single_imagebutton)
    app.button2.config(command=MainApp.go)

    root.mainloop()
