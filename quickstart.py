import os

import atproto

ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
USERNAME = os.environ.get("ATPROTO_USERNAME")
PASSWORD = os.environ.get("ATPROTO_PASSWORD")

if not ENDPOINT or not USERNAME or not PASSWORD:
    raise ValueError("Please set the ATPROTO_ENDPOINT, ATPROTO_USERNAME and ATPROTO_PASSWORD environment variables.")

ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

create_post = ap.create_post("My First Post")

print(create_post)
