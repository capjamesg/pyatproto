import os

import pyatproto as atproto

ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
USERNAME = os.environ.get("ATPROTO_USERNAME")
PASSWORD = os.environ.get("ATPROTO_PASSWORD")

if not ENDPOINT or not USERNAME or not PASSWORD:
    raise ValueError("Please set the ATPROTO_ENDPOINT, ATPROTO_USERNAME and ATPROTO_PASSWORD environment variables.")

ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

HOME_DIR = "/home/james/pyatproto/"

with open(HOME_DIR + "sent.txt", "r") as f:
    sent = f.read().split("\n")

notifications = ap.get_notifications()

def get_top_parent(uri, author):
    post = ap.get_post(uri)
    if post["thread"].get("parent") is None:
        return uri, post["thread"]["post"]["author"]["handle"]
    else:
        return get_top_parent(post["thread"]["parent"]["post"]["uri"], None)


for notification in notifications:
    post_uri = notification["uri"]
    post_cid = notification["cid"]

    if notification["record"].get("reply") is None:
        continue

    uri, author = get_top_parent(notification["record"]["reply"]["parent"]["uri"], None)
    
    post_id = uri.split("/")[-1]

    text_content = notification["record"].get("text", "")

    if "unroll" not in text_content.lower() or post_id in sent:
        continue

    url = "https://staging.bsky.app/profile/" + author + "/post/" + post_id

    roll_up = "https://bsky.link?show_thread=t&url=" + url

    ap.create_post(f"Hey! Here is your rolled up thread!", post_uri, post_cid, url=roll_up)

    with open(HOME_DIR + "sent.txt", "a") as f:
        f.write(post_id + "\n")
