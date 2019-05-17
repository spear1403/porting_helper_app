import os

class Status(object):

    def count_files(dir):

        counter = [0,0,0,0,0,0]

        for root, dirnames, files in os.walk(dir):
            for file in files:
                if file.lower().endswith('.rpa'):
                    counter[0] += 1
                elif file.lower().endswith(('.png', '.bmp', '.jpg', '.jpeg', '.webp')):
                    counter[1] += 1
                elif file.lower().endswith(('.mp3','.ogg', '.wav')):
                    counter[2] += 1
                elif file.lower().endswith(('.avi','.mpg', '.m4v', '.ogv', '.mkv', '.mp4', '.webm')):
                    counter[3] += 1
                elif file.lower().endswith('.rpy'):
                    if not file.endswith('spear1403.rpy'):
                        counter[4] += 1
                elif file.lower().endswith('.rpyc'):
                    if not file.endswith('spear1403.rpyc'):
                        counter[5] += 1

        print(counter)
        return counter
