import smtplib
from email.mime.text import MIMEText


class Email:
    def __init__(self):
        pass

    @staticmethod
    def send(to, subject, message):
        me = ''

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = to

        server = smtplib.SMTP(':')
        server.ehlo()
        server.starttls()
        server.login("", "")
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
