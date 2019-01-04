import requests

from .ApifyABC import ApifyABC


class StoreABC(ApifyABC):
    def __init__(self, store_id, session, config):
        super().__init__(session, config)
        self._store_id = store_id
        self._base_url = 'https://api.apify.com/v2/key-value-stores/' + self.get_store_id()

    def get_store_id(self):
        """Returns: store_id (str): store ID"""
        return self._store_id


class Store(StoreABC):
    def __init__(self, store_id, session=requests.Session(), config="apify_config.json"):
        """Class for interacting with Apify key-value stores
        https://www.apify.com/docs/api/v2#/reference/key-value-stores

        Args:
            store_id (str): key-value store ID or <username>~<store name>
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(store_id, session, config)

    def get(self):
        """Gets store details
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/store-object/get-store

        Returns:
            store_details (JSON object): store details
        """
        return super()._get()

    def delete(self):
        """Deletes the actor
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/store-object/delete-store
        """
        return super()._delete()

    def get_list_of_keys(self, **kwargs):
        """Gets list of store keys and info about values
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/key-collection/get-list-of-keys

        Args:
        kwargs:
            exclusiveStartKey (str): last key to skip from the result (default: None)
            limit (int): Maximum number of builds to return (default: 1000)

        Returns:
            key_list (JSON object): list of keys and info about values
        """
        url = self._base_url + "/keys"
        return super()._get(url, None, **kwargs)

    def Record(self, record_key):
        """Class for interacting with Apify key-value store records
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/record

        Args:
            record_key (str): key of the record
        Returns:
            record (Store.Record): store record
        """
        return _Record(self.get_store_id(), record_key, self.get_session(), self._config)


class _Record(StoreABC):
    def __init__(self, store_id, record_key, session, config):
        super().__init__(store_id, session, config)
        self._record_key = record_key
        self._base_url += "/records/" + self.get_record_key()

    def get_record_key(self):
        """Returns: record_key (str): store record key"""
        return self._record_key

    def get(self, **kwargs):
        """Gets value stored under the key
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/record/get-record

        Args:
        kwargs:
            disableRedirect (bool): whether to get the record from apify.com instead of amazonaws.com (default: False)
        """
        return super()._get(None, None, **kwargs)

    def put(self, value, mime_type="application/json", gzip=False):
        """Stores a value for the key
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/record/put-record

        Args:
            value (any object): value to store
            mime_type (str) : MIME type of value (default: application/json)
            gzip (bool): whether value is gzipped (default: False)
        """
        if mime_type.lower() in ("application/json", "application/javascript") and gzip is False:
            return super()._put(None, value)

        headers = {"Content-Type": mime_type}
        if gzip:
            headers["Content-Encoding"] = "gzip"
        r = self.get_session().put(self._base_url, params={"token": self.get_token()}, json={self.get_record_key(): value}, headers=headers)
        r.raise_for_status()
        return r.json()

    def delete(self):
        """Deletes record
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/record/delete-record
        """
        return super()._delete()

    def get_direct_upload_url(self, mime_type="application/json", gzip=False):
        """Gets unique url to upload record
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/direct-upload-url/get-direct-upload-url

        Args:
            mime_type (str) : MIME type of value (default: application/json)
            gzip (bool): whether value is gzipped (default: False)

        Returns:
            upload_url (JSON object): JSON object containing upload url
        """
        url = self._base_url + "/direct-upload-url"
        if mime_type.lower() in ("application/json", "application/javascript") and gzip is False:
            return super()._get(url)

        headers = {"Content-Type": mime_type}
        if gzip:
            headers["Content-Encoding"] = "gzip"
        r = self.get_session().get(url, params={"token": self.get_token()}, headers=headers)
        r.raise_for_status()
        return r.json()
