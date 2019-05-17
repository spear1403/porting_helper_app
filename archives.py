import os

def get_archive_files(gameDir):
    archives_list =[]
    for filename in os.listdir(gameDir):
        if filename.lower().endswith('.rpa'):
            archives_list.append(os.path.join(gameDir, filename))
    return archives_list
