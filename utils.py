import os
import stat
import shutil


def files_exist(fname):
    return os.path.isfile(fname)


def remove_not_empty_dir(name):
    for root, dirs, files in os.walk(name):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(name, ignore_errors=True)