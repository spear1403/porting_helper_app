import os
import struct
import shutil
from PIL import Image

def compress_media(file, quality=None, video=False, video_resize='720', image=False, audio=False, OS='Windows'):
    cwebp = 'cwebp'
    ffmpeg = 'ffmpeg'
    if OS=='Windows':
        cwebp = os.path.join('tools', 'cwebp.exe')
        ffmpeg = os.path.join('tools', 'ffmpeg.exe')
    if video_resize == None:
        vf_scale = ''
    else:
        vf_scale = '-vf scale=-1:720'
    minusSize = 0
    oldSize = os.path.getsize(file)
    tmpFile = file + '.temp'
    # print(tmpFile)
    print("{0}".format(file))
    if image:
        if file.lower().endswith('.webp'):
            print("found one")
            try:
                new_image = Image.open(file)
            except Exception as e:
                print(e)
                # webp header fix from bas@F95zone ###############
                b = os.path.getsize(file)-8
                c = struct.pack('<I', b)
                offset = 0o4
                with open(file, 'r+b') as f:
                    f.seek(offset)
                    f.write(c)
                ##################################################
                new_image = Image.open(file)
                print(new_image.getbands())
                new_image.save(file,'png')

        cmd = f'{cwebp} "{file}" -q {quality} -z 6 -mt -v -quiet -o "{tmpFile}"'
    elif audio:
        tmpFile = tmpFile + ".mp3"
        cmd = f'{ffmpeg} -i "{file}" -codec:a libmp3lame -loglevel warning -vn -qscale:a 7 "{tmpFile}"'
    elif video:
        tmpFile = tmpFile + ".webm"
        cmd = f'{ffmpeg} -y -i "{file}" {vf_scale} -c:v libvpx -pix_fmt yuv420p -loglevel warning -threads 2 -slices 8 -lag-in-frames 16 -auto-alt-ref 1 -c:a libvorbis -g 120 -level 216 -qmin {quality-3} -crf {quality} -qmax {quality+3} -b:v 0 -qscale:a 3 "{tmpFile}"'
    try:
        os.system(cmd)
        newSize = os.path.getsize(tmpFile)
        sizeReduction = oldSize - newSize
        if sizeReduction > 0:
            shutil.copyfile(tmpFile, file)
            minusSize += sizeReduction
            print(f'Size crunched: {sizeReduction}')
        else:
            print("Too big :-(")
    except:
        pass

    if os.path.isfile(tmpFile):
        os.remove(tmpFile)
    if os.path.isfile('ffmpeg2pass-0.log'):
        os.remove('ffmpeg2pass-0.log')
