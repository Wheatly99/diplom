import pandas as pd
from lab1 import final_score_lab1
from lab2 import final_score_lab2
from lab3 import final_score_lab3
from lab4 import final_score_lab4
from lab5 import final_score_lab5
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

    list_labs = [[lab1, final_score_lab1],
                 [lab2, final_score_lab2],
                 [lab3, final_score_lab3],
                 [lab4, final_score_lab4],
                 [lab5, final_score_lab5]]

    def add_score(lab, lab_score, final_score_lab, teams):
        lab = lab.merge(teams[teams[lab_score].isnull()], left_on='index', right_on='link_index', how='inner')[
            ['index', 'link']].drop_duplicates()
        lab[lab_score] = lab.link.apply(lambda x: final_score_lab(x))
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
