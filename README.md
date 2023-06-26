# periodic_quote_email
This Python script sends an email containing a quote randomly selected from the quotes.csv file. There is a log function to prevent the same quote being sent within the same week. The default saved quotes are chosen for to inspire, or to make the recipient think. Automation is done using crontab for MacOS and Linux or Scheduler for Windows. 

It is designed for use by Gmail email accounts. Credentials of the sender email account and recipients are stored in .env file. Recipients are BCC'd for privacy and the email is only addressed to the sender. The .env.example file is provided as a template for credentials and recipients. The password of the Gmail account is a generated 16-character App Password. Instructions to set up this App Password are found in Step 1 here: https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151. 

The CSV must contain two columns: Author and Text. Where the text of the quote should not include quotation marks.

Future development:
- Instructions for crontab/scheduler and pipelines