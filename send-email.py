"""
Send an email message via Office 365 based configuration.json file and
supplied arguments.
"""
from configuration_values import ConfigurationValues
from office_365_client import Office365Client
from utility_path import is_valid_file

import argparse
import os
import utility_path

MAIN_DIR = utility_path.get_main_dir()
GLOBAL_CONFIGURATION = ConfigurationValues(os.path.join(
    MAIN_DIR,
    'configuration.json'))


def main():
    """
    Send email when this module is called.
    """
    parser = argparse.ArgumentParser(
        description=('Send an email using Office365 client.'))
    
    parser.add_argument('-f', '--filename', dest='filename', required=True,
                    help='File containing the email message body.', metavar='FILE',
                    type=lambda x: is_valid_file(parser, x))
    
    parser.add_argument('-html', action='store_true',
                            help='Send the email in HTML format.')                    
    
    args = parser.parse_args()

    msg = args.filename.read()
    args.filename.close()

    mail_client = Office365Client(GLOBAL_CONFIGURATION.office_365_smtp_host,
                                GLOBAL_CONFIGURATION.office_365_smtp_port,
                                GLOBAL_CONFIGURATION.office_365_username,
                                GLOBAL_CONFIGURATION.office_365_password)

    mail_client.send_msg(GLOBAL_CONFIGURATION.email_from,
                        GLOBAL_CONFIGURATION.email_to,
                        GLOBAL_CONFIGURATION.email_subject,
                        msg,
                        args.html)

if __name__ == '__main__':
  main() 