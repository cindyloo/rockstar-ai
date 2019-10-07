# Import smtplib for the actual sending function
import smtplib
import os
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
print(PROJECT_HOME)
#PROJECT_HOME = os.sys.path[0] #not safe
#print(PROJECT_HOME)
SERVER_FOLDER = '{}/server'.format(os.path.dirname(os.path.realpath(__file__)))
IMAGE_FOLDER = '{}/static/'.format(SERVER_FOLDER)

def prepare_email(user_email, matched_images):
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    rockstar_email = 'rockstar.ai.rockelganger@gmail.com'
    rockstar_pwd = 'Petrock1!'

    #TODO verify user_email
    msg['From'] = rockstar_email
    msg['To'] = user_email
    msg['Subject'] = "You are a Rockstar! Here's your proof"
    from_text = MIMEText("Thanks, come rock out again at rockstar-ai.com!", 'plain')
    # Assume we know that the image files are all in PNG format
    for file in [matched_images]:
        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        file = '{}{}'.format(IMAGE_FOLDER,file)
        with open(file, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)

    rockstar_file = '{}/templates/rockstar_text.png'.format(SERVER_FOLDER, file)
    with open(rockstar_file, 'rb') as fp:
        logo = MIMEImage(fp.read())
    msg.attach(logo)
    msg.attach(from_text)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(rockstar_email, rockstar_pwd)
    s.sendmail(rockstar_email, [user_email], msg.as_string())
    #s.send_message(msg)
    s.quit()
    return "success"