from fabric.api import run
import path


def listdir(dir_path):
    ls_output = run("ls -A %s" % dir_path)
    return ls_output.split()