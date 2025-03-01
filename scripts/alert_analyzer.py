#!/usr/bin/env python3
"""
监控告警分析工具 v1.0
"""
import smtplib
import configparser
from email.mime.text import MIMEText
from datetime import datetime

# 配置读取
config = configparser.ConfigParser()
config.read('../config/smtp.ini')  # 实际配置文件不应提交

def send_alert(subject, content):
    """发送告警邮件"""
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = f"[ALERT] {subject}"
    msg['From'] = config['DEFAULT']['Sender']
    msg['To'] = ', '.join(config['DEFAULT']['Receivers'].split(','))

    with smtplib.SMTP(config['DEFAULT']['SMTPServer'], 
                     int(config['DEFAULT']['SMTPPort'])) as server:
        server.login(config['DEFAULT']['Username'], 
                    config['DEFAULT']['Password'])
        server.send_message(msg)

if __name__ == "__main__":
    # （实际应从监控系统获取数据）
    send_alert("CPU过载警告", f"[{datetime.now()}] CPU使用率超过90%")