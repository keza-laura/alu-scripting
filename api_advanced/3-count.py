#!/usr/bin/python3
"""
3-count
"""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively queries Reddit API, parses hot article titles,
    and prints sorted count of given keywords.
    """

    # Initialize counts dictionary only on first call
    if counts is None:
        counts = {}

        # Normalize word_list and count duplicates
        for word in word_list:
            word_lower = word.lower()
            if word_lower in counts:
                counts[word_lower] += 1
            else:
                counts[word_lower] = 1

    # Reddit API URL
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    headers = {
        "User-Agent": "my-reddit-app/1.0"
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

    # Invalid subreddit
    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    children = data.get("children", [])

    # Count occurrences in titles
    for post in children:
        title = post.get("data", {}).get("title", "")
        words = title.lower().split()

        for word in words:
            clean_word = word.strip(".,!?\"'()[]{}:;_")

            if clean_word in counts:
                counts[clean_word] += 1

    # Recursive call if more pages
    after = data.get("after")
    if after is not None:
        return count_words(subreddit, word_list, after, counts)

    # Final output (only once recursion is done)
    # Filter out words with no matches
    final_counts = {k: v - word_list.count(k)
                    for k, v in counts.items()
                    if v - word_list.count(k) > 0}

    # Sort by count desc, then alphabetically
    sorted_words = sorted(
        final_counts.items(),
        key=lambda x: (-x[1], x[0])
    )

    for word, count in sorted_words:
        print("{}: {}".format(word, count))
