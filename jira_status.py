"""
Connects to an instance of JiRA and log statistics.
"""
from collections import defaultdict
from jira import JIRA

import utility_math


class JiraStatus:
    """
    Connect to an instance of JiRA and collects statistics.
    """
    MAX_QUERY_RESULT_SIZE = 1000

    def __init__(self, jira_server, jira_username, jira_password, logger,
                 is_verbose):
        """
        Initialize the class.
        """
        self._jira_server = jira_server
        self._jira_username = jira_username
        self._jira_password = jira_password
        self._logger = logger
        self._is_verbose = is_verbose

        # Establish connection.
        self._jira_instance = self._connect()

    def _connect(self):
        """
        Connect to the JiRA instance.
        """
        print('Connecting to JiRA...\n')
        try:
            self._logger.debug("Connecting to JiRA: %s" % self._jira_server)

            # Disable SSL Certificate Verification.
            jira_options = {
                'server': self._jira_server
            }

            # Connect.
            jira = JIRA(options=jira_options, basic_auth=(
                self._jira_username, self._jira_password))

            if self._is_verbose:
                print('Successfully connected to JiRA...\n')
            self._logger.debug('Successfully connected to JiRA: {0}'.format(
                self._jira_server))
            return jira
        except Exception as e:
            if self._is_verbose:
                print('Failure connecting to JiRA...\n')
            self._logger.error('Failed to connect to JiRA: {0}'.format(e))

    def get_bug_stats(self, logger, jira_instance, project, component,
                      labels_to_track):
        """
        Collect statistics on bugs in the project by component.
        Conditionally collect statistics on bugs by label, if labels parameter 
        set.
        """
        project_bugs = jira_instance.search_issues(
            ('project = {0} AND status = Open AND type = Bug ORDER BY priority '
             'DESC').format(project))

        component_bugs = jira_instance.search_issues(
            ('project = {0} AND component in ({1}) AND status = Open '
             'AND type = Bug ORDER BY priority DESC')
            .format(project, component))

        component_bugs_created_this_week = jira_instance.search_issues(
            ('project = {0} AND component in ({1}) AND type = Bug AND '
             'createdDate > startOfWeek() ORDER BY priority DESC')
            .format(project, component))

        logger.info(('\'bugStatus\': [There are {0} open bugs in {1}. '
                     'This is {2}% of the open bugs in {3} ({4} total open bugs'
                     ').,')
                    .format(len(component_bugs), component,
                            utility_math.get_percentage(
                        len(component_bugs), len(project_bugs)), project,
            len(project_bugs)))

        logger.info('{0} bug(s) have been created this week.,'.format(
            len(component_bugs_created_this_week)))

        bugs_by_priority = defaultdict(list)
        bugs_by_label = defaultdict(list)

        # Collect detailed information on each bug.
        for bug in component_bugs:
            # Get bug priority level.
            priority = bug.fields.priority
            bugs_by_priority['{0}'.format(priority)].append(bug)

            # Get bug labels.
            labels = bug.fields.labels

            for label in labels:
                label_str = label.encode('utf-8')
                if label_str in labels_to_track:
                    bugs_by_label['{0}'.format(label_str)].append(bug)

        # Print information about priority level.
        for key in bugs_by_priority:
            logger.info('There are {0} bug(s) with priority level {1},'.format(
                len(bugs_by_priority[key]), key))

        # Print information about bugs with labels of interest.
        for key in bugs_by_label:
            logger.info('There are {0} bug(s) with label {1}.,'.format(
                len(bugs_by_label[key]), key))

        logger.info(']')

    def get_epic_stats(self, logger, jira_instance, project, component,
                       epics_to_track):
        """
        Collect statistics on epics by component.
        """
        for epic in epics_to_track:
            stories = jira_instance.search_issues(
                ('project = {0} AND component in ({1}) AND type = Story AND '
                 '"Epic Link" = {2}')
                .format(project, component, epic['id']))

            completed_stories = jira_instance.search_issues(
                ('project = {0} AND component in ({1}) AND type = Story AND '
                 'status not in (Open, "In Progress", "Code Review Ready") AND '
                 '"Epic Link" = {2}')
                .format(project, component, epic['id']))

            stories_in_code_review = jira_instance.search_issues(
                ('project = {0} AND component in ({1}) AND type = Story AND '
                 'status = "Code Review Ready" AND "Epic Link" = {2}')
                .format(project, component, epic['id']))

            incomplete_stories = len(stories) - \
                len(completed_stories)

            logger.info(('\'{3}\': [There are {0} open stories out of {1} total '
                         'stories for component {2} in epic {3}.,')
                        .format(incomplete_stories, len(stories),
                                component, epic['name']))

            total_story_points = 0
            for story in stories:
                if story.fields.customfield_10004 is not None:
                    total_story_points += story.fields.customfield_10004

            completed_story_points = 0
            for story in completed_stories:
                if story.fields.customfield_10004 is not None:
                    completed_story_points += story.fields.customfield_10004

            code_review_story_points = 0
            for story in stories_in_code_review:
                if story.fields.customfield_10004 is not None:
                    code_review_story_points += story.fields.customfield_10004

            incomplete_story_points = total_story_points - completed_story_points

            logger.info(('There are {0} story points out of {1} that need to be '
                         'completed for component {2} in epic {3}.,')
                        .format(incomplete_story_points, total_story_points, component,
                                epic['name']))

            logger.info('The {0} is {1}% complete for epic {2},'.format(
                component, utility_math.get_percentage(
                    completed_story_points, total_story_points),
                epic['name']))

            logger.info('The {0} has {1}% of the work in code review for epic {2}.,'
                        .format(component, utility_math.get_percentage(
                            code_review_story_points,
                            total_story_points), epic['name']))

            epic_bugs = jira_instance.search_issues(
                ('project = {0} AND component in ({1}) AND status = Open AND '
                 'type = Bug AND "Epic Link" = {2}')
                .format(project, component, epic['id']))

            logger.info(('There are {0} open bugs in {1} for epic {2}.,')
                        .format(len(epic_bugs), component, epic['name']))

            logger.info(']')

    def search_issues(self, query):
        """
        Perform a query on the JiRA instance.
        """
        return self._jira_instance.search_issues(query, 0,
                                                 JiraStatus.MAX_QUERY_RESULT_SIZE)
