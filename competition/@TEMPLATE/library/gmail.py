import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


class GMail:

    def __init__(self, user_address: str|None, user_password: str|None):
        user_address = user_address if user_address else os.environ.get("GOOGLE_USER_ADDRESS")
        user_password = user_address if user_address else os.environ.get("GOOGLE_USER_PASSWORD")
        self._user_address = user_address
        self._user_password = user_password

    def send_mail(self, send_address: str|None, subject: str, body: str = "", crown_name: str = "[Colab]") -> None:
        send_address = send_address if send_address is not None else self._user_address

        # SMTPサーバに接続
        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpobj.starttls()
        smtpobj.login(self._user_address, self._user_password)

        # メール作成
        msg = MIMEText(body)
        msg['Subject'] = crown_name + subject
        msg['From'] = self._user_address
        msg['To'] = send_address
        msg['Date'] = formatdate()

        # 作成したメールを送信
        smtpobj.send_message(msg)
        smtpobj.close()
