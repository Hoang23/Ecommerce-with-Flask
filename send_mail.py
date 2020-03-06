import smtplib
from email.mime.text import MIMEText # allows to parse in html

def send_mail(name, email, message):
    # enable less secure apps (https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp)
    user = '<email>'
    password = '<pw>'
    message = f"<h3>New message</h3> <br> name: {name} <br> email: {email} <br> message: {message}"

    sender_email = email
    receiver_email = '<email>'
    msg = MIMEText(message, 'html') # can use either html or txt    
    msg['Subject'] = 'New Message'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.close()
    print ('successfully sent the mail')
    # except:
    #     print ("failed to send mail")
