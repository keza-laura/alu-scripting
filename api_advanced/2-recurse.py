#!/usr/bin/python3
"""
Module that recursively queries the Reddit API and
returns a list of titles of all hot articles.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively retrieves all hot post titles for a subreddit.
    Returns a list of titles, or None if subreddit is invalid.
    """

    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "alu-reddit-recursion-script/1.0"
    }

    params = {
        "limit": 100,
        "after": after
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    if response.status_code != 200:
        return None

    data = response.json().get("data")

    children = data.get("children")
    for post in children:
        hot_list.append(post.get("data").get("title"))

    after = data.get("after")

    if after is None:
        return hot_list

    return recurse(subreddit, hot_list, after)
