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
        r = self.get_session().get(url, params={"token": self.get_token()})
        r.raise_for_status()
        return r.json()

    def create_version(self):
        """Creates actor version
        https://www.apify.com/docs/api/v2#/reference/actors/version-collection/create-version

        Returns:
            actor_version (JSON object): basic information about the version
        """
        url = self._base_url + "/versions"
        r = self.get_session().post(url, params={"token": self.get_token()})
        r.raise_for_status()
        return r.json()

# TODO ADD VERSION OBJECT
# TODO ADD BUILD OBJECT
# TODO ADD RUN OBJECT


class ActorTask(ApifyABC):
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
