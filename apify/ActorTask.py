import requests

from .ApifyABC import ApifyABC


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
