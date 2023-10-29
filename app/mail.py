import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

mail=smtplib.SMTP_SSL('smtp.gmail.com',465)
mail.ehlo()
# mail.starttls()
username=os.getenv('MAIL_USERNAME')
password=os.getenv('MAIL_PASSWORD')
mail.login(username,password)
mail.sendmail(username,'omachonucodes@gmail.com','Subject:Email \n\n Hello this is an email ')
mail.quit()
print("successfully sent email please check your gmail.............")

