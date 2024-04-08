import os
import subprocess
import re
from utils import remove_not_empty_dir, files_exist
import sys


def check_files():
    """
    Проверка наличия файлов
    """
    if (files_exist("data_creation.py") and
            files_exist("model_fit.py") and
            files_exist("data_noise.py") and
            files_exist("test_model.py")):
        return 40
    else:
        return 0


def check_execute():
    """
    Проверка исполняемости файлов
    """
    if check_files() > 0:
        try:

            # with open('pipeline.sh') as file:
            #     filedata = file.read()
            # filedata = filedata.replace('python ', 'python3 ')
            # with open('pipeline.sh', 'w', newline='') as file:
            #     file.write(filedata)

            subprocess.run([sys.executable, "data_creation.py"])
            subprocess.run([sys.executable, "model_fit.py"])
            subprocess.run([sys.executable, "data_noise.py"])
            result = subprocess.run("pytest", stdout=subprocess.PIPE, shell=True).stdout
            if (b"failed" in result and
                    b"passed" in result):
                return 20
            else:
                return 0
        except Exception:
            return 0


def check_output_files():
    """
    Проверка выходных файлов
    """
    dir_name_data = "data"
    model_name = "model.*"
    try:
        if (os.listdir(dir_name_data) and
                files_exist(model_name)):
            return 20
        else:
            return 0
    except Exception:
        return 0


def final_score_lab5(link):
    """
    Итоговый балл
    """
    subprocess.run(f"git clone {link} git_repo", stdout=subprocess.PIPE)
    subprocess.run(["pip3", "install", "-r", "git_repo/lab5/requirements.txt"], stdout=subprocess.PIPE)
    os.chdir("git_repo/lab5")

    if check_files() == 0:
        final_score = 0
    else:
        final_score = check_files() + check_execute() + check_output_files()

    os.chdir("../..")

    remove_not_empty_dir('git_repo')

    return final_score
