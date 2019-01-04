import itertools
import json
import os
import time

import requests

FILE_LOCATION = os.path.split(__file__)[0]


class Crawler:
    """
    Arguments
    crawler_id (string): id of Apify crawler
    session: requests.session object for sending the HTTP requests

    Defines methods for running Apify crawlers & getting results
    """

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
                wait = min(time_left, 60)
                time.sleep(wait)
                status = self.session.get(details_url).json()["status"]

        assert status == "SUCCEEDED", "Crawler did not finish. Response received:\n" + \
            str(r.json())
        if verbose:
            print("Success.")

    def get_results(self, verbose=False):
        """
        GETs result of last execution as JSON
        Returns: JSON response data
        """
        url = self.base_url + '/lastExec/results'
        if verbose:
            print("Getting crawler results")
        data = self.session.get(url, params={"token": self.token})
        data_json = data.json()
        result = list(
            d_j["pageFunctionResult"]
            for d_j in data_json if d_j["pageFunctionResult"] is not None
        )
        if len(result) > 0:
            if isinstance(result[0], list):
                result = list(itertools.chain.from_iterable(result))

            if verbose:
                print("Success.")
        return result

    def get_settings(self, noSecrets=0, executionId=""):
        params = {"token": self.token}
        if noSecrets == 1:
            params["noSecrets"] = 1
        if len(executionId) > 0:
            params["executionId"] = executionId
        r = self.session.get(self.base_url, params=params)
        assert r.status_code == 200, "Error. Status code: {0}: {1}".format(
            r.status_code, r.json())
        return r.json()

    def update_settings(self, settings={}):
        r = self.session.put(self.base_url, params={"token": self.token}, json=settings)
        assert r.status_code == 200, "Error. Status code: {0}: {1}".format(
            r.status_code, r.json())
        return r.json()

    def refresh(self, timeout=600, settings={}):
        """
        Calls run then get_crawler_results
        """
        self.run(timeout=timeout, settings=settings)
        return self.get_results()
    
    def raise_for_status(self):
        # TODO
        pass