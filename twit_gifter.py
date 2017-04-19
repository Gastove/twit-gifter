import os

import requests as r


API_ROOT = 'https://api.twitter.com/'
TWITTER_KEY_VAR = 'TWITTER_CONSUMER_KEY'
TWITTER_SECRET_VAR = 'TWITTER_CONSUMER_SECRET'


def get_twitter_creds_from_env():
    """
    Load a Twitter key and secret from the environment.
    """
    consumer_key = os.environ[TWITTER_KEY_VAR]
    consumer_secret = os.environ[TWITTER_SECRET_VAR]

    return consumer_key, consumer_secret


def get_auth_token(consumer_key, consumer_secret):
    """
    Per the Twitter Docs:
    https://dev.twitter.com/oauth/application-only

    We need to:
    1. Hit the `oauth2/token` endpoint with a POST request
    2. With the Content-Type header set to 'application/x-www-form-urlencoded;charset=UTF-8'
    3. And the body set to 'grant_type=client_credentials'
    4. Using our key and secret as the user name and password for Basic Auth.
    """
    endpoint = 'oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    # Per the Twitter Docs:
    resp = r.post(
        API_ROOT + endpoint,
        auth=(consumer_key, consumer_secret),
        headers=headers,
        data='grant_type=client_credentials'
    )

    response_json = resp.json()

    # Twitter is awfully firm on this point: if the token_type is not 'bearer',
    # _do not use it_.
    if response_json['token_type'] != 'bearer':
        raise RuntimeError('Could not authorize!')

    return response_json['access_token']


if __name__ == '__main__':
    key, secret = get_twitter_creds_from_env()
    print(get_auth_token(key, secret))
