from . import common


class ApifyABC:
    def __init__(self, session, config):
        self._user_id, self._token = common._get_auth(config)
        self.set_session(session)
        self._config = config

    def get_session(self):
        """Returns: session (requests.Session): session used for requests"""
        return self._session

    def get_token(self):
        """Returns: token (str): API token"""
        return self._token

    def set_session(self, session):
        """Changes the session object used for requests
        Args:
            session (requests.Session): session used for requests
        """
        self._session = session
