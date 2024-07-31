import os
from typing import Literal
from urllib.parse import urljoin

import requests
from pydantic import BaseModel


class GetAuthenticationCodeParams(BaseModel):
    client_id: str
    redirect_uri: str
    scope: str
    response_type: Literal["code"] = "code"


class GetRefreshTokenBody(BaseModel):
    code: str
    client_id: str
    client_secret: str
    redirect_uri: str
    grant_type: Literal["authorization_code"] = "authorization_code"


SCOPE = "playlist-modify-public playlist-modify-private"
ACCOUNTS_BASE_URL = "https://accounts.spotify.com"
REDIRECT_URI = "http://localhost"


def get_authorization_code(
    client_id: str,
    scope: str,
) -> str:
    url_ext = "authorize?"
    url = urljoin(base=ACCOUNTS_BASE_URL, url=url_ext)

    params = GetAuthenticationCodeParams(
        client_id=client_id, redirect_uri=REDIRECT_URI, scope=scope
    ).model_dump()

    response = requests.get(url=url, params=params, timeout=30)
    authentication_code = input(f"""
    Paste this URL into your browser.....
    
    {response.url}

    You may be asked to sign into spotify, after which you will be redirected to a 
    URL with the authentication code in it.

    Enter your authentication code here:""")

    return authentication_code


def get_refresh_token(
    authorization_code: str,
    client_id: str,
    client_secret: str,
):
    url_ext = "api/token"
    url = urljoin(base=ACCOUNTS_BASE_URL, url=url_ext)
    body = GetRefreshTokenBody(
        code=authorization_code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
    ).model_dump()

    response = requests.post(url=url, data=body, timeout=30)
    print(response.json())


if __name__ == "__main__":

    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    authorization_code = get_authorization_code(client_id=client_id, scope=SCOPE)
    get_refresh_token(
        authorization_code=authorization_code,
        client_id=client_id,
        client_secret=client_secret,
    )
