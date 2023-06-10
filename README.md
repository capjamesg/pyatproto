# AT Protocol Python Library

[![version](https://badge.fury.io/py/pyatproto.svg)](https://badge.fury.io/py/pyatproto)
[![downloads](https://img.shields.io/pypi/dm/pyatproto)](https://pypistats.org/packages/pyatproto)
[![license](https://img.shields.io/pypi/l/pyatproto)](https://github.com/capjamesg/pyatproto/blob/main/LICENSE)
[![python-version](https://img.shields.io/pypi/pyversions/pyatproto)](https://badge.fury.io/py/pyatproto)

A wrapper for interacting with the [AT Protocol API](https://atproto.com/), specifically for the [Bluesky](https://bsky.app/) social network.

*Note: There are some hard-coded Bluesky method names in this library, so the current version will not work with other AT Protocol implementations. The plan is to change this as new servers become available.*

## Getting Started

To install the library, run:

```
pip install pyatproto
```

## Quickstart

```
import pyatproto as atproto
import os

ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
USERNAME = os.environ.get("ATPROTO_USERNAME")
PASSWORD = os.environ.get("ATPROTO_PASSWORD")

ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

create_post = ap.create_post("My First Post")

print(create_post)
```

## Example Scripts

- [quickstart.py](quickstart.py): Authenticate and create a post on Bluesky.
- [crawler.py](crawler.py): Find the messages posted by each person a user follows, recursively (rate limits prevent this being used for crawling the whole network without adjusting the logic, however).
- [unroll.py](unroll.py): Find the parent of a message for use with the [bsky.link](https://bsky.link) thread unrolling feature.

## Contributing

Contributions are welcome, especially those that add more methods to the library. Please open an issue or pull request to contribute to the library.

## License

This project is licensed under an [MIT 0 License](LICENSE).

## Contributors

- capjamesg
