import requests

from . import common


def create_crawler(session=requests.session(), config="apify_config.json", settings={}):
    """Creates crawler with specified settings
    https://www.apify.com/docs/api/v1#/reference/results/create-crawler

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
        settings (JSON object): crawler settings

    Returns:
        crawler_settings (JSON object): crawler settings
    """
    user_id, token = common._get_auth(config)
    url = "https://api.apify.com/v1/" + user_id + "/crawlers"
    r = session.post(url, params={"token": token}, json=settings)
    r.raise_for_status()
    return r.json()


def create_actor(session=requests.session(), config="apify_config.json", settings={}, **kwargs):
    """Creates actor with specified settings
    https://www.apify.com/docs/api/v2#/reference/actors/actor-collection/create-actor

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
        settings (JSON object): crawler settings
    kwargs:
        my (bool) : if True, only actors owned by the user are returned (default: False)

    Returns:
        actor (JSON object): actor
    """
    user_id, token = common._get_auth(config)
    url = "https://api.apify.com/v2/acts"
    kwargs.setdefault("token", token)
    r = session.post(url, params=kwargs, json=settings)
    r.raise_for_status()
    return r.json()


def create_task(session=requests.session(), config="apify_config.json", settings={}):
    """Creates task with specified settings
    https://www.apify.com/docs/api/v2#/reference/actor-tasks/tasks-collection/create-a-task

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
        settings (JSON object): crawler settings

    Returns:
        task (JSON object): actor task
    """
    user_id, token = common._get_auth(config)
    url = "https://api.apify.com/v2/actor-tasks"
    r = session.post(url, params={"token": token}, json=settings)
    r.raise_for_status()
    return r.json()


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
    r.raise_for_status()
    return r.json()


def get_list_of_actors(session=requests.session(), config="apify_config.json", **kwargs):
    """Gets list of actors a user created or used
    https://www.apify.com/docs/api/v2#/reference/actors/actor-collection/get-list-of-actors

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
    kwargs:
        my (bool): if True, only actors owned by the user are returned (default: False)
        offset (int): rank of first request to return (default: 0)
        limit (int): maximum number of page results to return (default: 10000)
        desc (int): If 1, executions are sorted from newest to oldest (default: None)

    Returns:
        actor_list (JSON object): basic information about each crawler
    """
    user_id, token = common._get_auth(config)
    url = "https://api.apify.com/v2/acts"
    kwargs.setdefault("token", token)
    r = session.get(url, params=kwargs)
    r.raise_for_status()
    return r.json()


def get_list_of_tasks(session=requests.session(), config="apify_config.json", **kwargs):
    """Gets list of tasks a user created or used
    https://www.apify.com/docs/api/v2#/reference/actor-tasks/tasks-collection/get-a-list-of-tasks

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
    kwargs:
        offset (int): rank of first request to return (default: 0)
        limit (int): maximum number of page results to return (default: 10000)
        desc (int): If 1, executions are sorted from newest to oldest (default: None)

    Returns:
        actor_list (JSON object): basic information about each crawler
    """
    user_id, token = common._get_auth(config)
    url = "https://api.apify.com/v2/actor-tasks"
    kwargs.setdefault("token", token)
    r = session.get(url, params=kwargs)
    r.raise_for_status()
    return r.json()
