import os
import platform
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GuiWindow(object):
    def __init__(self, master):
        self.master = master

        self.OS = platform.system()
        self.checkmark = ImageTk.PhotoImage(file = os.path.join("images", "check.png"))
        self.blank = ImageTk.PhotoImage(file = os.path.join("images", "blank.png"))
        self.icon = ImageTk.PhotoImage(file = os.path.join("images", "android-icon.png"))
        self.no_image = ImageTk.PhotoImage(file = os.path.join("images", "no_image.png"))
        self.file_types =["Archive files","Image Files","Audio Files","Video Files","Rpy Files","Rpyc Files"]
        self.stat_list = [0] * len(self.file_types)
        self.icon_found = False

        self.frame1 = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame1, text='Browse', width=10)
        self.button1.pack(side=tk.RIGHT, padx=2, pady=2)
        self.labelframe = tk.LabelFrame(self.frame1)
        self.left = tk.Label(self.labelframe, font='Helvetica 12', text="Select Your game folder")
        self.left.pack(side=tk.LEFT)
        self.labelframe.pack(fill=tk.X)

        self.frame1.pack(fill=tk.X, pady=2, padx=10)

        self.frame6 = tk.Frame(master)

        self.frame6.pack(fill=tk.X, pady=10, padx=10)

        self.frame4 = tk.Frame(master)

        self.frame2 = tk.Frame(self.frame4)

        self.button10 = tk.Button(self.frame2, text='Select All', command=self.select_all)
        self.button10.grid(row=2, column=0, columnspan=2, sticky=tk.W + tk.E)

        self.CheckVar1 = tk.IntVar()
        self.C1 = tk.Checkbutton(self.frame2, variable=self.CheckVar1)
        self.C1.grid(row=3)
        self.C1_label = tk.Label(self.frame2, font='Helvetica 12', text="Extraxct rpa archives")
        self.C1_label.grid(row=3, column=1, sticky=tk.W)

        self.CheckVar2 = tk.IntVar()
        self.C2 = tk.Checkbutton(self.frame2, variable=self.CheckVar2)
        self.C2.grid(row=4)
        self.C2_label = tk.Label(self.frame2, font='Helvetica 12', text="Delete rpa archives")
        self.C2_label.grid(row=4, column=1, sticky=tk.W)

        self.CheckVar3 = tk.IntVar()
        self.C3 = tk.Checkbutton(self.frame2, variable=self.CheckVar3)
        self.C3.grid(row=6)
        self.C3_label = tk.Label(self.frame2, font='Helvetica 12', text="Compress images")
        self.C3_label.grid(row=6, column=1, sticky=tk.W)

        self.CheckVar6 = tk.IntVar()
        self.C6 = tk.Checkbutton(self.frame2, variable=self.CheckVar6)
        self.C6.grid(row=7)
        self.C6_label = tk.Label(self.frame2, font='Helvetica 12', text="Compress audio")
        self.C6_label.grid(row=7, column=1, sticky=tk.W)

        self.CheckVar4 = tk.IntVar()
        self.C4 = tk.Checkbutton(self.frame2, variable=self.CheckVar4)
        self.C4.grid(row=8)
        self.C4_label = tk.Label(self.frame2, font='Helvetica 12', text="Compress video")
        self.C4_label.grid(row=8, column=1, sticky=tk.W)
        self.CheckVar5 = tk.IntVar()
        self.C5 = tk.Checkbutton(self.frame2, variable=self.CheckVar5)
        self.C5.grid(row=5)
        self.C5_label = tk.Label(self.frame2, font='Helvetica 12', text="Decompile rpyc files")
        self.C5_label.grid(row=5, column=1, sticky=tk.W)

        self.check = tk.Label(self.frame2, image=self.blank).grid(row=3, column=2)
        self.check = tk.Label(self.frame2, image=self.blank).grid(row=3, column=3)
        self.check = tk.Label(self.frame2, image=self.blank).grid(row=3, column=4)

        self.icon_image_frame = tk.LabelFrame(self.frame2,text="Icon Image")
        self.icon_image = tk.Button(self.icon_image_frame, image=self.no_image)
        self.icon_image.pack(pady=10, padx=10)
        self.icon_image_frame.grid(row=3, column=5, rowspan=6, sticky=tk.W)

        self.frame2.pack(side=tk.LEFT, padx=25, pady=10)

        self.frame3 = tk.Frame(self.frame4)

        self.button6 = tk.Button(self.frame3, text='Edit .rpy files', width=15)
        self.button6.config(state=tk.DISABLED)
        self.button6.pack(pady=10, padx=25)

        self.button14 = tk.Button(self.frame3, text='Imagebutton', width=15)
        self.button14.config(state=tk.DISABLED)
        self.button14.pack(pady=10, padx=25)

        self.button15 = tk.Button(self.frame3, text='Imagebutton single', width=15)
        self.button15.pack(pady=10, padx=25)

        self.button16 = tk.Button(self.frame3, text='Finish Up', width=15)
        # self.button16.config(state=tk.DISABLED)
        self.button16.pack(pady=10, padx=25)

        self.frame3.pack(side=tk.RIGHT, padx=10)

        self.frame4.pack(fill=tk.X)

        self.frame8 = tk.Frame(master)

        self.image_quality_frame = tk.LabelFrame(self.frame8,text="Image Quality")
        self.image_quality_slider = tk.Scale(self.image_quality_frame, from_=10, to=100, width=7, length=150, orient=tk.HORIZONTAL)
        self.image_quality_slider.pack()
        self.image_quality_slider.set("65")
        self.image_quality_frame.pack(side=tk.LEFT, padx=10)

        self.audio_quality_frame = tk.LabelFrame(self.frame8,text="Audio Quality(lower is better)")
        self.audio_quality_slider = tk.Scale(self.audio_quality_frame, from_=0, to=9, width=7, length=150, orient=tk.HORIZONTAL)
        self.audio_quality_slider.pack()
        self.audio_quality_slider.set("7")
        self.audio_quality_frame.pack(side=tk.LEFT, padx=10)

        self.video_quality_frame = tk.LabelFrame(self.frame8,text="Video Quality")
        self.video_quality_slider = tk.Scale(self.video_quality_frame, from_=10, to=55, width=7, length=150, orient=tk.HORIZONTAL)
        self.video_quality_slider.pack()
        self.video_quality_slider.set("23")
        self.video_quality_frame.pack(side=tk.LEFT, padx=10)

        self.button17 = tk.Button(self.frame8, text='Default', width=15, command = self.toggle_default_quality)
        self.button17.pack(side=tk.LEFT, padx=25)

        self.frame8.pack(fill=tk.X)

        self.frame5 = tk.Frame(master)

        self.progressPercent = tk.IntVar()
        self.progressframe = tk.LabelFrame(self.frame5, text="Progress: {0} % ".format(self.progressPercent.get()))
        self.progressframe.pack(fill=tk.X)
        self.progress_bar = ttk.Progressbar(self.progressframe,variable=self.progressPercent,maximum=100, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=3, pady=3)
        self.label = tk.Label(self.progressframe, text="")
        self.label.pack(side=tk.LEFT)

        self.button2 = tk.Button(self.frame5, text='Start', width=10)
        self.button2.config(state=tk.DISABLED)
        self.button2.pack(side=tk.LEFT, pady=15, padx=15)

        self.button3 = tk.Button(self.frame5, text='Quit', width=10, command = self.close_windows)
        self.button3.pack(side=tk.RIGHT, pady=15, padx=15)

        self.frame5.pack(fill=tk.X, pady=10, padx=10)

        self.frame7 = tk.Frame(self.frame6)

        self.set_stats(self.stat_list)

        self.frame7.pack()

    def toggle_default_quality(self):
        self.image_quality_slider.set("65")
        self.audio_quality_slider.set("7")
        self.video_quality_slider.set("23")

    def close_windows(self):
        self.master.destroy()

    def select_all(self):
        self.C1.select()
        self.C2.select()
        self.C3.select()
        self.C4.select()
        self.C5.select()
        self.C6.select()
        self.button10.config(text='Deselect All', command=self.deselect_all)

    def deselect_all(self):
        self.C1.deselect()
        self.C2.deselect()
        self.C3.deselect()
        self.C4.deselect()
        self.C5.deselect()
        self.C6.deselect()
        self.button10.config(text='Select All', command=self.select_all)

    def reset_all(self):
        self.button2.config(state=tk.DISABLED)
        self.button6.config(state=tk.DISABLED)
        self.button14.config(state=tk.DISABLED)
        self.set_stats(self.stat_list)
        self.set_progress_text("")
        self.remove_checkmarks()
        self.set_percent(0)

    def set_checkmark(self, r):
        self.check = tk.Label(self.frame2, image=self.checkmark).grid(row=r, column=2)

    def remove_checkmarks(self):
        for i in range(3, 9):
            self.check = tk.Label(self.frame2, image=self.blank).grid(row=i, column=2)

    def set_percent(self, percent):
            self.progressPercent.set(percent)
            self.progressframe.config(text="Progress: {0} % ".format(self.progressPercent.get()))

    def set_progress_text(self, text):
        self.label.config(text = "")
        self.label.config(text = text)
        self.label.update()

    def set_stats(self,stats):
        self.frame7.destroy()
        self.frame7 = tk.Frame(self.frame6)

        if stats[1] != 0:
            self.C3.select()  # images
        if stats[2] != 0:
            self.C6.select()  # audio
        else:
            self.C6.deselect()  # audio
        if stats[3] != 0:
            self.C4.select()  # video
        else:
            self.C4.deselect()  # video
        if stats[4] < stats[5]:
            self.C5.select()  # rpyc
        if stats[0] != 0:
            self.C1.select()  # extract_archive
            self.C2.select()  # delete_archive
            self.C3.deselect()  # images
            self.C4.deselect()  # video
            self.C5.deselect()  # rpyc
            self.C6.deselect()  # audio
        else:
            self.C1.deselect()  # extract_archive
            self.C2.deselect()  # delete_archive

        for i in range(len(stats)):
            stat_name = 'self.stat{}'.format(i)
            text_name = 'self.text{}'.format(i)
            stat_name = tk.LabelFrame(self.frame7, text=self.file_types[i])
            text_name = tk.Label(stat_name, font='Helvetica 12 bold', text=stats[i]).pack()
            stat_name.pack(side=tk.LEFT, padx=10)
        self.frame7.pack()

        return stats

def main():

    root = tk.Tk()
    app = GuiWindow(root)
    root.title('spear1403\'s Ren\'py porting app')
    root.minsize(680, 485)
    root.mainloop()

if __name__ == '__main__':
    main()
