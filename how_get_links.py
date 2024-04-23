import pandas as pd
from final_score import final_score_lab
from get_email_text import get_email_text, send_email


def yandex_forms(lab1_params, lab2_params, lab3_params, lab4_params, lab5_params):
    '''
    Получение работ студентов с Яндекс.Формы по почте
    '''
    list_works = get_email_text(mail_user='MarkinM99@mail.ru',
                                mail_pass='HMQTZRehXw7wvznWWEcC',
                                mail_subject='MLOps lab from Form',
                                main_dir='inbox')

    df_empty_score = pd.DataFrame(columns=['group', 'full_name', 'link_index', 'lab1_score',
                                           'lab2_score', 'lab3_score', 'lab4_score', 'lab5_score'])

    for number, work in enumerate(list_works):

        link_git_repo = work['git_link']
        lab_number = work['lab_number']
        lab_owner_name = work['FIO']
        lab_owner_group = work['group']
        email_to_send = work['mail_to']

        lab1_score = None
        lab2_score = None
        lab3_score = None
        lab4_score = None
        lab5_score = None

        if lab_number == "lab1":
            lab1_score = str(final_score_lab(link_git_repo, **lab1_params))
        elif lab_number == "lab2":
            lab2_score = str(final_score_lab(link_git_repo, **lab2_params))
        elif lab_number == "lab3":
            lab3_score = str(final_score_lab(link_git_repo, **lab3_params))
        elif lab_number == "lab4":
            lab4_score = str(final_score_lab(link_git_repo, **lab4_params))
        elif lab_number == "lab5":
            lab5_score = str(final_score_lab(link_git_repo, **lab5_params))

        score = pd.DataFrame({'group': lab_owner_group,
                              'full_name': lab_owner_name,
                              'link_index': number + 1,
                              'lab1_score': [lab1_score],
                              'lab2_score': [lab2_score],
                              'lab3_score': [lab3_score],
                              'lab4_score': [lab4_score],
                              'lab5_score': [lab5_score]})

        df_empty_score = pd.concat([df_empty_score, score], ignore_index=True)

        send_email(mail_user='MarkinM99@mail.ru',
                   mail_pass='HMQTZRehXw7wvznWWEcC',
                   mail_to=email_to_send,
                   mail_subject='MLOps lab score',
                   mail_text=f'''
                   Your points and comments for laboratory work {lab_number} is
                   {next(item for item in [lab1_score, lab2_score, lab3_score, lab4_score, lab5_score]
                         if item is not None)}
                   ''')

    df_empty_score = df_empty_score.groupby(['group', 'full_name'], as_index=False).last()

    with pd.ExcelWriter('test.xlsx', engine='openpyxl') as writer:
        df_empty_score.to_excel(writer, "teams", index=False)






def teams(lab1_params, lab2_params, lab3_params, lab4_params, lab5_params):
    '''
    Получение работ студентов с teams и выставление оценок с комментариями
    Предварительно должен быть файл full_file.xlsx в папке проекта
    с вкладками teams и лабораторными, такими как lab1, lab2, lab3 и т.д.
    Пример файла лежит в git-репозитории данного проекта
    '''

    file_name = 'full_file.xlsx'

    teams = pd.read_excel(file_name, sheet_name='teams')
    lab1 = pd.read_excel(file_name, sheet_name='lab1')
    lab2 = pd.read_excel(file_name, sheet_name='lab2')
    lab3 = pd.read_excel(file_name, sheet_name='lab3')
    lab4 = pd.read_excel(file_name, sheet_name='lab4')
    lab5 = pd.read_excel(file_name, sheet_name='lab5')

    list_labs = [[lab1, lab1_params],
                 [lab2, lab2_params],
                 [lab3, lab3_params],
                 [lab4, lab4_params],
                 [lab5, lab5_params]]

    def add_score_teams(lab, lab_score, lab_params, teams):
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
            teams = add_score_teams(lab[0], f'lab{number + 1}_score', lab[1], teams)

    with pd.ExcelWriter(file_name, engine='openpyxl', mode="a", if_sheet_exists="replace") as writer:
        teams.to_excel(writer, "teams", index=False)