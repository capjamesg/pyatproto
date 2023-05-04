import datetime

import dns.resolver
import mf2py
import requests

SUPPORTED_METHODS = [
    "com.atproto.session.create",
    "com.atproto.repo.createRecord",
    "com.atproto.repo.deleteRecord",
    "com.atproto.repo.getAuthorFeed",
    "com.atproto.handle.change",
]


class AtProtoConfiguration:
    """
    A class to hold the configuration for the AT Protocol.

    :param endpoint: Your ATP endpoint
    :param username: The username for your ATP account
    :param password: The password for your ATP account

    Example:

    .. code-block:: python

        import pyatproto
        import os

        ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
        USERNAME = os.environ.get("ATPROTO_USERNAME")
        PASSWORD = os.environ.get("ATPROTO_PASSWORD")

        if not ENDPOINT or not USERNAME or not PASSWORD:
            raise ValueError(
                "Please set the ATPROTO_ENDPOINT, ATPROTO_USERNAME and ATPROTO_PASSWORD environment variables."
            )

        ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

        create_post = ap.create_post("My First Post")

        print(create_post)
    """

    def __init__(self, endpoint, username, password):
        """
        Authentication is done on instantiation of the class.
        """
        self.endpoint = endpoint
        self.username = username
        self.password = password

        auth_token, did = self._authenticate()

        self.auth_token = auth_token
        self.did = did

        self.AUTH_HEADERS = {
            "Authorization": "Bearer " + self.auth_token,
            "Content-Type": "application/json",
        }

    def _authenticate(self) -> str:
        """
        Authenticate with the ATP endpoint and return the auth token and DID.
        """
        user_token_request = requests.post(
            self.endpoint + "com.atproto.server.createSession",
            json={"identifier": self.username, "password": self.password},
            headers={"Content-Type": "application/json"},
        )

        return user_token_request.json()["accessJwt"], user_token_request.json()["did"]

    def get_followers(self, user=None) -> list:
        """
        Get the followers of a user.

        :return: The list of followers
        :rtype: list

        Example:

        .. code-block:: python

            import pyatproto
            import os

            ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
            USERNAME = os.environ.get("ATPROTO_USERNAME")
            PASSWORD = os.environ.get("ATPROTO_PASSWORD")

            ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

            followers = ap.get_followers()
            
            print(followers)
        """
        if user is None:
            user = self.username

        response = requests.get(
            self.endpoint + "app.bsky.graph.getFollowers?actor=" + user,
            headers=self.AUTH_HEADERS,
        )

        return response.json()["followers"]

    def create_post(self, title):
        """
        Create a post.

        :param title: The title of the post

        :return: The rkey of the post

        Example:

        .. code-block:: python

            import pyatproto
            import os

            ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
            USERNAME = os.environ.get("ATPROTO_USERNAME")
            PASSWORD = os.environ.get("ATPROTO_PASSWORD")

            ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

            create_post = ap.create_post("My First Post")

            print(create_post)
        """
        iso_time = datetime.datetime.utcnow().isoformat()

        response = requests.post(
            self.endpoint + "com.atproto.repo.createRecord",
            json={
                "did": self.did,
                "collection": "app.bsky.feed.post",
                "validate": True,
                "record": {"text": title, "createdAt": iso_time},
            },
            headers=self.AUTH_HEADERS,
        )
        rkey = response.json()["cid"]

        return rkey

    def delete_post(self, rkey):
        """
        Delete a post.

        :param rkey: The rkey of the post to delete

        Example:

        .. code-block:: python

            import pyatproto
            import os

            ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
            USERNAME = os.environ.get("ATPROTO_USERNAME")
            PASSWORD = os.environ.get("ATPROTO_PASSWORD")

            ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

            ap.delete_post("rkey")
        """
        requests.post(
            self.endpoint + "com.atproto.repo.deleteRecord",
            json={
                "did": self.did,
                "collection": "app.bsky.feed.deleteRecord",
                "rkey": rkey,
            },
            headers=self.AUTH_HEADERS,
        )

    def get_user_feed(self, user) -> dict:
        """
        Get the feed of posts from a user.

        :return: The user feed
        :rtype: dict

        Example:

        .. code-block:: python



        Example:

        .. code-block:: python

            import pyatproto
            import os

            ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
            USERNAME = os.environ.get("ATPROTO_USERNAME")
            PASSWORD = os.environ.get("ATPROTO_PASSWORD")

            ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

            user_feed = ap.get_user_feed()

            print(user_feed)
        """
        if user is None:
            user = self.username

        response = requests.get(
            self.endpoint + "app.bsky.feed.getAuthorFeed?actor=" + user,
            headers=self.AUTH_HEADERS,
        )

        return response.json()

    def get_post(self, atp_uri: str) -> dict:
        """
        Get a post.

        :param atp_uri: The ATP URI of the post
        :return: The post
        :rtype: dict

        Example:

        .. code-block:: python

            import pyatproto

            ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

            post = ap.get_post("atp://rkey")

            print(post)
        """
        response = requests.get(
            self.endpoint + "app.bsky.feed.getPostThread?uri=" + atp_uri,
            headers=self.AUTH_HEADERS,
        )

        return response.json()

    def get_user_timeline(self, did=None) -> dict:
        """
        Get the timeline from a user's homepage.

        :return: The user timeline.
        :rtype: dict

        Example:

        .. code-block:: python

            import pyatproto

            ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

            user_timeline = ap.get_user_timeline()

            print(user_timeline)
        """

        if not did:
            did = self.did

        response = requests.get(
            self.endpoint + "app.bsky.feed.getTimeline?author=" + did,
            headers=self.AUTH_HEADERS,
        )

        return response.json()

    def change_username_to_domain(self, domain):
        """
        Change the username to a domain.

        :param domain: The domain to change to

        Example:

        .. code-block:: python

            import pyatproto

            ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

            ap.change_username_to_domain("example.com")
        """

        answers = dns.resolver.query("_atproto." + domain, "TXT")

        if len(answers) == 0:
            raise Exception("Domain does not resolve to an ATP endpoint.")

        if not answers[0].strings[0].decode("utf-8").startswith("did=did:"):
            raise Exception("Domain does not resolve to an ATP endpoint.")

        change_request = requests.post(
            self.endpoint + "com.atproto.handle.change",
            json={"did": self.did, "handle": domain},
            headers=self.AUTH_HEADERS,
        )

        if change_request.status_code != 200:
            raise Exception("Server error. Could not change username to domain.")

        self.username = domain

