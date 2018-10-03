import argparse
import urllib.request
from bs4 import BeautifulSoup

def get_urls(subreddit, max_pages=0, category="hot"):
    """
    Get the URLs for all available pages of a subreddit to avoid clicking
    through tens of pages.
    """

    if category not in ("hot", "new", "rising", "controversial", "top", "gilded"):
        category = "hot"

    headers = {"User-Agent": "Mozilla/5.0"}

    # Must use old reddit since new reddit uses infinite scroll.
    base_url = "https://old.reddit.com/r/"
    url = base_url + subreddit

    if category != "hot":
        url += "/{}".format(category)

    urls = []
    while url:
        urls.append(url)

        if len(urls) >= max_pages > 0:
            break

        request = urllib.request.Request(url, headers=headers)
        try:
            page = urllib.request.urlopen(request)
            soup = BeautifulSoup(page, "html.parser")
            span_tags = soup.find("span", {"class": "next-button"})
            
            if span_tags is not None:
                url = span_tags.find("a")["href"]
            else:
                url = None
        except Exception as e:
            raise e

    return urls

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sub", type=str, help="Name of subreddit")
    ap.add_argument("-n", "--num-pages", type=int, default=0,
        help="Maximum number of pages to return")
    ap.add_argument("-c", "--category", type=str, default="hot",
        help="Category: hot (default), new, rising, controversial,"\
            "top, gilded.")
    args = vars(ap.parse_args())

    urls = get_urls(args["sub"], max_pages=args["num_pages"],
        category=args["category"])
    for url in urls:
        print(url)
