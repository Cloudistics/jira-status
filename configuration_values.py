import json
import time

class ConfigurationValues:
    """
    Fetch configuration values from a JSON configuration file.
    """

    def __init__(self, json_file_path):
        """
        Look up the JSON values and initialize the class.
        """
        try:
            json_data = json.load(open(json_file_path))
        except (AttributeError, TypeError):
            raise AssertionError('JSON file path should be a string.')

        # Set configuration values from JSON file.
        self.jira_component = json_data['jiraComponent'].encode('utf-8')
        self.jira_url = json_data['jiraUrl'].encode('utf-8')
        self.jira_username = json_data['jiraUsername'].encode('utf-8')
        self.jira_password = json_data['jiraPassword'].encode('utf-8')
        self.jira_project_name = json_data['jiraProjectName'].encode('utf-8')
        self.jira_epics_to_track = [{ 'id': epic['id'].encode('utf-8'), \
            'name': epic['name'].encode('utf-8') } \
            for epic in json_data['jiraEpicsToTrack']]
        self.jira_labels_to_track = [label.encode('utf-8') \
            for label in json_data['jiraLabelsToTrack']] 
        self.log_formatter = json_data['logFormatter'].encode('utf-8')
        self.office_365_username = json_data['office365Username'].encode('utf-8')
        self.office_365_password = json_data['office365Password'].encode('utf-8')
        self.office_365_smtp_host = json_data['office365SmtpHost'].encode('utf-8')
        self.office_365_smtp_port = json_data['office365SmtpPort'].encode('utf-8')        
        self.email_from = json_data['emailFrom'].encode('utf-8')
        self.email_to = [email.encode('utf-8') for email in json_data['emailTo']] 
        self.email_subject = json_data['emailSubject'].encode('utf-8')
        
        # Save timestamp of script initialization.
        self.log_filename = json_data['logFilename'].encode('utf-8')
        if json_data['logFilenameAppendTimestamp']:
            self.log_filename += time.strftime("%Y%m%d-%H%M%S")
        self.log_filename += json_data['logFileExtension'].encode('utf-8')
