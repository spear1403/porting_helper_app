#!/usr/bin/env python
##############################################################################
# Copyright (c) 2019 spear1403<spear1403@gmail.com>
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
#
# An application for unpacking Ren'py game apk's to Ren'py project.
##############################################################################
import os
import shutil
import subprocess
import zipfile
import json
from pyaxmlparser import APK
from tkinter.filedialog import askopenfilename

def rename(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
        shutil.rmtree(src)
    else:
        shutil.copy(src, dst)
        os.unlink(src)
    # print(dst)

def extract_apk(file):
    print(file)
    extract_dir = file.replace(".apk","-pc")
    print(extract_dir)
    zip = zipfile.ZipFile(file)
    name_list = zip.namelist()
    print("Extracting files from apk......")
    for name in name_list:
        if name.startswith("res/drawable") and name.endswith("icon.png"):
            zip.extract(name,extract_dir)
            print(name)
        if name.startswith("res/mipmap-xxhdpi-v4"):
            zip.extract(name,extract_dir)
            print(name)
        if name.startswith("assets"):
            if name.startswith("assets/x-renpy") or name.endswith("private.mp3"):
                continue
            zip.extract(name,extract_dir)
            print(name)
    print("All files extracted.")
    return extract_dir

def create_android_json(folder, app_name, pack_name, version):
    config_file =	{
        "layout": None,
    	"orientation": "sensorLandscape",
    	"package": "com.spear1403.app",
    	"google_play_key": None,
    	"include_pil": False,
    	"expansion": False,
    	"name": "Application name",
    	"source": False,
    	"icon_name": "Application name",
    	"version": "1.0",
    	"store": "none",
    	"target_version": 14,
    	"permissions": ["VIBRATE"],
    	"include_sqlite": False,
    	"google_play_salt": None,
    	"numeric_version": "100"
    }
    config_file["package"] = f"{pack_name}"
    config_file["version"] = f"{str(version)}"
    config_file["name"] = f"{app_name}"
    config_file["icon_name"] = f"{app_name}"
    try:
        v = 0
        for i in version.split('.'):
            v *= 100
            v += int(i)

        config_file["numeric_version"] = f"{str(v)}"
    except:
        pass
    with open(os.path.join(folder,'.android.json'), 'w') as fp:
        json.dump(config_file, fp)

def rename_files(folder):
    print("Renaming files.....")
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):

        for fn in filenames + dirnames:
            src = os.path.join(dirpath, fn)
            dst = os.path.join(dirpath, fn.replace("x-",""))

            if os.path.exists(dst):
                continue

            rename(src, dst)
            print(f"Renamed {os.path.basename(src)} to {os.path.basename(dst)}")
    print("All files renamed.")

def rearrange_directory(folder):
    print("Putting everything back in it's place.....")
    game_dirs = os.listdir(os.path.join(folder,"assets"))
    # print(game_dirs)
    for x in game_dirs:
        rename(os.path.join(folder,"assets", x), os.path.join(folder, x))
    if os.path.isdir(os.path.join(folder,"res","drawable")):
        rename(os.path.join(folder,"res","drawable","icon.png"),os.path.join(folder,"android-icon.png"))
    if os.path.isdir(os.path.join(folder,"res","mipmap-xxhdpi-v4")):
        rename(os.path.join(folder,"res","mipmap-xxhdpi-v4","icon.png"),os.path.join(folder,"android-icon.png"))
        rename(os.path.join(folder,"res","mipmap-xxhdpi-v4","icon_background.png"),os.path.join(folder,"android-icon_background.png"))
        rename(os.path.join(folder,"res","mipmap-xxhdpi-v4","icon_foreground.png"),os.path.join(folder,"android-icon_foreground.png"))
    shutil.rmtree(os.path.join(folder,"assets"))
    shutil.rmtree(os.path.join(folder,"res"))
    print("Almost done......")

def decompile_rpyc_files(folder):
    print("Decrypting rpyc files....")
    for root, dirnames, filenames in os.walk(folder):
        for file in filenames:
            if file.endswith(".rpyc"):
                try:
                    os.system(f'win_unrpyc.exe "{os.path.join(root,file)}"')
                    print(file)
                except:
                    pass
    print ("All files decrypted")

def main(apk_file):
    apk = APK(apk_file)
    print(apk.application)
    print(apk.package)
    print(apk.version_name)
    folder = extract_apk(apk_file)
    create_android_json(folder, apk.application, apk.package, apk.version_name)
    rename_files(folder)
    rearrange_directory(folder)
    decompile_rpyc_files(folder)
    print("All done :-)")

if __name__ == "__main__":
    apk_file = askopenfilename(filetypes=[('Apk files', '*.apk'), ('All files', '*,*')])
    main(apk_file)
