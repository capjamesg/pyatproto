# AT Protocol Python Library

A wrapper for interacting with the [AT Protocol API](https://atproto.com/).

## Getting Started

To install the library, run:

```
pip install pyatproto
```

## Quickstart

```
import atproto
import os

ENDPOINT = os.environ.get("ATPROTO_ENDPOINT")
USERNAME = os.environ.get("ATPROTO_USERNAME")
PASSWORD = os.environ.get("ATPROTO_PASSWORD")

ap = atproto.AtProtoConfiguration(ENDPOINT, USERNAME, PASSWORD)

create_post = ap.create_post("My First Post")

print(create_post)
```

## Contributing

Contributions are welcome, especially those that add more methods to the library. Please open an issue or pull request to contribute to the library.

## License

This project is licensed under an [MIT 0 License](LICENSE).

## Contributors

- capjamesg