import os
import subprocess
import re
from utils import remove_not_empty_dir, files_exist
import glob


def check_files():
    """
    Проверка наличия файлов
    """
    if (files_exist("*.py") and
            files_exist("Dockerfile") and
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

            # with open('pipeline.sh') as file:
            #     filedata = file.read()
            # filedata = filedata.replace('python ', 'python3 ')
            # with open('pipeline.sh', 'w', newline='') as file:
            #     file.write(filedata)

            # Удаление каретки из файла
            with open("pipeline.sh", 'r') as file:
                content = file.read()
            with open("pipeline.sh", 'w', newline='\n') as file:
                file.write(content)

            result = subprocess.run("bash docker_pipeline.sh", stdout=subprocess.PIPE, shell=True)
            if "Model test accuracy is: " in f"{result.stdout}":
                return 20
            else:
                return 0
        except Exception:
            return 0


def additional_points():
    '''
    Дополнительные баллы за docker-compose и dockerhub
    '''
    add = 0
    if files_exist("docker-compose.*"):
        add += 10

    with open('docker_pipeline.sh') as file:
        content = file.read()
    if "docker push" in content:
        add += 10

    return add


def final_score_lab3(link):
    """
    Итоговый балл
    """
    subprocess.run(f"git clone {link} git_repo", stdout=subprocess.PIPE)
    subprocess.run(["pip3", "install", "-r", "git_repo/lab3/requirements.txt"], stdout=subprocess.PIPE)
    os.chdir("git_repo/lab3")

    if check_files() == 0:
        final_score = 0
    else:
        final_score = check_files() + check_execute() + additional_points()

    os.chdir("../..")

    remove_not_empty_dir('git_repo')

    return final_score
