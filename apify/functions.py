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
    return common._create(url, session, config, settings)


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
    url = "https://api.apify.com/v2/acts"
    return common._create(url, session, config, settings, **kwargs)


def create_dataset(name, session=requests.session(), config="apify_config.json", **kwargs):
    """Creates dataset
    https://www.apify.com/docs/api/v2#/reference/datasets/dataset-collection/create-dataset

    Args:
        name (str): unique name for the dataset
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
        settings (JSON object): crawler settings

    Returns:
        actor (JSON object): actor
    """
    url = "https://api.apify.com/v2/datasets"
    return common._create(url, session, config, {}, name=name)


def create_key_value_store(name, session=requests.session(), config="apify_config.json"):
    """Creates key-value store
    https://www.apify.com/docs/api/v2#/reference/key-value-stores/store-collection/create-key-value-store

    Args:
        name (str): unique name for the key-value store
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token

    Returns:
        store (JSON object): key-value store
    """
    url = "https://api.apify.com/v2/key-value-stores"
    return common._create(url, session, config, {}, name=name)


def create_request_queue(name, session=requests.session(), config="apify_config.json"):
    """Creates key-value store
    https://www.apify.com/docs/api/v2#/reference/request-queues/queue-collection/create-request-queue

    Args:
        name (str): unique name for the request queue
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token

    Returns:
        store (JSON object): key-value store
    """
    url = "https://api.apify.com/v2/request-queues"
    return common._create(url, session, config, {}, name=name)


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
    url = "https://api.apify.com/v2/actor-tasks"
    return common._create(url, session, config, settings)


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
    return common._get_list(url, session, config, **kwargs)


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
    url = "https://api.apify.com/v2/acts"
    return common._get_list(url, session, config, **kwargs)


def get_list_of_datasets(session=requests.session(), config="apify_config.json", **kwargs):
    """Gets list of datasets owned by the user
    https://www.apify.com/docs/api/v2#/reference/datasets/dataset-collection/get-list-of-datasets

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
    kwargs:
        offset (int): rank of first request to return (default: 0)
        limit (int): maximum number of page results to return (default: 10000)
        desc (int): If 1, executions are sorted from newest to oldest (default: None)
        unnamed (bool): If True, unnamed key-value stores are returned with named ones (default: False)

    Returns:
        dataset_list (JSON object): basic information about each dataset
    """
    url = "https://api.apify.com/v2/datasets"
    return common._get_list(url, session, config, **kwargs)


def get_list_of_key_value_stores(session=requests.session(), config="apify_config.json", **kwargs):
    """Gets list of key-value stores owned by the user
    https://www.apify.com/docs/api/v2#/reference/key-value-stores/store-collection/get-list-of-key-value-stores

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
    kwargs:
        offset (int): rank of first request to return (default: 0)
        limit (int): maximum number of page results to return (default: 10000)
        desc (int): If 1, executions are sorted from newest to oldest (default: None)
        unnamed (bool): If True, unnamed key-value stores are returned with named ones (default: False)

    Returns:
        store_list (JSON object): basic information about each key-value store
    """
    url = "https://api.apify.com/v2/key-value-stores"
    return common._get_list(url, session, config, **kwargs)


def get_list_of_request_queues(session=requests.session(), config="apify_config.json", **kwargs):
    """Gets list of requests queues owned by user
    https://www.apify.com/docs/api/v2#/reference/request-queues/queue-collection/get-list-of-request-queues

    Args:
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
    kwargs:
        offset (int): rank of first request to return (default: 0)
        limit (int): maximum number of page results to return (default: 10000)
        desc (int): If 1, executions are sorted from newest to oldest (default: None)
        unnamed (bool): If True, unnamed key-value stores are returned with named ones (default: False)

    Returns:
        queue_list (JSON object): basic information about each key-value store
    """
    url = "https://api.apify.com/v2/request-queues"
    return common._get_list(url, session, config, **kwargs)


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
    url = "https://api.apify.com/v2/actor-tasks"
    return common._get_list(url, session, config, **kwargs)
