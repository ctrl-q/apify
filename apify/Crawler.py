import itertools
import json
import os
import time

import requests

FILE_LOCATION = os.path.split(__file__)[0]


class CrawlerABC:
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

    def get_user_id(self):
        """Returns: user_id (str): API user ID"""
        return self._user_id

    def set_session(self, session):
        """Changes the session object used for requests
        Args:
            session (requests.Session): session used for requests
    """
        self._session = session


class Crawler(CrawlerABC):
    def __init__(self, crawler_id, session=requests.session(), config="apify_config.json"):
        """Class for interacting with Apify crawlers
        https://www.apify.com/docs/api/v1#/reference/crawlers

        Args:
            crawler_id (str): ID of Apify crawler
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
    """
        super().__init__(session, config)
        self._crawler_id = crawler_id
        self._base_url = 'https://api.apify.com/v1/' + \
            self.get_user_id() + '/crawlers/' + self.get_crawler_id()

    def __init__(self, crawler_id, session=requests.session()):
        try:
            with open(os.path.join(FILE_LOCATION, 'apify_config.json')) as f:
                data = json.load(f)
                self.user_id = data['user']
                self.token = data['token']
                self.session = session
        except FileNotFoundError:
            print("apify_config.json not found. Creating it now...")
            self.user_id = input("Please enter your Apify user_id: ")
            self.token = input("Please enter your Apify API token: ")
            with open(os.path.join(FILE_LOCATION, 'apify_config.json', 'w')) as f:
                data = {"token": self.token, "user": self.user_id}
                json.dump(data, f)
                f.write("\n")

        self.crawler_id = crawler_id
        self.base_url = 'https://api.apify.com/v1/' + \
            self.user_id + '/crawlers/' + crawler_id

    def run(self, timeout=600, settings={}, verbose=False):
        """
        Sends POST request to Apify server to run the crawler
        Returns Server Response
        """
        url = self.base_url + '/execute'
        if verbose:
            print("Running crawler", self.crawler_id)
        r = self.session.post(url, params={"token": self.token, "wait": timeout}, json=settings)
        status = r.json()["status"]
        if status == "RUNNING":
            # Check status every 2 min.
            time_elapsed = min(timeout, 120)
            time_left = timeout - time_elapsed
            details_url = r.json()["detailsUrl"]
            while time_left > 0 and status == "RUNNING":

    def get_last_execution(self, **kwargs):
        """Gets information about the crawler's last execution
        https://www.apify.com/docs/api/v1#/reference/executions/last-execution/get-last-execution

        Args:
        kwargs:
            status (str): filter for the execution status (default: no filter)

        Returns:
            execution_details (JSON object): execution details
        """
        return self.get_list_of_executions(desc=1)[0]

    def get_last_execution_results(self, status=None, combine=False, **kwargs):
        """Gets results from the last crawler execution
        https://www.apify.com/docs/api/v1#/reference/results/last-execution-results/get-last-execution-results

        Args:
            status (str): filter for the execution status (default: no filter)
            combine (bool): if each page function result is a JSON object, combine them into one (if format == "json" and attachment == 0) (default: False)
        kwargs:
            format (str): format of the results, either "json", "jsonl", "csv", "html", "xlsx", "xml" or "rss". (default: "json")
            simplified (int): if 1, then results are returned without metadata (default: 0)
            offset (int): rank of first request to return (default: 0)
            limit (int): maximum number of page results to return (default: 10000)
            desc (int): if 1, results are returned from most-recently to least-recently saved in database
            attachment (int): if 1, results will be saved to working directory and not returned (default: 0)
            delimiter (str): delimiter character for CSV format (default: ",")
            bom (int): if 1, results for all formats will be prefixed by UTF-8 BOM. If 0, BOM will be skipped (default: None)
            xmlRoot (str): default root element name of XML output (default: "results")
            xmlRow (str): default element name wrapping each page function results (default: "page" if simplified == 1 else "result")
            hideUrl (int): if 1, "url" field will not be added to each page function result (default: 0)
            skipFailedPages (int): if 1, pages with errors are skipped are errorInfo is hidden (default: 0)
            skipHeaderRow (int): if 1, header row is skipped in CSV format (default: 0)

        Returns:
            out (JSON object or str): path to download file if attachment == 0 else execution results
        """
        if status is None:
            execution_id = self.get_last_execution()["_id"]
        else:
            execution_id = self.get_last_execution(status=status)["_id"]

        execution = Execution(execution_id, session=self.get_session(), config=self._config)

        return execution.get_results(combine=combine, **kwargs)

    def delete(self):
        """Deletes the crawler
        https://www.apify.com/docs/api/v1#/reference/crawlers/crawler-settings/delete-crawler
        """
        r = self.get_session().delete(self._base_url, params={"token": self.get_token()})
        r.raise_for_status()

    def get_settings(self, **kwargs):
        """Gets full details and settings of a specific crawler
        https://www.apify.com/docs/api/v1#/reference/crawlers/crawler-settings/get-crawler-settings

        Args:
        kwargs:
            noSecrets (int): If 1, response will not contain sensitive data like auth tokens (default: 0)
            executionId (str): execution ID for which to return the settings (default: current settings)

        Returns:
            settings (JSON object): crawler settings
        """
        kwargs.setdefault("token", self.get_token())
        r = self.get_session().get(self._base_url, params=kwargs)
        r.raise_for_status()
        return r.json()

