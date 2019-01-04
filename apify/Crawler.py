import itertools
import time
import urllib.request

import requests

from .ApifyABC import ApifyABC


class CrawlerABC(ApifyABC):

    def get_user_id(self):
        """Returns: user_id (str): API user ID"""
        return self._user_id


class Crawler(CrawlerABC):
    def __init__(self, crawler_id, session=requests.Session(), config="apify_config.json"):
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

    def get_crawler_id(self):
        """Returns: crawler_id (str): crawler ID"""
        return self._crawler_id

    def get_settings(self, **kwargs):
        """Gets full crawler details and settings
        https://www.apify.com/docs/api/v1#/reference/crawlers/crawler-settings/get-crawler-settings

        Args:
        kwargs:
            noSecrets (int): If 1, response will not contain sensitive data like auth tokens (default: 0)
            executionId (str): execution ID for which to return the settings (default: current settings)

        Returns:
            settings (JSON object): crawler settings
        """
        return super()._get(None, None, **kwargs)

    def update_settings(self, settings={}):
        """Updates crawler settings
        https://www.apify.com/docs/api/v1#/reference/crawlers/crawler-settings/update-crawler-settings

        Args:
            settings (JSON object): settings to be updated

        Returns:
            settings (JSON object): new crawler settings
        """
        return super()._put(data=settings)

    def delete(self):
        """Deletes the crawler
        https://www.apify.com/docs/api/v1#/reference/crawlers/crawler-settings/delete-crawler
        """
        return super()._delete()

    def start(self, settings={}, **kwargs):
        """Executes crawler
        https://www.apify.com/docs/api/v1#/reference/executions/start-execution/start-execution

        Args:
            settings (JSON object): custom settings to use (default: {})
        kwargs:
            tag (str): custom tag for the execution. Cannot be longer than 64 characters (default: None)
            wait (int): max. number of seconds the server waits for execution to finish (default: 0)

        Returns:
            execution_details (JSON object): execution details
        """
        if len(kwargs.get("tag", "")) > 64:
            raise ValueError("tag cannot be longer than 64 characters")
        url = self._base_url + '/execute'
        kwargs.setdefault("token", self.get_token())
        r = self.get_session().post(url, params=kwargs, json=settings)
        r.raise_for_status()
        status = r.json()["status"]
        if status == "RUNNING":
            # Check status every minute
            wait = kwargs.get("wait", 0)
            time_elapsed = min(wait, 120)
            time_left = wait - time_elapsed
            details_url = r.json()["detailsUrl"]
            while time_left > 0 and status == "RUNNING":
                sleep = min(time_left, 60)
                time.sleep(sleep)
                status = self.get_session().get(details_url).json()["status"]
        r.raise_for_status()
        return r.json()

    def get_list_of_executions(self, **kwargs):
        """Gets the crawler's list of executions
        https://www.apify.com/docs/api/v1#/reference/executions/list-of-executions/get-list-of-executions

        Args:
        kwargs:
            status (str): Filter for the execution status (default: no filter)
            offset (int): Rank of first execution to return (default: 0)
            limit (int): Maximum number of executions to return (default: 1000)
            desc (int): If 1, executions are sorted from newest to oldest (default: None)

        Returns:
            execution_list (JSON object): list of executions and their metadata
        """
        url = self._base_url + "/execs"
        return super()._get(url, None, **kwargs)

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

    def stop_last_execution(self):
        """Stops the last crawler execution
        https://www.apify.com/docs/api/v1#/reference/executions/stop-execution

        Returns:
            execution_details (JSON object): execution details
        """
        execution_id = self.get_last_execution()["_id"]
        execution = Execution(execution_id, session=self.get_session(), config=self._config)
        return execution.stop()


class Execution(CrawlerABC):
    def __init__(self, execution_id, session=requests.Session(), config="apify_config.json"):
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

    def get_execution_id(self):
        """Returns: execution_id (str): crawler ID"""
        return self._execution_id

    def stop(self):
        """Stops the execution
        https://www.apify.com/docs/api/v1#/reference/executions/stop-execution/

        Returns:
            execution_details (JSON object): execution details
        """
        url = self._base_url + "/stop"
        return super()._post(url)

    def get_details(self):
        """Gets execution details
        https://www.apify.com/docs/api/v1#/reference/executions/execution-details/get-execution-details

        Returns:
            execution_details (JSON object): execution details
        """
        return super()._get()

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
            out (JSON object or str): path to download file if attachment == 1 else execution results

        """
        url = self._base_url + "/results"
        kwargs.setdefault("token", self.get_token())
        format_ = kwargs.get("format", "json").lower()
        accepted_formats = ("json", "jsonl", "csv", "html",
                            "rss", "xlsx", "xml", None)
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
