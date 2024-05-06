from utils import remove_not_empty_dir
from how_get_links import teams, yandex_forms
import os
import sys


if __name__ == '__main__':

    remove_not_empty_dir('git_repo')

    os.makedirs("git_repo")

    # Критерии проверки
    lab1_params = {"lab": "lab1",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "data_preprocessing.py", "model_preparation.py", "model_testing.py", "pipeline.sh"],

                   "max_score_check_execute": 15, "execute_files": [],
                   "get_output_file": "pipeline.sh",
                   "string_to_output": ["Model test accuracy is:"], "how_execute": "bash", "time_out": 20,

                   "max_score_dop_string": 0, "strings_in_file": [""], "files_to_check_string": [""],

                   "max_score_check_output": 15, "output_files": ["train", "test", "model.*"]}

    lab2_params = {"lab": "lab2",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "data_preprocessing.py", "model_preparation.py",
                                  "model_testing.py", "Jenkinsfile"],

                   "max_score_check_execute": 10, "execute_files": ["data_creation.py", "data_preprocessing.py",
                                                                    "model_preparation.py"],
                   "get_output_file": "model_testing.py",
                   "string_to_output": ["Model test accuracy is:",], "how_execute": sys.executable, "time_out": 300,

                   "max_score_dop_string": 5, "strings_in_file": ["git"], "files_to_check_string": ["Jenkinsfile"],

                   "max_score_check_output": 15, "output_files": ["train", "test", "model.*"]}

    lab3_params = {"lab": "lab3",

                   "max_score_check_files": 40,
                   "files_ness": ["*.py", "Dockerfile", "docker_pipeline.sh"],

                   "max_score_check_execute": 20, "execute_files": [],
                   "get_output_file": "docker_pipeline.sh",
                   "string_to_output": ["Model test accuracy is:"], "how_execute": "bash", "time_out": 600,

                   "max_score_dop_string": 0, "strings_in_file": [""], "files_to_check_string": [""],

                   "max_score_check_output": 0, "output_files": []}

    lab4_params = {"lab": "lab4",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "data_preprocessing.py", "data_update.py",
                                  "data_final.py", "*.dvc"],

                   "max_score_check_execute": 0, "execute_files": [],
                   "get_output_file": "",
                   "string_to_output": [""], "how_execute": "", "time_out": 300,

                   "max_score_dop_string": 20, "strings_in_file": ["md5: ", "size", "nfiles", "path", "url = "],
                   "files_to_check_string": ["data.dvc", ".dvc/config"],

                   "max_score_check_output": 0, "output_files": []}

    lab5_params = {"lab": "lab5",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "model_fit.py", "data_noise.py", "test_model.py"],

                   "max_score_check_execute": 15, "execute_files": ["data_creation.py", "model_fit.py",
                                                                    "data_noise.py"],
                   "get_output_file": "pytest",
                   "string_to_output": ["passed", "failed"], "how_execute": sys.executable, "time_out": 300,

                   "max_score_dop_string": 0, "strings_in_file": [""], "files_to_check_string": [""],

                   "max_score_check_output": 15, "output_files": ["data", "model.*"]}

    # Решение через файл, который будет размещен в teams
    teams(lab1_params, lab2_params, lab3_params, lab4_params, lab5_params)

    # Решение через яндекс форму
    # yandex_forms(lab1_params, lab2_params, lab3_params, lab4_params, lab5_params, flag_email=True)