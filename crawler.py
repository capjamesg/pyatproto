import src.atproto as atproto
import os
import json
import concurrent.futures

ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
USERNAME = os.environ.get("ATPROTO_USERNAME")
PASSWORD = os.environ.get("ATPROTO_PASSWORD")

if not ENDPOINT or not USERNAME or not PASSWORD:
    raise ValueError(
        "Please set the ATPROTO_ENDPOINT, ATPROTO_USERNAME and ATPROTO_PASSWORD environment variables."
    )

ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

print("SEED USER: " + USERNAME)

users = set()
user_queue_to_index = set()


def get_followers(user):
    followers = ap.get_followers(user)

    for follower in followers:
        users.add(follower["handle"])
        user_queue_to_index.add(follower["handle"])

    return followers


with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    future_to_url = {executor.submit(get_followers, USERNAME): USERNAME}
    while future_to_url and len(users) < 2000:
        done, _ = concurrent.futures.wait(
            future_to_url, return_when=concurrent.futures.FIRST_COMPLETED
        )
        for future in done:
            del future_to_url[future]
            print("FOLLOWERS: " + str(len(users)))
            print("QUEUE: " + str(len(user_queue_to_index)))
            if len(user_queue_to_index) > 0:
                user = user_queue_to_index.pop()
                future_to_url[executor.submit(get_followers, user)] = user

all_posts = {}

print("USERS: " + str(len(users)))


def get_user_feed(user):
    print("USER: " + user)
    all_posts = {}
    posts = ap.get_user_feed(user)

    for post in posts["feed"]:
        all_posts[post["post"]["uri"]] = post

    return all_posts


with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    future_to_url = {executor.submit(get_user_feed, user): user for user in users}
    while future_to_url:
        done, _ = concurrent.futures.wait(
            future_to_url, return_when=concurrent.futures.FIRST_COMPLETED
        )
        for future in done:
            del future_to_url[future]
            user = future.result()[0]
            all_posts.update(user)
            print("POSTS: " + str(len(all_posts)))
            print("QUEUE: " + str(len(future_to_url)))

with open("posts.json", "w") as f:
    json.dump(all_posts, f)

print("DONE")
