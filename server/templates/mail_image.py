# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

def prepare_email(user_email, matched_images):
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Your rockstar'
    me = 'csbishop@media.mit.edu'
    user = user_email
    msg['From'] = me
    msg['To'] = COMMASPACE.join(user)
    msg.preamble = 'Your rockstar is amazing!'

    # Assume we know that the image files are all in PNG format
    for file in matched_images:
        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        with open(file, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()