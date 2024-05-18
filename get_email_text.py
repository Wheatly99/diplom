import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_email_text(mail_user, mail_pass, main_dir, mail_subject):

    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login(mail_user, mail_pass)
    mail.select(main_dir)

    result, data = mail.uid('search', None, f'(SUBJECT "{mail_subject}")')

    if result == 'OK':

        all_msg = []

        for num in data[0].split():

            result, data = mail.uid('fetch', num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Получение тела письма
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True).decode(part.get_content_charset())
                    lst_body = body.split('<pre style="white-space:pre-wrap;">')[1].split('&#x27;')[1:-1:2]
                    json_body = [{lst_body[0]: lst_body[1],
                                  lst_body[2]: lst_body[3],
                                  lst_body[4]: lst_body[5],
                                  lst_body[6]: lst_body[7],
                                  lst_body[8]: lst_body[9]}]
                    all_msg += json_body

    mail.close()
    mail.logout()

    return all_msg


def send_email(mail_user, mail_pass, mail_to, mail_subject, mail_text):

    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()
    server.login(mail_user, mail_pass)

    msg = MIMEMultipart()
    msg['From'] = mail_user
    msg['To'] = mail_to
    msg['Subject'] = mail_subject

    msg.attach(MIMEText(mail_text, 'plain'))

    text = msg.as_string()
    server.sendmail(mail_user, mail_to, text)

    server.quit()
