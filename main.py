import pandas as pd
from utils import remove_not_empty_dir, final_score_lab
import os
import sys


if __name__ == '__main__':

    remove_not_empty_dir('git_repo')

    os.makedirs("git_repo")

    file_name = 'full_file.xlsx'

    teams = pd.read_excel(file_name, sheet_name='teams')
    lab1 = pd.read_excel(file_name, sheet_name='lab1')
    lab2 = pd.read_excel(file_name, sheet_name='lab2')
    lab3 = pd.read_excel(file_name, sheet_name='lab3')
    lab4 = pd.read_excel(file_name, sheet_name='lab4')
    lab5 = pd.read_excel(file_name, sheet_name='lab5')

    # Критерии проверки
    lab1_params = {"lab": "lab1",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "data_preprocessing.py", "model_preparation.py", "model_testing.py", "pipeline.sh"],

                   "max_score_check_execute": 15, "execute_files": [],
                   "get_output_file": "pipeline.sh",
                   "string_to_output": ["Model test accuracy is:"], "how_execute": "bash",

                   "max_score_dop_string": 0, "strings_in_file": [""], "files_to_check_string": [""],

                   "max_score_check_output": 15, "output_files": ["train", "test", "model.*"]}

    lab2_params = {"lab": "lab2",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "data_preprocessing.py", "model_preparation.py",
                                  "model_testing.py", "Jenkinsfile"],

                   "max_score_check_execute": 10, "execute_files": ["data_creation.py", "data_preprocessing.py",
                                                                    "model_preparation.py"],
                   "get_output_file": "model_testing.py",
                   "string_to_output": ["Model test accuracy is:",], "how_execute": sys.executable,

                   "max_score_dop_string": 5, "strings_in_file": ["git"], "files_to_check_string": ["Jenkinsfile"],

                   "max_score_check_output": 15, "output_files": ["train", "test", "model.*"]}

    lab3_params = {"lab": "lab3",

                   "max_score_check_files": 40,
                   "files_ness": ["*.py", "Dockerfile", "docker_pipeline.sh"],

                   "max_score_check_execute": 20, "execute_files": [],
                   "get_output_file": "docker_pipeline.sh",
                   "string_to_output": ["Model test accuracy is:"], "how_execute": "bash",

                   "max_score_dop_string": 0, "strings_in_file": [""], "files_to_check_string": [""],

                   "max_score_check_output": 0, "output_files": []}

    lab4_params = {"lab": "lab4",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "data_preprocessing.py", "data_update.py",
                                  "data_final.py", "*.dvc"],

                   "max_score_check_execute": 0, "execute_files": [],
                   "get_output_file": "",
                   "string_to_output": [""], "how_execute": "",

                   "max_score_dop_string": 20, "strings_in_file": ["md5: ", "size", "nfiles", "path", "url = "],
                   "files_to_check_string": ["data.dvc", ".dvc/config"],

                   "max_score_check_output": 0, "output_files": []}

    lab5_params = {"lab": "lab5",

                   "max_score_check_files": 40,
                   "files_ness": ["data_creation.py", "model_fit.py", "data_noise.py", "test_model.py"],

                   "max_score_check_execute": 15, "execute_files": ["data_creation.py", "model_fit.py",
                                                                    "data_noise.py"],
                   "get_output_file": "pytest",
                   "string_to_output": ["passed", "failedasd"], "how_execute": sys.executable,

                   "max_score_dop_string": 0, "strings_in_file": [""], "files_to_check_string": [""],

                   "max_score_check_output": 15, "output_files": ["data", "model.*"]}

    list_labs = [[lab1, lab1_params],
                 [lab2, lab2_params],
                 [lab3, lab3_params],
                 [lab4, lab4_params],
                 [lab5, lab5_params]]

    def add_score(lab, lab_score, lab_params, teams):
        lab = lab.merge(teams[teams[lab_score].isnull()], left_on='index', right_on='link_index', how='inner')[
            ['index', 'link']].drop_duplicates()
        lab[lab_score] = lab.link.apply(lambda x: final_score_lab(x, **lab_params))
        teams = teams.merge(lab, left_on='link_index', right_on='index', how='left')
        teams[lab_score] = teams[lab_score + '_x'].combine_first(teams[lab_score + '_y'])
        teams = teams[
            ['group', 'full_name', 'link_index', 'lab1_score', 'lab2_score', 'lab3_score', 'lab4_score', 'lab5_score']]
        return teams

    for number, lab in enumerate(list_labs):
        if ~lab[0].empty:
            teams = add_score(lab[0], f'lab{number + 1}_score', lab[1], teams)

    with pd.ExcelWriter(file_name, engine='openpyxl', mode="a", if_sheet_exists="replace") as writer:
        teams.to_excel(writer, "teams", index=False)
