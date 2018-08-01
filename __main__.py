"""
Log JiRA statistics based on the configuration.json file.
"""
from configuration_values import ConfigurationValues
from jira_logger import JiraLogger
from jira_status import JiraStatus
from office_365_client import Office365Client

import argparse
import os
import sys
import utility_path

MAIN_DIR = utility_path.get_main_dir()
GLOBAL_CONFIGURATION = ConfigurationValues(os.path.join(
    MAIN_DIR,
    'configuration.json'))


def main():
    """
    Execute when this module is called.
    """
    parser = argparse.ArgumentParser(
        description=('Collect statistics on the status of the configured '
                     'JiRA project.'))
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='output information about script to console')
    args = parser.parse_args()

    if args.verbose:
        print('Collecting JiRA status...\n')

    logger = JiraLogger(GLOBAL_CONFIGURATION.log_filename,
                        GLOBAL_CONFIGURATION.log_formatter)

    jira_instance = JiraStatus(GLOBAL_CONFIGURATION.jira_url,
                               GLOBAL_CONFIGURATION.jira_username,
                               GLOBAL_CONFIGURATION.jira_password,
                               logger,
                               args.verbose)

    jira_instance.get_bug_stats(logger, jira_instance,
                                GLOBAL_CONFIGURATION.jira_project_name,
                                GLOBAL_CONFIGURATION.jira_component,
                                GLOBAL_CONFIGURATION.jira_labels_to_track)

    jira_instance.get_epic_stats(logger, jira_instance,
                                 GLOBAL_CONFIGURATION.jira_project_name,
                                 GLOBAL_CONFIGURATION.jira_component,
                                 GLOBAL_CONFIGURATION.jira_epics_to_track)

    if args.verbose:
        # Read results.
        fp = open(os.path.join(
            MAIN_DIR,
            'logs',
            GLOBAL_CONFIGURATION.log_filename),
            'rb')
        msg = fp.read()
        fp.close()

        # Output stats to console.
        print(msg)
        print('You can find a copy of this information in the logs directory.')


if __name__ == '__main__':
    sys.exit(main())
