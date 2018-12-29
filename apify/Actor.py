import requests

from .ApifyABC import ApifyABC

# TODO MOVE COMMON FUNCTIONS BETWEEN OBJECTS TO APIFYABC AND JUST CHANGE DOCSTRINGS
# TODO MOVE ALL FUNCTIONS THAT JUST TO GET/POST/PUT(URL) AND RETURN R.JSON() TO ONE COMMON FUNCTION WITH URL & METHOD AS PARAMS
class Actor(ApifyABC):
    def __init__(self, actor_id, session=requests.session(), config="apify_config.json"):
        """Class for interacting with Apify crawlers
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
        r = self.get_session().get(self._base_url, params={"token": self.get_token()})
        r.raise_for_status()
        return r.json()

    def update(self, settings={}):
        """Updates actor settings
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/update-actor

        Args:
            settings (JSON object): settings to be updated

        Returns:
            settings (JSON object): new crawler settings
        """
        r = self.get_session().put(self._base_url, params={"token": self.get_token()}, json=settings)
        r.raise_for_status()
        return r.json()

    def delete(self):
        """Deletes the actor
        https://www.apify.com/docs/api/v2#/reference/actors/actor-object/delete-actor
        """
        r = self.get_session().delete(self._base_url, params={"token": self.get_token()})
        r.raise_for_status()

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
