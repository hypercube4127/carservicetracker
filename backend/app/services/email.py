from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from app.models.confirm import Confirm
from app.models.user import User

class EmailSenderService:
  def __init__(self, smtp_server, smtp_port, sender, username, password, starttls):
    self.smtp_server = smtp_server
    self.smtp_port = smtp_port
    self.username = username
    self.password = password
    self.starttls = starttls
    self.sender = sender
    self.env = Environment(loader=FileSystemLoader('templates'))

  def send_email(self, to_email, subject, template_name, context):
    # Load the template
    template = self.env.get_template(template_name)
    body = template.render(context)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = self.username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Send the email
    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
      if self.starttls:
        server.starttls()
      server.login(self.username, self.password)
      server.sendmail(self.sender, to_email, msg.as_string())

  def send_confirm_email(self, confirm: Confirm):
    user: User = confirm.user
    self.send_email(
      to_email=user.email,
      subject="Confirm your email",
      template_name="confirm_email.html",
      context={
        'name': user.fullname,
        'confirmation_link': os.getenv('EXTERNAL_URL') + "/confirm/" + confirm.code,
        'current_year' : datetime.now().year
      }
    )