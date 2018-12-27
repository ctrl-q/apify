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
