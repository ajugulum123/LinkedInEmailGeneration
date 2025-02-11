import pandas as pd
import smtplib
from email.message import EmailMessage
import time
from datetime import datetime

# server creds
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASSWORD = input("Enter your Gmail-App password: ")
SENDER_EMAIL = input("Enter your email: ")

# read the CSV file
df_contacts = pd.read_csv('contacts.csv')

# inputs for personalized message
para_one = input('Please input para 1: ')
para_two = input('Please input para 2: ')
para_three = input('Please input para 3: ')
signature = input('Please input Your Email Signature: ')

# function to send email
def send_email(recipient_email, recipient_name):
    # create email content
    template = f"""
               <html>
               <body>
                   <p>Hi {recipient_name},</p>
                   <p>
                       {para_one} <br>
                   </p>
                   <p>
                        {para_two} <br>
                   </p>
                   <p>
                       {para_three}
                   </p>
                   <p>
                       Best regards,<br>
                       {signature}
                   </p>
               </body>
               </html>
               """

    # create email message
    email = EmailMessage()
    email["From"] = SENDER_EMAIL
    email["To"] = recipient_email
    email["Subject"] = "Student Seeking Advice"
    email.set_content(template, subtype='html')

    # add pdf
    pdf_path = input("Enter the Path name for the PDF file: ")
    with open(pdf_path, 'rb') as pdf_file:
        email.add_attachment(pdf_file.read(), maintype='application', subtype='pdf', filename='AarohJugulumResume.pdf')

    try:
        # connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SMTP_PASSWORD)
            smtp.send_message(email)
            print(f"Email sent to {recipient_email} successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to send email to {recipient_email}. Authentication Error: {e}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}. Error: {e}")


# function to schedule email
def schedule_email(recipient_email, recipient_name, send_time):
    current_time = datetime.now()
    time_difference = (send_time - current_time).total_seconds()
    if time_difference > 0:
        print(f"Waiting {time_difference} seconds to send email to {recipient_email}")
        time.sleep(time_difference)
    send_email(recipient_email, recipient_name)


# user inputs
schedule_choice = input("Do you want to schedule the email send? (yes/no): ").strip().lower()

# if case: yes
if schedule_choice == 'yes':
    month = int(input('Enter the month (1-12): ').strip())
    day = int(input('Enter the day (1-31): ').strip())
    hour = int(input('Enter the hour (0-23): ').strip())
    minute = int(input('Enter the minute (0-59): ').strip())

    # specify the schedule time for the current year
    current_year = datetime.now().year
    scheduled_time = datetime(current_year, month, day, hour, minute, 0)
else:
    # send immediately if no
    scheduled_time = datetime.now()

# send emails
for index, row in df_contacts.iterrows():
    recipient_email = row['Email']
    recipient_name = row['Name']
    schedule_email(recipient_email, recipient_name, scheduled_time)

# output message if process was completed well
print("Email sending process completed.")