def username_to_did(endpoint, username):
    """
    Get the DID associated with a username.

    :param endpoint: The ATP endpoint to use
    :param username: The username to get the DID of
    :return: The DID associated with the username

    Example:

    .. code-block:: python

        import pyatproto

        did = pyatproto.username_to_did(ENDPOINT, "username")

        print(did)
    """
    response = requests.get(
        endpoint + "com.atproto.identity.resolveHandle?handle=" + username
    )

    return response.json()["did"]


def hentry_to_atproto_post(post_url: str, server_config: AtProtoConfiguration) -> None:
    """
    Convert a h-entry to an ATP post.

    :param post_url: The URL of the post whose h-entry you want to syndicate to ATP
    :param server_config: The configuration for the ATP server

    :raises Exception: If no h-entry is found

    Example:

    .. code-block:: python

        import pyatproto

        ap = pyatproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

        pyatproto.hentry_to_atproto_post("https://example.com/post", ap)
    """

    parsed_tree = mf2py.parse(post_url)

    if len(parsed_tree["items"]) == 0:
        raise Exception("No h-entry found.")

    h_entry = None

    for item in parsed_tree["items"]:
        if "type" in item and "h-entry" in item["type"]:
            h_entry = item
            break

    if h_entry is None:
        raise Exception("No h-entry found.")

    h_entry_object = h_entry["properties"]
    post_body = None

    if "name" in h_entry_object:
        post_body = h_entry_object["name"][0]
    elif "description" in h_entry_object:
        post_body = h_entry_object["description"][0]
    elif "content" in h_entry_object:
        post_body = h_entry_object["content"][0]["value"]
    elif "content" is None:
        raise Exception("No post title found.")

    server_config.create_post(post_body)


def is_supported_method(method: str) -> bool:
    """
    Check if a method is supported by this library.

    :param method: The method to check

    :return: Whether the method is supported
    :rtype: bool

    Example:

    .. code-block:: python

        import pyatproto

        print(pyatproto.is_supported_method("com.atproto.handle.change"))
    """
    return method in SUPPORTED_METHODS
