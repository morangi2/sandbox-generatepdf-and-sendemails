#!/usr/bin/env python3 

from email.message import EmailMessage
import os.path
import mimetypes
import smtplib
import getpass

message = EmailMessage() # creates an empty email message

print(message) #printing gives us the string representation of the message object

sender = "xyz@gmail.com"
gpass = "gpass"
recepient = "mo@example.com"

message["From"] = sender
message["To"] = recepient

print(message)
"""OUTPUT from above is:::::
From: mj@example.com
To: mo@example.com


"""

message["Subject"] = "Greetings from {} to {}!".format(sender, recepient)
print(message)
"""OUTPUT from above is:::::
From: mj@example.com
To: mo@example.com
Subject: Greetings from mj@example.com to mo@example.com!


"""
#From, TO and Subject == Email Header fields
#       == key-value pairs used by the email client and email server to route and display th eemail

body = """Hey there!!

I'm learning to send email using Python!"""

message.set_content(body)
print(message)
"""OUTPUT from above is::::
From: mj@example.com
To: mo@example.com
Subject: Greetings from mj@example.com to mo@example.com!
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0

Hey there!!

I'm learning to send email using Python!
"""

# All about ATTACHEMENTS
# import mimetypes and os.path

att_path = "/~/doe.jpg"
att_filename = os.path.basename(att_path) 
mime_type, _ = mimetypes.guess_type(att_path) 

print(mime_type) #OUTPUT: image/jpeg == #MIME type and #MIME sub-type seperaqted by a /

#the EmailMessage obj needs a mime type and a subtype as seperate strings, so let's split it up
mime_type, mime_subtype = mime_type.split("/", 1) #seperator is / and number of splits is 1
print(mime_type) #OUTPUT: image
print(mime_subtype) #OUTPUT: jpeg

# ADD ATTACHEMENTS to the message
with open(att_path, 'rb') as ap:
    message.add_attachment(ap.read(), maintype = mime_type, subtype = mime_subtype, filename = os.path.basename(att_path))
print("Message with attachement...")
#print(message)

"""OUTPUT is:
Content-Type: multipart/mixed; boundary="===============5350123048127315795=="

--===============5350123048127315795==
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit

Hey there!

I'm learning to send email using Python!

--===============5350123048127315795==
Content-Type: image/png
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="example.png"
MIME-Version: 1.0

iVBORw0KGgoAAAANSUhEUgAAASIAAABSCAYAAADw69nDAAAACXBIWXMAAAsTAAALEwEAmpwYAAAg
AElEQVR4nO2dd3wUZf7HP8/M9k2nKIJA4BCUNJKgNJWIBUUgEggCiSgeVhA8jzv05Gc5z4KHiqin
eBZIIBDKIXggKIeCRCAhjQAqx4UiCARSt83uzDy/PzazTDZbwy4BnHde+9qZydNn97Pf5/uUIZRS
(...We deleted a bunch of lines here...)
wgAAAABJRU5ErkJggg==

--===============5350123048127315795==--
"""

# IMPORT smptlib to create an smtp server obj, then send messages to that server
# mail_server = smtplib.SMTP("localhost") #OUTPUT: is ConnectionRefusedError: [Errno 61] Connection refused

#check GMAIL on Google: Gmail SMTP connection settings
mail_server = smtplib.SMTP_SSL("smtp.gmail.com")
mail_server.set_debuglevel(1)

#import getpass and use it to prompt for a password
mail_pass = getpass.getpass("Password? ")
print(mail_pass)

mail_server.login(sender, mail_pass)
"""OUTPUT is:
Password? 
..........
send: 'ehlo 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa\r\n'
reply: b'250-smtp.gmail.com at your service, [184.149.38.6]\r\n'
reply: b'250-SIZE 35882577\r\n'
reply: b'250-8BITMIME\r\n'
reply: b'250-AUTH LOGIN PLAIN XOAUTH2 PLAIN-CLIENTTOKEN OAUTHBEARER XOAUTH\r\n'
reply: b'250-ENHANCEDSTATUSCODES\r\n'
reply: b'250-PIPELINING\r\n'
reply: b'250-CHUNKING\r\n'
reply: b'250 SMTPUTF8\r\n'
reply: retcode (250); Msg: b'smtp.gmail.com at your service, [184.149.38.6]\nSIZE 35882577\n8BITMIME\nAUTH LOGIN PLAIN XOAUTH2 PLAIN-CLIENTTOKEN OAUTHBEARER XOAUTH\nENHANCEDSTATUSCODES\nPIPELINING\nCHUNKING\nSMTPUTF8'
send: 'AUTH PLAIN AG1lcmN5b3JhbmdpMkBnbWFpbC5jb20AZ2d6dHZucm5weXNzZG52eA==\r\n'
reply: b'235 2.7.0 Accepted\r\n'
reply: retcode (235); Msg: b'2.7.0 Accepted'
"""

# ABove 1) connect to SMTP server (Gmail)
# ABove 2) authenticate with the server
# Below 3) send message
# Below 4) close conection with SMTP server

mail_server.send_message(message)
mail_server.quit()

# succesfully sent an email!!!!


# reusable methods
def generate(sender, recepient, subject, body, attachement_path):
    # CREATES and email with an attachment
    message = EmailMessage()
    #BASIC email formatting
    #message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recepient
    message["Subject"] = subject
    message.set_content(body)

    #PROCESS the attachement and add it to the email
    attachement_filename = os.path.basename(attachement_path)
    mime_type, _ = mimetypes.guess_type(attachement_path)
    mime_type, mime_subtype = mime_type.split("/", 1)

    with open(attachement_path, "rb") as ap:
        message.add_attachement(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=attachement_filename)

    return message

def send(message):
    # sends the email to the configured SMTP server
    mail_server = smtplib.SMTP("localhost")
    mail_server.send_message(message)
    mail_server.quit()





