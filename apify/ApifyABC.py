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

    def _delete(self):
        r = self.get_session().delete(self._base_url, params={"token": self.get_token()})
        r.raise_for_status()

    def _get(self, url=None, data=None, **kwargs):
        url = self._base_url if url is None else url
        kwargs.setdefault("token", self.get_token())
        if data is None:
            r = self.get_session().get(url, params=kwargs)
        else:
            r = self.get_session().get(url, params=kwargs, json=data)
        r.raise_for_status()
        return r.json()

    def _put(self, url=None, data=None, **kwargs):
        kwargs.setdefault("token", self.get_token())
        url = self._base_url if url is None else url
        r = self.get_session().put(url, params=kwargs, json=data)
        r.raise_for_status()
        return r.json()

    def _post(self, url=None, data=None, **kwargs):
        url = self._base_url if url is None else url
        kwargs.setdefault("token", self.get_token())
        if data is None:
            r = self.get_session().post(url, params=kwargs)
        else:
            r = self.get_session().psot(url, params=kwargs, json=data)
        r.raise_for_status()
        return r.json()
