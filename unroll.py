import os

import src.pyatproto as atproto
import requests

ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
USERNAME = os.environ.get("ATPROTO_USERNAME")
PASSWORD = os.environ.get("ATPROTO_PASSWORD")

if not ENDPOINT or not USERNAME or not PASSWORD:
    raise ValueError("Please set the ATPROTO_ENDPOINT, ATPROTO_USERNAME and ATPROTO_PASSWORD environment variables.")

ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

with open("sent.txt", "r") as f:
    sent = f.read().split("\n")

notifications = ap.get_notifications()

thumbnail = requests.get("https://bsky.app/img/default-social-card.png")

# get as blob
thumbnail = thumbnail.content

for notification in notifications:
    author = notification["author"]["handle"]

    post_uri = notification["uri"]
    post_cid = notification["cid"]

    if notification["record"].get("reply") is None:
        continue

    uri = notification["record"]["reply"]["parent"]["uri"]
    
    post_id = uri.split("/")[-1]

    text_content = notification["record"].get("text", "")

    if "unroll" not in text_content.lower() or post_id in sent:
        continue

    url = "https://staging.bsky.app/profile/" + author + "/post/" + post_id

    roll_up = "https://bsky.link?show_thread=t&url=" + url

    ap.create_post(f"Hey! Here is your rolled up thread!", post_uri, post_cid, url=roll_up)

    with open("sent.txt", "a") as f:
        f.write(post_id + "\n")
