import requests

from .ApifyABC import ApifyABC

# TODO MOVE COMMON FUNCTIONS BETWEEN OBJECTS TO APIFYABC AND JUST CHANGE DOCSTRINGS
# TODO ONCE ALL IS FINISHED, REORDER FUNCTIONS ALPHABETICALLY


class Actor(ApifyABC):
    def __init__(self, actor_id, session=requests.session(), config="apify_config.json"):
        """Class for interacting with Apify actors
        https://www.apify.com/docs/api/v2#/reference/actors

        Args:
            actor_id (str): actor ID or <username>~<actor name>
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(session, config)
        self._actor_id = actor_id
        self._base_url = 'https://api.apify.com/v2/acts/' + self.get_actor_id()

    def get_actor_id(self):
        """Returns: actor_id (str): actor ID"""
        return self._actor_id

    def get_details(self):
        """Gets actor details
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/get-actor

        Returns:
            actor_details (JSON object): actor details
        """
        return super().get()

    def update(self, settings={}):
        """Updates actor settings
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/update-actor

        Args:
            settings (JSON object): settings to be updated

        Returns:
            settings (JSON object): new actor settings
        """
        return super().put(data=settings)

    def delete(self):
        """Deletes the actor
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/delete-actor
        """

    def get_list_of_versions(self):
        """Gets list of actor versions
        https://www.apify.com/docs/api/v2#/reference/actors/version-collection/get-list-of-versions

        Returns:
            version_list (JSON object): basic information about each version
        """
        url = self._base_url + "/versions"
        return super().get(url)

    def create_version(self):
        """Creates actor version
        https://www.apify.com/docs/api/v2#/reference/actors/version-collection/create-version

        Returns:
            actor_version (JSON object): basic information about the version
        """
        url = self._base_url + "/versions"
        return super().post(url)

    def version(self, version_number):
        """Class for interacting with Apify actor versions
        https://www.apify.com/docs/api/v2#/reference/actors/version-object

        Args:
            version_number (str): actor version number
        Returns:
            actor_version (Actor.Version)
        """
        class Version(Actor):
            def __init__(self, actor_id, version_number, session, config):
                super().__init__(actor_id, session, config)
                self._version_number = version_number
                self._base_url += "versions/" + self.get_version_number()

            def get_version_number(self):
                """Returns: version_number (str): actor version number
                """
                return self._version_number

            def get_details(self):
                """Gets actor version details
                https://www.apify.com/docs/api/v2#/reference/actors/version-object/get-version

                Returns:
                    actor_version_details (JSON object): actor version details
                """

        return Version(self.get_actor_id(), version_number, self.get_session(), self._config)



# TODO ADD VERSION OBJECT
# TODO ADD BUILD OBJECT
# TODO ADD RUN OBJECT


class Task(ApifyABC):
    def __init__(self, actor_task_id, session=requests.session(), config="apify_config.json"):
        """Class for interacting with Apify actor tasks
        https://www.apify.com/docs/api/v2#/reference/actor-tasks

        Args:
            actor_id (str): actor ID or <username>~<actor name>
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(session, config)
        self._actor_task_id = actor_task_id
        self._base_url = 'https://api.apify.com/v2/actor-tasks/' + self.get_actor_task_id()

    def get_actor_task_id(self):
        """Returns: actor_task_id (str): actor task ID"""
        return self._actor_task_id

    def get_details(self):
        """Gets task details
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/task-object/get-task

        Returns:
            task_details (JSON object): actor details
        """
        return super().get()

    def update(self, settings={}):
        """Updates task settings
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/task-object/update-task

        Args:
            settings (JSON object): settings to be updated

        Returns:
            settings (JSON object): new task settings
        """
        return super().put(data=settings)

    def delete(self):
        """Deletes the task
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/task-object/delete-task
        """

    def get_list_of_runs(self, **kwargs):
        """Gets the task's list of runs
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/runs-collection/get-a-list-of-runs

        Args:
        kwargs:
            offset (int): Rank of first execution to return (default: 0)
            limit (int): Maximum number of executions to return (default: 1000)
            desc (int): If 1, executions are sorted from newest to oldest (default: None)

        Returns:
            run_list (JSON object): list of runs and their metadata
        """
        url = self._base_url + "/runs"
        return super().get(url, None, **kwargs)


    def run_synchronously(self, input_={}, **kwargs):
        """Runs task and returns its output
        https://www.apify.com/docs/api/v2#/reference/actor-tasks/run-task-synchronously/run-task-synchronously

        Args:
            input_ (JSON object): custom input fields (default: None)
        kwargs:
            outputRecordKey (str): key to return from default key-value store (default: 'OUTPUT')
        """
        url = self._base_url + "/run-sync"
        return super().get(url, input_, **kwargs)
