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
            files_exist("data_preprocessing.py") and
            files_exist("model_preparation.py") and
            files_exist("model_testing.py") and
            files_exist("Jenkinsfile")):
        return 40
    else:
        return 0


def check_execute():
    """
    Проверка исполняемости файлов и наличия определенных строк в Jenkinsfile
    """
    if check_files() > 0:
        try:

            subprocess.run([sys.executable, "data_creation.py"])
            subprocess.run([sys.executable, "data_preprocessing.py"])
            subprocess.run([sys.executable, "model_preparation.py"])
            result = subprocess.run([sys.executable, "model_testing.py"], stdout=subprocess.PIPE)

            with open('Jenkinsfile') as f:
                if 'git' in f.read() and "Model test accuracy is: " in f"{result.stdout}":
                    return 20
                else:
                    return 0

        except Exception:
            return 0


def check_output_files():
    """
    Проверка выходных файлов
    """
    dir_name_train = "train"
    dir_name_test = "test"
    model_name = "model"
    try:
        if (os.listdir(dir_name_train) and
                os.listdir(dir_name_test) and
                len([file for file in os.listdir('.') if re.search(model_name, file)])):
            return 20
        else:
            return 0
    except Exception:
        return 0


def final_score_lab2(link):
    """
    Итоговый балл
    """
    subprocess.run(f"git clone {link} git_repo", stdout=subprocess.PIPE)
    subprocess.run(["pip3", "install", "-r", "git_repo/lab2/requirements.txt"], stdout=subprocess.PIPE)
    os.chdir("git_repo/lab2")

    final_score = check_files() + check_execute() + check_output_files()

    os.chdir("../..")

    remove_not_empty_dir('git_repo')

    return final_score
