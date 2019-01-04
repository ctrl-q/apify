import urllib.request

import requests

from .ApifyABC import ApifyABC


class Dataset(ApifyABC):
    def __init__(self, dataset_id, session=requests.Session(), config="apify_config.json"):
        """Class for interacting with Apify datasets
        https://www.apify.com/docs/api/v2#/reference/datasets/dataset/

        Args:
            dataset_id (str): dataset ID or <username>~<dataset name>
            session (requests.Session object): used to send the HTTP requests (default: new session)
            config (str, path-like): path to JSON file with user ID and token
        """
        super().__init__(session, config)
        self._dataset_id = dataset_id
        self._base_url = "https://api.apify.com/v2/datasets/" + self.get_dataset_id()

    def get_dataset_id(self):
        """Returns: dataset_id (str): dataset ID"""
        return self._dataset_id

    def get(self):
        """Gets actor details
        https://www.apify.com/docs/api/v2#/reference/datasets/dataset/get-dataset

        Returns:
            dataset_details (JSON object): dataset details
        """
        return super()._get()

    def delete(self):
        """Deletes the dataset
        https://www.apify.com/docs/api/v2#/reference/datasets/dataset/delete-dataset
        """
        return super()._delete()

    def get_items(self, **kwargs):
        """Gets items stored in the dataset
        https://www.apify.com/docs/api/v2#/reference/datasets/item-collection/get-items

        Args:
            combine (bool): if each page function result is a JSON object, combine them into one (if format == "json" and attachment == 0) (default: False)
        kwargs:
            format (str): format of the results, either "json", "jsonl", "csv", "html", "xlsx", "xml" or "rss". (default: "json")
            offset (int): rank of first item to return (default: 0)
            limit (int): maximum number of items to return (default: 10000)
            fields (str): comma-separated list of fields to return (default: all)
            omit (str): comma-separated list of fields to omit (default: none)
            unwind (str): name of a field to unwind. If it's an array, its items are split into separate records
            desc (int): if 1, results are returned from most-recently to least-recently saved in database
            attachment (int): if 1, results will be saved to working directory and not returned (default: 0)
            delimiter (str): delimiter character for CSV format (default: ",")
            bom (int): if 1, results for all formats will be prefixed by UTF-8 BOM. If 0, BOM will be skipped (default: None)
            xmlRoot (str): default root element name of XML output (default: "items")
            xmlRow (str): default element name wrapping each page function results (default: "item")
            skipHeaderRow (int): if 1, header row is skipped in CSV format (default: 0)

        Returns:
            out (JSON object or str): path to download file if attachment == 1 else execution results
        """
        url = self._base_url + "/items"
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
        return r.json() if format_ in ("json", "jsonl") else r.text

    def put_items(self, data):
        """Saves item(s) into the dataset
        https://www.apify.com/docs/api/v2#/reference/datasets/item-collection/put-items

        Args:
            data (JSON object or array of JSON objects): items to store
        """
        url = self._base_url + "/items"
        return super()._put(url, data)
