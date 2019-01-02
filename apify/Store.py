import requests

from .ApifyABC import ApifyABC


class StoreABC(ApifyABC):
    def __init__(self, store_id, session=requests.session(), config="apify_config.json"):
        super().__init__(session, config)
        self._store_id = store_id
        self._base_url = 'https://api.apify.com/v2/key-value-stores/' + self.get_store_id()

    def get_store_id(self):
        """Returns: store_id (str): store ID"""
        return self._store_id


class Store(StoreABC):
    def __init__(self, store_id, session=requests.session(), config="apify_config.json"):
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
        return super().get()

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
        return super().get(url, None, **kwargs)

    def delete(self):
        """Deletes the actor
        https://www.apify.com/docs/api/v2#/reference/key-value-stores/store-object/delete-store
        """
        return super().delete()
