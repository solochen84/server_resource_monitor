# -*- coding: utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from dingtalkchatbot.chatbot import DingtalkChatbot
from config import notify_dingding_webhooks


# 发送邮件函数
def send(content, subject, receiver):
    my_sender = '592750654@qq.com'
    my_pass = 'sbndswrkrjvrbfib'
    result = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["黄泽伟", my_sender])
        msg['Subject'] = subject
        msg['To'] = receiver
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.set_debuglevel(1)                     #和SMTP服务器的交互信息
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, receiver, msg.as_string())
        server.quit()
    except:
        result = False
    return result


# 使用钉钉机器人发送消息
def dingding(webhooks, msg):
    for webhook in webhooks:
        xiaoding = DingtalkChatbot(webhook)
        xiaoding.send_text(msg=msg, is_at_all=True)


# 使用钉钉机器人发送markdown消息
def send_mk_dingding(webhooks, msg_list):
    str = ''
    for msg in msg_list:
        str = str + '- ' + msg + '\n'
        print(msg)
    print(str)
    for webhook in webhooks:
        xiaoding = DingtalkChatbot(webhook)
        xiaoding.send_markdown(title='cloudtogo生产环境告警', text=str, is_at_all=True)


def monitor_notify_dingding(msg_lsit):
    send_mk_dingding(notify_dingding_webhooks, msg_lsit)


