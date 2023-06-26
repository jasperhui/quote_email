# decouple used for login credentials for sender email as well as email recipients
from decouple import config, Csv
# datetime used to retrieve current date
from datetime import date
# these packages are used to send the email securely
import smtplib
import ssl
from email.message import EmailMessage
# pandas is used to import the CSV and sample the quote
import pandas as pd
# os is used to read the CSV regardless of where the .py script is run
import os

# import these variables from .env file. Where email_sender is the gmail account that the emails will be sent from, 
# email_password is the app password to the aforementioned gmail account
# and email_receiver is a list of the email addresses that will receive the email
email_sender = config('email_sender', default='')
email_password = config('email_password', default='')
email_receiver = config('email_receiver', cast=Csv())
# separate the list of email recipeints with comma 
email_receiver_str = ", ".join(email_receiver)

# retrieve current date and set as the email subject line
today = date.today().strftime("%A %B %-d %Y")
subject = 'Daily Quote: ' + today

# retrieve absolute file path to properly read quote.csv regardless of where the script is run.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

# read quote CSV and retrieve random row for use in email
df_quotes = pd.read_csv(dname+'/quotes.csv')

# read log CSV to prevent duplicates during a week
df_log = pd.read_csv(dname+'/log.csv')

# left outer join with log to remove recent quotes
df = pd.merge(df_quotes, df_log, on = ['Text', 'Author'], how = "outer", indicator = True)
df = df[df['_merge'] == 'left_only']
df = df.drop(columns = ['_merge'])

# Select random quote
random_quote = df.sample().reset_index(drop =True)

# Append random quote to the log, if there are already 7 quotes in the log, delete the earliest quote

if len(df_log) >= 7:
    df_log = df_log.drop([0])

df_log = pd.concat([df_log, random_quote]).reset_index(drop=True)

# Export back the log to CSV for future usage
df_log.to_csv(dname+'/log.csv',index=False)

# Extract text and author string from row sampled and create body of email
quote = random_quote.loc[0, 'Text']
author = random_quote.loc[0, 'Author']

body = '"' + quote + '"' + '\n - ' + author

# Compose email message object, from and to email sender, with receipients on BCC 
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_sender
em['Subject'] = subject
em.set_content(body)

# SSL for security
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver + [email_receiver_str], em.as_string())