class Execution(CrawlerABC):
    def __init__(self, execution_id, session=requests.session(), config="apify_config.json"):
        """Class for interacting with Apify executions
        https://www.apify.com/docs/api/v1#/reference/executions

        Args:
            crawler_id (str): ID of Apify crawler
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(session, config)
        self._execution_id = execution_id
        self._base_url = "https://api.apify.com/v1/execs/" + self.get_execution_id()

    def get_results(self, combine=False, **kwargs):
        """ Gets execution results
        https://www.apify.com/docs/api/v1#/reference/executions

        Args:
            combine (bool): if each page function result is a JSON object, combine them into one (if format == "json" and attachment == 0) (default: False)
        kwargs:
            format (str): format of the results, either "json", "jsonl", "csv", "html", "xlsx", "xml" or "rss". (default: "json")
            simplified (int): if 1, then results are returned without metadata (default: 0)
            offset (int): rank of first request to return (default: 0)
            limit (int): maximum number of page results to return (default: 10000)
            desc (int): if 1, results are returned from most-recently to least-recently saved in database
            attachment (int): if 1, results will be saved to working directory and not returned (default: 0)
            delimiter (str): delimiter character for CSV format (default: ",")
            bom (int): if 1, results for all formats will be prefixed by UTF-8 BOM. If 0, BOM will be skipped (default: None)
            xmlRoot (str): default root element name of XML output (default: "results")
            xmlRow (str): default element name wrapping each page function results (default: "page" if simplified == 1 else "result")
            hideUrl (int): if 1, "url" field will not be added to each page function result (default: 0)
            skipFailedPages (int): if 1, pages with errors are skipped are errorInfo is hidden (default: 0)
            skipHeaderRow (int): if 1, header row is skipped in CSV format (default: 0)

        Returns:
            out (JSON object or str): path to download file if attachment == 0 else execution results

        """
        url = self._base_url + "/results"
        kwargs.setdefault("token", self.get_token())
        format_ = kwargs.get("format", "json").lower()
        accepted_formats = ("json", "jsonl", "csv", "html",
                            "xlsx", "xml", "csv", None)
        if format_ not in accepted_formats:
            raise ValueError("Accepted formats: {0}".format(accepted_formats))

        if kwargs.get("attachment") == 1:
            file_name, headers = urllib.request.urlretrieve(url)
            return file_name

        r = self.get_session().get(url, params=kwargs)
        r.raise_for_status()
        if format_ in ("json", "jsonl"):
            result = r.json()
            if combine:
                simplified = kwargs.get("simplified", 0)
                if simplified == 0:
        result = list(
                        r["pageFunctionResult"]
                        for r in result if r["pageFunctionResult"] is not None
        )
                elif simplified == 1:
                    result = list(r for r in result if r is not None)

        if len(result) > 0:
            if isinstance(result[0], list):
                result = list(itertools.chain.from_iterable(result))

        else:
            result = r.text
        return result

    def stop(self):
        """Stops the execution
        https://www.apify.com/docs/api/v1#/reference/executions/stop-execution/stop-execution

        Returns:
            execution_details (JSON object): execution details
        """
        url = self._base_url + "/stop"
        r = self.get_session().post(url, params={"token": self.get_token()})
        r.raise_for_status()
        return r.json()

    def get_details(self):
        """Gets execution details
        https://www.apify.com/docs/api/v1#/reference/executions/execution-details/get-execution-details

        Returns:
            execution_details (JSON object): execution details
        """
        r = self.get_session().get(self._base_url, params={"token": self.get_token()})
        r.raise_for_status()
        return r.json()

    def get_execution_id(self):
        """Returns: execution_id (str): crawler ID"""
        return self._execution_id
    
