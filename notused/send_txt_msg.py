import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    

    user = "orangepi899@outlook.com"
    msg['from'] = user
    password = "glean-convene-madman"

    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    email_alert("mobster", "thing", "5138007585@tmomail.net")
