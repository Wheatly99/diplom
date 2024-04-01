import os
import subprocess
import re
from utils import remove_not_empty_dir, files_exist


def check_files():
    """
    Проверка наличия файлов
    """
    if (files_exist("data_creation.py") and
            files_exist("data_preprocessing.py") and
            files_exist("data_update.py") and
            files_exist("data_final.py") and
            files_exist("*.dvc")):
        return 40
    else:
        return 0

def check_data_control():
    """
    Проверка версионирования данных
    """
    try:
        with open('data.dvc') as file:
            content = file.read()
        if ("md5: " in content and
            "size" in content and
            "nfiles" in content and
            "path" in content):
            return 20
    except:
        return 0


def check_remote():
    """
    Проверка удаленного хранилища
    """
    try:
        with open('.dvc/config') as file:
            content = file.read()
        if "url = " in content:
            return 20
    except:
        return 0


def final_score_lab4(link):
    """
    Итоговый балл
    """
    subprocess.run(f"git clone {link} git_repo", stdout=subprocess.PIPE)
    subprocess.run(["pip3", "install", "-r", "git_repo/lab4/requirements.txt"], stdout=subprocess.PIPE)
    os.chdir("git_repo/lab4")

    if check_files() == 0:
        final_score = 0
    else:
        final_score = check_files() + check_data_control() + check_remote()

    os.chdir("../..")

    remove_not_empty_dir('git_repo')

    return final_score
