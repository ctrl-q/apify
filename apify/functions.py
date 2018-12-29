import requests

from . import common


def get_list_of_crawlers(session=requests.session(), config="apify_config.json", **kwargs):
    """Gets a list of crawlers belonging to a specific user
    https://www.apify.com/docs/api/v1#/reference/crawlers/list-of-crawlers/get-list-of-crawlers

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
    kwargs:
        offset (int): rank of first request to return (default: 0)
        limit (int): maximum number of page results to return (default: 10000)
        desc (int): If 1, executions are sorted from newest to oldest (default: None)

    Returns:
        crawler_list (JSON object): basic information about each crawler
    """
    user_id, token = common._get_auth(config)
    url = "https://api.apify.com/v1/" + user_id + "/crawlers"
    kwargs.setdefault("token", token)
    r = session.get(url, params=kwargs)
    common.raise_for_status(r)
    return r.json()


def get_list_of_actors(session=requests.session(), config="apify_config.json", **kwargs):
    """Gets list of actors a user created or used
    https://www.apify.com/docs/api/v2#/reference/actors/actor-collection/get-list-of-actors

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
    kwargs:
        my (int): if 1, only actors owned by the user are returned (default: 0)
        offset (int): rank of first request to return (default: 0)
        limit (int): maximum number of page results to return (default: 10000)
        desc (int): If 1, executions are sorted from newest to oldest (default: None)

    Returns:
        actor_list (JSON object): basic information about each crawler
    """
    user_id, token = common._get_auth(config)
    url = "https://api.apify.com/v1/" + user_id + "/crawlers"
    kwargs.setdefault("token", token)
    r = session.get(url, params=kwargs)
    common.raise_for_status(r)
    return r.json()
