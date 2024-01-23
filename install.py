import os
import sys

def check_os():
    if sys.platform.startswith("win"):
        return "window"
    elif sys.platform.starstwith("linux"):
        return "linux"
    else:
        return "unknown"

def runner_create():
    file = open("/usr/local/bin/iha089ftp",'w')
    file.write("#!/bin/bash")
    file.write("\n")
    file.write("python3 /usr/share/ihaahi/iha089ftp/start.py")
    file.close()
    os.system("chmod +x /usr/local/bin/iha089ftp")
    print("type `iha089ftp` to start this script\n")



def iha089_dir():
    dir_path = "/usr/share/ihaahi"
    if not os.path.exists(dir_path) and os.path.isdir(dir_path):
        os.mkdir("/usr/share/ihaahi")

def check_root():
    return os.geteuid() == 0

def get_working_dir():
    return os.getcwd()


if __name__=="__main__":
    if check_os == "linux":
        if check_root():
            iha089_dir()
            pwd = get_working_dir()
            print(pwd)
            cmd = "mv {} /usr/share/ihaahi".format(pwd)
            os.system(cmd)
            runner_create()
        else:
            print("Please run with root\n")
elif check_os == "window":
    print("comming soon....\n")
else:
    print("This tool is not supproted by your Operating system.\n")
    


    
