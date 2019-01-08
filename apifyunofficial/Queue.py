import requests

from .ApifyABC import ApifyABC


class QueueABC(ApifyABC):
    def __init__(self, queue_id, session, config):
        super().__init__(session, config)
        self._queue_id = queue_id
        self._base_url = 'https://api.apify.com/v2/request-queues/' + self.get_queue_id()

    def get_queue_id(self):
        """Returns: queue_id (str): queue ID"""
        return self._queue_id


class Queue(QueueABC):
    def __init__(self, queue_id, session=requests.Session(), config="apify_config.json"):
        """Class for interacting with Apify request queues
        https://www.apify.com/docs/api/v2#/reference/request-queues/queue/

        Args:
            queue_id (str): queue ID or <username>~<queue name>
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(queue_id, session, config)

    def get(self):
        """Gets queue details
        https://www.apify.com/docs/api/v2#/reference/request-queues/queue/get-request-queue

        Returns:
            queue_details (JSON object): queue details
        """
        return super()._get()

    def delete(self):
        """Deletes queue
        https://www.apify.com/docs/api/v2#/reference/request-queues/queue/delete-request-queue
        """
        return super()._delete()

    def add_request(self, unique_key, url, method, **kwargs):
        """Adds request to the queue
        https://www.apify.com/docs/api/v2#/reference/request-queues/request-collection/add-request

        Args:
            unique_key (str): unique identifier for the request
            url (str): url to request
            method (str): HTTP method to use for request
        kwargs:
            forefront (bool): whether request should be at head of the queue (default: False)
        """
        accepted_methods = ("CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE")
        if method not in accepted_methods:
            raise ValueError("accepted methods: {0}".format(accepted_methods))

        url_ = self._base_url + "/requests"
        data = {"uniqueKey": unique_key, "url": url, "method": method}
        return super()._post(url_, data, **kwargs)

    def Request(self, request_id):
        """Class for interacting with Apify queue requests
        https://www.apify.com/docs/api/v2#/reference/request-queues/request/

        Args:
            request_id (str): request ID
        """
        return _Request(self.get_queue_id(), request_id, self.get_session(), self._config)

    def get_head(self, **kwargs):
        """Gets first request(s) from the queue
        https://www.apify.com/docs/api/v2#/reference/request-queues/queue-head/get-head

        Args:
        kwargs:
            limit (int): Maximum number of requests to return

        Returns:
            queue_head (JSON object): information about first request(s)
        """
        url = self._base_url + "/head"
        return super()._get(url, None, **kwargs)


class _Request(QueueABC):
    def __init__(self, queue_id, request_id, session, config):
        super().__init__(queue_id, session, config)
        self._request_id = request_id
        self._base_url += "/requests/" + self.get_request_id()

    def get_request_id(self):
        """Returns: request_id (str): queue request ID"""
        return self._request_id

    def get(self):
        """Gets queue request details
        https://www.apify.com/docs/api/v2#/reference/request-queues/request/get-request

        Returns:
            request_details (JSON object): queue request details
        """
        return super()._get()

    def update(self, id, unique_key, url, method, **kwargs):
        """Updates queue request
        https://www.apify.com/docs/api/v2#/reference/request-queues/request/update-request

        Args:
            id (str): request ID
            unique_key (str): unique identifier for the request
            url (str): url to request
            method (str): HTTP method to use for request
        kwargs:
            forefront (bool): whether request should be at head of the queue (default: False)
        """
        accepted_methods = ("CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE")
        if method not in accepted_methods:
            raise ValueError("accepted methods: {0}".format(accepted_methods))

        data = {"id": id, "uniqueKey": unique_key, "url": url, "method": method}
        return super()._put(None, data, **kwargs)

    def delete(self):
        """Deletes queue request
        https://www.apify.com/docs/api/v2#/reference/request-queues/request/delete-request
        """
        return super()._delete()
