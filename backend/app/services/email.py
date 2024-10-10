from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from app.models.confirm import Confirm, ConfirmType
from app.models.user import User
import asyncio

from app import db

class EmailSenderService:

  _instance = None

  @staticmethod
  def get_instance(smtp_server=None, smtp_port=None, sender=None, username=None, password=None, starttls=None):
    if EmailSenderService._instance is None:

      EmailSenderService._instance = EmailSenderService(
        smtp_server=os.getenv('SMTP_SERVER'),
        smtp_port=int(os.getenv('SMTP_PORT')),
        username=os.getenv('SMTP_USERNAME'),
        password=os.getenv('SMTP_PASSWORD'),
        starttls=os.getenv('SMTP_STARTTLS').lower() == 'true',
        sender=os.getenv('SMTP_SENDER')
      )
    return EmailSenderService._instance


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

  def send_confirm_emails(self):
    asyncio.run(self.async_send_confirm_emails())

  async def async_send_confirm_emails(self):
    unhandled_confirms = Confirm.query.filter_by(email_sent_at=None).all()
    for confirm in unhandled_confirms:
      confirm: Confirm = confirm
      context = {
        'name' : confirm.name,
        'confirmation_link': os.getenv('EXTERNAL_URL') + "/confirm/" + str(confirm.code),
        'current_year' : datetime.now().year
      }
      template_name = None
      subject = None
      if confirm.type == ConfirmType.CONFIRM_EMAIL:
        template_name="confirm_email.html"
        subject="Confirm your email"
      elif confirm.type == ConfirmType.MODIFY_EMAIL:
        template_name="modify_email.html"
        subject="Email change confirmation"
      else:
        raise Exception(f"Unhandled confirm type {confirm.type}")

      self.send_email(
        to_email=confirm.email,
        subject=subject,
        template_name=template_name,
        context=context
      )
      confirm.email_sent_at = datetime.now()
      db.session.add(confirm)
      db.session.commit()

    