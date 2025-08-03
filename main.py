from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import find_dotenv,load_dotenv
import schedule
import time


env_file = find_dotenv()
load_dotenv(env_file)
SMTP_SERVER= os.getenv("SMTP_SERVER")
PORT = os.getenv("PORT")
USEREMAIL = os.getenv("USEREMAIL")
PASSWORD = os.getenv("PASSWORD")





def main():
    def getDataFromBrowser(url):
        content = 'Content of Hacker News for the day:\n'
        respose = requests.get(url)
        resposeContent = respose.content
        soup = BeautifulSoup(resposeContent,'html.parser')
        listElement = soup.find_all('span',attrs={"class": "titleline"})
        for i,tag in enumerate(listElement):
            content += f'{i+1}. {tag.text}\n'
        return content
    content = getDataFromBrowser('https://news.ycombinator.com/')

    recieverEmail = 'soyampaul34@gmail.com'
    body = content
    msg = MIMEMultipart()

    msg['Subject'] = 'Todays Hacker News'
    msg['From'] = USEREMAIL
    msg['To'] = recieverEmail
    msg.attach(MIMEText(body,'plain'))

    with smtplib.SMTP(SMTP_SERVER,PORT) as server:
        print("Mail is being send..")
        server.starttls()
        server.login(USEREMAIL,PASSWORD)
        server.sendmail(USEREMAIL,recieverEmail,msg.as_string())
    


schedule.every().day.at("10:00 ").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)