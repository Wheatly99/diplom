import os
import subprocess
import psutil
from utils import files_exist, remove_not_empty_dir


def check_files(files_ness, max_score):
    cnt_files = len(files_ness)
    score = 0
    message = []
    for file in files_ness:
        if files_exist(file):
            score += max_score/cnt_files
        else:
            message.append(f"File {file} does not exist")
    return score, message


def check_execute(how_execute, execute_files, get_output_file, string_to_output, max_score, time_out):

    # Накопление обратной связи
    cnt_output_strings = len(string_to_output)
    cnt_execute_files = len(execute_files)
    message = []

    # Выполнение файлов по списку
    if execute_files:
        score = 0

        for file in execute_files:

            if files_exist(file):

                # Смена формата файла с Windows на Linux
                with open(file, 'r') as open_file:
                    content = open_file.read()
                with open(file, 'w', newline='\n') as open_file:
                    open_file.write(content)

                try:
                    result = subprocess.run(f"{how_execute} {file}", stderr=subprocess.PIPE, timeout=time_out, shell=True)
                    stderr = result.stderr
                except subprocess.TimeoutExpired:
                    stderr = 'cancel'

                if stderr == 'cancel':
                    message.append(f"The code execution time in the file {file} has expired ({time_out} seconds)")
                    return 0, message
                if not stderr:
                    score += max_score / cnt_execute_files
                elif stderr:
                    message.append(stderr)

            else:
                message.append(f"File {file} does not exist")

        # Если выходную строку не ищем
        if not get_output_file:
            return score, message
    # Получение строки в stdout у файла при необходимости
    if get_output_file:
        score = 0

        if files_exist(get_output_file) or (get_output_file == "pytest"):
            if get_output_file == "pytest":

                try:
                    result = subprocess.run(f"{get_output_file}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=time_out)
                    stdout = result.stdout
                    stderr = result.stderr
                except subprocess.TimeoutExpired:
                    message.append(f"The code execution time of pytest has expired ({time_out} seconds)")
                    return 0, message

                if stderr:
                    message.append(stderr)
            else:

                # Смена формата файла с Windows на Linux
                with open(get_output_file, 'r') as open_file:
                    content = open_file.read()
                with open(get_output_file, 'w', newline='\n') as open_file:
                    open_file.write(content)

                # Смена формата файла с Windows на Linux для ЛР3 (Docker)
                if files_exist('pipeline.sh'):
                    with open('pipeline.sh', 'r') as open_file:
                        content = open_file.read()
                    with open('pipeline.sh', 'w', newline='\n') as open_file:
                        open_file.write(content)

                try:
                    result = subprocess.run(f"{how_execute} {get_output_file}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=time_out, shell=True)
                    stdout = result.stdout
                    stderr = result.stderr
                except subprocess.TimeoutExpired:
                    message.append(f"The code execution time in the file {get_output_file} has expired ({time_out} seconds)")
                    return 0, message

                if b'DONE' not in stderr and stderr:
                    message.append(stderr)
            for string in string_to_output:
                if string in f"{stdout}":
                    score += max_score/cnt_output_strings
                else:
                    message.append(f"Output of {get_output_file} is not correct")
            return score, message
        else:
            message.append(f"File {get_output_file} does not exist")
            return 0, message

    message.append("Nothing to execute")
    return 0, message


def check_string_in_file(max_score, strings_in_file, files_to_check_string):
    cnt_words = len(strings_in_file)
    score = 0
    message = []
    for file in files_to_check_string:
        if files_exist(file):
            with open(file) as file_open:
                filedata = file_open.read()
            for string in strings_in_file:
                if string in filedata:
                    score += max_score/cnt_words
        else:
            message.append(f"File {file} does not exist")
    return score, message


def check_output_files(exist_files, max_score):
    count_ness_files = len(exist_files)
    score = 0
    message = []
    for file in exist_files:
            if files_exist(file):
                score += max_score / count_ness_files
            else:
                message.append(f"Output file {file} does not exist")
    return score, message


def final_score_lab(link, lab,

                    max_score_check_files, files_ness,

                    max_score_check_execute, execute_files, get_output_file, string_to_output, how_execute, time_out,

                    max_score_dop_string, strings_in_file, files_to_check_string,

                    max_score_check_output, output_files):
    """
    Итоговый балл
    """

    subprocess.run(["git", "clone", f"{link}", "git_repo"], stdout=subprocess.PIPE)

    root_files = f"git_repo/{lab}/requirements.txt"

    # Проверка на наличие директории и файла requirements.txt
    if not files_exist(root_files):
        return 0, [f"Directory {lab}/ or file requirements.txt does not exist"]

    subprocess.run(["pip3", "install", "-r", f"git_repo/{lab}/requirements.txt"], stdout=subprocess.PIPE)
    os.chdir(f"git_repo/{lab}")

    # Проверка наличия файлов
    if max_score_check_files > 0:
        score_check_files, message_check_files = check_files(files_ness=files_ness,
                                                             max_score=max_score_check_files)
    else:
        score_check_files, message_check_files = 0, []

    # Проверка исполняемости файлов
    if max_score_check_execute > 0:
        score_check_execute, message_check_execute = check_execute(how_execute=how_execute,
                                                                   execute_files=execute_files,
                                                                   get_output_file=get_output_file,
                                                                   string_to_output=string_to_output,
                                                                   max_score=max_score_check_execute,
                                                                   time_out=time_out)
    else:
        score_check_execute, message_check_execute = 0, []

    # Проверка наличия подстроки в файле
    if max_score_dop_string > 0:
        score_check_string_in_file, message_check_string_in_file = check_string_in_file(max_score=max_score_dop_string,
                                                                                        strings_in_file=strings_in_file,
                                                                                        files_to_check_string=files_to_check_string)
    else:
        score_check_string_in_file, message_check_string_in_file = 0, []

    # Проверка выходных файлов
    if max_score_check_output > 0:
        score_check_output_files, message_check_output_files = check_output_files(exist_files=output_files,
                                                                                  max_score=max_score_check_output)
    else:
        score_check_output_files, message_check_output_files = 0, []


    final_score = score_check_files + score_check_execute + score_check_string_in_file + score_check_output_files
    final_message = message_check_files + message_check_execute + message_check_string_in_file + message_check_output_files

    os.chdir("../..")

    # Необходимо для завершения процесса, если в одной из задач есть бесконечный цикл
    lst_stuck_proc = [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name', 'cwd'])
                      if ('wslhost.exe' in p.info['name']) and ('git_repo' in p.info['cwd'])]
    for pid in lst_stuck_proc:
        p = psutil.Process(pid)
        p.kill()

    remove_not_empty_dir('git_repo')

    # subprocess.run('docker system prune -af')

    # # Остановить докер с лабой и перенсти dockerfile_execute в текущую директорию
    # subprocess.run(f"docker stop {lab}", stdout=subprocess.PIPE, shell=True)
    # subprocess.run(f"docker rm --force {lab}", stdout=subprocess.PIPE, shell=True)
    return final_score, final_message