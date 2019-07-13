import os
import shutil
import subprocess

class Definitions():

    def counting_files(folder, *ext):
        count = 0
        for root, dirnames, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(ext):
                    count += 1
        print('\nCounted {0} {1} files\n'.format(count, ext))
        return (count)

    def listing_files(folder, *ext):
        file_list = []
        for root, dirnames, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(ext):
                    file_list.append(os.path.join(root,file))
        return (file_list)

    def open_rpy_for_edit(gameDir, opsis):
        if opsis == 'Windows':
            txt_editor_cmd = "start notepad++"
        if opsis == 'Linux':
            txt_editor_cmd = "geany"
        for root, dirnames, files in os.walk(gameDir, topdown=True):
            #print(dirnames)
            dirnames[:] = [d for d in dirnames if d not in 'tl']
            for file in files:
                if file.lower().endswith('.rpy'):
                    rpyFile = os.path.join(root, file)
                    if not file == "asset-index.rpy":
                        try:
                            os.popen(f'{txt_editor_cmd} "{rpyFile}"')
                        except:
                            print("No supported text editor found ... :-(")
                            break

    def hover_button_copy(gameDir):
        phone_dir = os.path.join(gameDir, 'gui', 'phone', 'button')
        #print(phone_dir)
        if os.path.exists(phone_dir):
            print('>>>Copying choice buttons to the phone folder')
            idle = os.path.join(gameDir, 'gui', 'button', 'choice_idle_background.png')
            hover = os.path.join(gameDir, 'gui', 'button', 'choice_hover_background.png')
            try:
                shutil.copy(idle, phone_dir)
                shutil.copy(hover, phone_dir)
            except:
                pass
        else:
            print('>>>No button folder in phone folder')

    def icon_copy(dir):
        icon_names = ['icon.png', 'win_icon.png', 'logo.png', 'window_icon2.png', 'window_icon_2.png'
                        , 'window_icon.png']
        images_dir = os.path.join(dir, 'images')
        gui_dir = os.path.join(dir, 'gui')
        icon = os.path.join('images', 'android-icon.png')

        for icon_file in icon_names:
            if os.path.isfile(os.path.join(gui_dir, icon_file)):
                icon = os.path.join(gui_dir, icon_file)
                break
            elif os.path.isfile(os.path.join(images_dir, icon_file)):
                icon = os.path.join(images_dir, icon_file)
                break

        print('>>>Copying android icon to game directory')
        icon_file = os.path.join(dir.split("game")[0], 'android-icon.png')
        # icon_file_gradle = os.path.join(dirOpen, 'android-icon_foreground.png')
        shutil.copyfile(icon, icon_file)
        # shutil.copyfile(icon, icon_file_gradle)
        return icon

    def delete_lib_renpy(dir):
        lib_dir = os.path.join(os.path.dirname(dir), 'lib')
        if os.path.isdir(lib_dir):
            shutil.rmtree(lib_dir)
        renpy_dir = os.path.join(os.path.dirname(dir), 'renpy')
        if os.path.isdir(renpy_dir):
            shutil.rmtree(renpy_dir)
