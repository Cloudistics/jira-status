"""
Client for initializing a connection to an Office 365 server and sending
email messages.
"""
from email.mime.text import MIMEText
import smtplib

class Office365Client:
  """
  Send email messages via Office 365 server.
  """

  def __init__(self, smtp_host, smtp_port, username, password):
    """
    Initialize configuration properties.
    """
    self._smtp_host = smtp_host
    self._smtp_port = smtp_port
    self._username = username
    self._password = password

  def send_msg(self, msg_from, msg_to, msg_subject, msg, is_html_msg):
    """
    Send a message using the configured properties.
    """
    # Initialize MIME message.
    if is_html_msg:
      mime_msg = MIMEText(msg, 'html')
    else:
      mime_msg = MIMEText(msg)
    mime_msg['Subject'] = msg_subject
    mime_msg['From'] = msg_from
    mime_msg['To'] = ", ".join(msg_to)

    mail_server = smtplib.SMTP(self._smtp_host, self._smtp_port)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(self._username, self._password)
    mail_server.sendmail(msg_from, msg_to, mime_msg.as_string())
    mail_server.quit()
