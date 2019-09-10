from smsc_api import SMSC as smsc
import smtplib

def SMS(num,mes):
    #smsc.send_sms(num,mes)
    pass


def email(mail,message):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    tls = smtpObj.starttls()
    f = open('mail.txt', 'r')
    user = f.read()
    user = user.split()

    smtpObj.login(user[0],user[1])
    smtpObj.sendmail(user[0],mail,message)
    smtpObj.quit()

num = 'your phone'
mess = 'done'
SMS(num,mess)