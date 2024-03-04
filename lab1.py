import os
import subprocess
import re

os.chdir("git_repo/lab1")


def files_exist(fname):
    return os.path.isfile(fname)


def check_files():
    """
    Проверка наличия файлов
    """
    if (files_exist("data_creation.py") and
            files_exist("data_preprocessing.py") and
            files_exist("model_preparation.py") and
            files_exist("model_testing.py") and
            files_exist("pipeline.sh")):
        return 40
    else:
        return 0


def check_execute():
    """
    Проверка исполняемости файлов
    """
    if check_files() > 0:
        try:

            with open('pipeline.sh') as file:
                filedata = file.read()
            filedata = filedata.replace('python ', 'python3 ')
            with open('pipeline.sh', 'w', newline='') as file:
                file.write(filedata)

            result = subprocess.run("bash pipeline.sh", stdout=subprocess.PIPE, shell=True)
            if "Model test accuracy is: " in f"{result.stdout}":
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


def final_score_lab1():
    """
    Итоговый балл
    """
    final_score = check_files() + check_execute() + check_output_files()
    return final_score
