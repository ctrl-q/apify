import requests

from .ApifyABC import ApifyABC


class Actor(ApifyABC):
    def __init__(self, actor_id, session=requests.session(), config="apify_config.json"):
        """Class for interacting with Apify crawlers
        https://www.apify.com/docs/api/v1#/reference/crawlers

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
        r = self.get_session().get(self._base_url, params={"token": self.get_token()})
        r.raise_for_status()
        return r.json()
