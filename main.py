from utils import remove_not_empty_dir
from how_get_links import teams, yandex_forms
import os
import sys
import json


if __name__ == '__main__':

    remove_not_empty_dir('git_repo')

    os.makedirs("git_repo")

    # Критерии проверки
    with open('config/lab1_cond.json') as json_file:
        lab1_params = json.load(json_file)
    with open('config/lab2_cond.json') as json_file:
        lab2_params = json.load(json_file)
    with open('config/lab3_cond.json') as json_file:
        lab3_params = json.load(json_file)
    with open('config/lab4_cond.json') as json_file:
        lab4_params = json.load(json_file)
    with open('config/lab5_cond.json') as json_file:
        lab5_params = json.load(json_file)

    # Решение через файл, который будет размещен в teams
    teams(lab1_params, lab2_params, lab3_params, lab4_params, lab5_params)

    # Запуск докера
    # docker build -t lab_check_score .
    # docker run -v "//var/run/docker.sock:/var/run/docker.sock" --privileged --name lab_check_score lab_check_score
    # docker cp lab_check_score:/app/full_file.xlsx .

    # Решение через яндекс форму
    # yandex_forms(lab1_params, lab2_params, lab3_params, lab4_params, lab5_params, flag_email=True)