import requests
import datetime

class AtProtoConfiguration:
    """
    A class to hold the configuration for the AT Protocol.

    :param endpoint: Your ATP endpoint
    :param username: The username for your ATP account
    :param password: The password for your ATP account
    """
    def __init__(self, endpoint, username, password):
        """
        Authentication is done on instantiation of the class.
        """
        self.endpoint = endpoint
        self.username = username
        self.password = password

        auth_token, did = self.authenticate()

        self.auth_token = auth_token
        self.did = did

        self.AUTH_HEADERS = {
            "Authorization": "Bearer " + self.auth_token,
            "Content-Type": "application/json",
        }

    def authenticate(self) -> str:
        """
        Authenticate with the ATP endpoint and return the auth token and DID.
        """
        user_token_request = requests.post(
            self.endpoint + "com.atproto.session.create",
            json={"handle": self.username, "password": self.password},
            headers={"Content-Type": "application/json"},
        )

        return user_token_request.json()["accessJwt"], user_token_request.json()["did"]


    def create_post(self, title):
        """
        Create a post.

        :param title: The title of the post

        :return: The rkey of the post
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
            headers=self.AUTH_HEADERS
        )
        rkey = response.json()["cid"]

        return rkey

    def delete_post(self, rkey):
        """
        Delete a post.

        :param rkey: The rkey of the post to delete
        """
        requests.post(
            self.endpoint + "com.atproto.repo.deleteRecord",
            json={
                "did": self.did,
                "collection": "app.bsky.feed.deleteRecord",
                "rkey": rkey,
            },
            headers=self.AUTH_HEADERS
        )

    def get_user_feed(self) -> dict:
        """
        Get the feed of posts from a user.

        :return: The user feed
        :rtype: dict
        """
        response = requests.get(
            self.endpoint + "app.bsky.feed.getAuthorFeed?author=" + self.did,
            headers=self.AUTH_HEADERS
        )

        return response.json()
    
    def get_user_timeline(self) -> dict:
        """
        Get the timeline from a user's homepage.

        :return: The user timeline.
        :rtype: dict
        """
        response = requests.get(
            self.endpoint + "app.bsky.feed.getTimeline?author=" + self.did,
            headers=self.AUTH_HEADERS
        )

        return response.json()
    

def get_handle_did(endpoint, handle):
    """
    Retrieve the DID associated with a handle.
    """
    response = requests.get(
        endpoint + "com.atproto.handle.resolve?handle=" + handle
    )

    return response.json()["did"]