import subprocess,os

def decompile_rpyc_files(gameDir):
    if os.path.isfile(os.path.splitext(file)[0] + ".rpy"):
                continue
            try:
                print("Processing {0}....({1}/{2})".format(file,counter,rpyc_count))
                cmd = subprocess.Popen("myunrpyc.exe "'"{0}"'"".format(file))
                cmd.wait()
            except:
                pass
        print ("all files decrypted")
