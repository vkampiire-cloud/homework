"""
Homework Assignment: Query the Reddit API
==========================================
Collect the following information for a subreddit:
  1. The subreddit name
  2. The subreddit description
  3. Number of subscribers (subs)
  4. The subreddit rules
  5. The 10 newest posts

Requirements:
  - Use Python's `requests` library.
  - Set a custom, descriptive User-Agent header according to Reddit API rules.
"""

import requests


def get_subreddit_info(subreddit_name: str):
    """
    Queries Reddit's public API to retrieve and display information
    about the specified subreddit.
    """
    # --------------------------------------------------------------------------
    # REQUIREMENT: Set an appropriate custom User-Agent header
    # Format required by Reddit: <platform>:<app ID>:<version> (by /u/<username>)
    # --------------------------------------------------------------------------
    headers = {
        "User-Agent": "windows:homework_subreddit_query:v1.0 (by /u/student_dev)"
    }

    print("=" * 60)
    print(f"QUERYING REDDIT API FOR: r/{subreddit_name}")
    print("=" * 60)

    # ==========================================================================
    # 1. SUBREDDIT NAME, DESCRIPTION, AND NUMBER OF SUBS
    # Endpoint: https://www.reddit.com/r/{subreddit}/about.json
    # ==========================================================================
    about_url = f"https://www.reddit.com/r/{subreddit_name}/about.json"
    about_response = requests.get(about_url, headers=headers, allow_redirects=False)

    if about_response.status_code == 200:
        data = about_response.json().get("data", {})
        
        # 1. Subreddit Name
        sub_name = data.get("display_name_prefixed", f"r/{subreddit_name}")
        
        # 2. Number of Subs
        subscribers = data.get("subscribers", 0)
        
        # 3. Subreddit Description
        # 'public_description' is the short summary, 'description' is full text
        description = data.get("public_description") or data.get("description", "No description available.")

        print("\n[*] 1. SUBREDDIT DETAILS:")
        print(f"    - Subreddit Name: {sub_name}")
        print(f"    - Number of Subs: {subscribers:,}")
        print(f"    - Description:    {description.strip()[:200]}...")
    else:
        print(f"\n[-] Could not fetch about.json (Status Code: {about_response.status_code})")

    # ==========================================================================
    # 2. SUBREDDIT RULES
    # Endpoint: https://www.reddit.com/r/{subreddit}/about/rules.json
    # ==========================================================================
    rules_url = f"https://www.reddit.com/r/{subreddit_name}/about/rules.json"
    rules_response = requests.get(rules_url, headers=headers, allow_redirects=False)

    if rules_response.status_code == 200:
        rules_list = rules_response.json().get("rules", [])
        print("\n[*] 2. SUBREDDIT RULES:")
        if rules_list:
            for idx, rule in enumerate(rules_list, start=1):
                rule_title = rule.get("short_name", "Untitled Rule")
                print(f"    {idx}. {rule_title}")
        else:
            print("    No rules found for this subreddit.")
    else:
        print(f"\n[-] Could not fetch rules.json (Status Code: {rules_response.status_code})")

    # ==========================================================================
    # 3. 10 NEWEST POSTS
    # Endpoint: https://www.reddit.com/r/{subreddit}/new.json?limit=10
    # ==========================================================================
    new_posts_url = f"https://www.reddit.com/r/{subreddit_name}/new.json"
    params = {"limit": 10}
    posts_response = requests.get(new_posts_url, headers=headers, params=params, allow_redirects=False)

    if posts_response.status_code == 200:
        children = posts_response.json().get("data", {}).get("children", [])
        print("\n[*] 3. 10 NEWEST POSTS:")
        if children:
            for idx, child in enumerate(children, start=1):
                post_data = child.get("data", {})
                title = post_data.get("title", "No Title")
                author = post_data.get("author", "[deleted]")
                score = post_data.get("score", 0)
                print(f"    {idx:2d}. {title}")
                print(f"        (Author: u/{author} | Score: {score})")
        else:
            print("    No posts found.")
    else:
        print(f"\n[-] Could not fetch new.json (Status Code: {posts_response.status_code})")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Test with any subreddit, e.g. "learnpython", "python", "programming"
    get_subreddit_info("learnpython")
