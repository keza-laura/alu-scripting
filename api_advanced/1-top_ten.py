#!/usr/bin/python3
"""
Module that queries the Reddit API and prints
the titles of the first 10 hot posts of a subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts.
    If the subreddit is invalid, prints None.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "alu-reddit-top-ten-script/1.0"
    }

    params = {
        "limit": 10
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )

        if response.status_code != 200:
            print(None)
            return

        data = response.json().get("data", {}).get("children", [])

        for post in data:
            print(post.get("data", {}).get("title"))

    except Exception:
        print(None)
