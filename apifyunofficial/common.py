import json


def _get_auth(config):
    """Parses config file for auth info
    Args:
        config (str, path-like): path to JSON file with user ID and token

    Returns:
        user_id (str): Apify user ID
        token (str): Apify token
    """
    with open(config) as f:
        data = json.load(f)
        return data['user'], data['token']


def _get_list(url, session, config, **kwargs):
    """Gets list of items
    Args:
        url (str): url to get
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
        kwargs used by calling function

    Returns:
        list_of_items (JSON object): basic information about each object
    """
    user_id, token = _get_auth(config)
    kwargs.setdefault("token", token)
    r = session.get(url, params=kwargs)
    r.raise_for_status()
    return r.json()


def _create(url, session, config, settings, **kwargs):
    """Creates item
    Args:
        url (str): url to get
        session (requests.Session object): used to send the HTTP requests (default: new session)
        config (str, path-like): path to JSON file with user ID and token
        settings (JSON object): object settings
        kwargs used by calling function

    Returns:
        item (JSON object): object
    """
    user_id, token = _get_auth(config)
    kwargs.setdefault("token", token)
    if settings in ({}, None):
        r = session.post(url, params=kwargs)
    else:
        r = session.post(url, params=kwargs, json=settings)
    r.raise_for_status()
    return r.json()
