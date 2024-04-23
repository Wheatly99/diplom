import os
import stat
import shutil
import glob
import pandas as pd


def files_exist(fname):
    return glob.glob(fname)


def remove_not_empty_dir(name):
    for root, dirs, files in os.walk(name):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(name, ignore_errors=True)


def create_empty_excel_score_file():
    '''
    Создание пустого final_score.xlsx файла для наполнения баллами
    '''
    df_score = pd.DataFrame(columns=['group', 'full_name', 'link_index', 'lab1_score',
                                     'lab2_score', 'lab3_score', 'lab4_score', 'lab5_score'])
    df_labs = pd.DataFrame(columns=['index', 'link'])
    with pd.ExcelWriter('test.xlsx', engine='openpyxl') as writer:
        df_score.to_excel(writer, sheet_name='teams', index=False)
        df_labs.to_excel(writer, sheet_name='lab1', index=False)
        df_labs.to_excel(writer, sheet_name='lab2', index=False)
        df_labs.to_excel(writer, sheet_name='lab3', index=False)
        df_labs.to_excel(writer, sheet_name='lab4', index=False)
        df_labs.to_excel(writer, sheet_name='lab5', index=False)