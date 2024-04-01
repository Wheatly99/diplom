import pandas as pd
from lab1 import final_score_lab1
from lab2 import final_score_lab2
from lab3 import final_score_lab3
from lab4 import final_score_lab4
from utils import remove_not_empty_dir
import os


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

    if ~lab1.empty:
        lab1 = lab1.merge(teams[teams.lab1_score.isnull()], left_on='index', right_on='link_index', how='inner')[
            ['index', 'link']].drop_duplicates()
        lab1['lab1_score'] = lab1.link.apply(lambda x: final_score_lab1(x))
        teams = teams.merge(lab1, left_on='link_index', right_on='index', how='left')

        teams['lab1_score'] = teams.lab1_score_x.combine_first(teams.lab1_score_y)
        teams = teams[
            ['group', 'full_name', 'link_index', 'lab1_score', 'lab2_score', 'lab3_score', 'lab4_score', 'lab5_score']]

    if ~lab2.empty:
        lab2 = lab2.merge(teams[teams.lab2_score.isnull()], left_on='index', right_on='link_index', how='inner')[
            ['index', 'link']].drop_duplicates()
        lab2['lab2_score'] = lab2.link.apply(lambda x: final_score_lab2(x))
        teams = teams.merge(lab2, left_on='link_index', right_on='index', how='left')

        teams['lab2_score'] = teams.lab2_score_x.combine_first(teams.lab2_score_y)
        teams = teams[
            ['group', 'full_name', 'link_index', 'lab1_score', 'lab2_score', 'lab3_score', 'lab4_score', 'lab5_score']]

    if ~lab3.empty:
        lab3 = lab3.merge(teams[teams.lab3_score.isnull()], left_on='index', right_on='link_index', how='inner')[
            ['index', 'link']].drop_duplicates()
        lab3['lab3_score'] = lab3.link.apply(lambda x: final_score_lab3(x))
        teams = teams.merge(lab3, left_on='link_index', right_on='index', how='left')

        teams['lab3_score'] = teams.lab3_score_x.combine_first(teams.lab3_score_y)
        teams = teams[
            ['group', 'full_name', 'link_index', 'lab1_score', 'lab2_score', 'lab3_score', 'lab4_score', 'lab5_score']]

    if ~lab4.empty:
        lab4 = lab4.merge(teams[teams.lab4_score.isnull()], left_on='index', right_on='link_index', how='inner')[
            ['index', 'link']].drop_duplicates()
        lab4['lab4_score'] = lab4.link.apply(lambda x: final_score_lab4(x))
        teams = teams.merge(lab4, left_on='link_index', right_on='index', how='left')

        teams['lab4_score'] = teams.lab4_score_x.combine_first(teams.lab4_score_y)
        teams = teams[
            ['group', 'full_name', 'link_index', 'lab1_score', 'lab2_score', 'lab3_score', 'lab4_score', 'lab5_score']]

    with pd.ExcelWriter(file_name, engine='openpyxl', mode="a", if_sheet_exists="replace") as writer:
        teams.to_excel(writer, "teams", index=False)
