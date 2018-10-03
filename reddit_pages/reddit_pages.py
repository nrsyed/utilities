import argparse
import urllib.request
from bs4 import BeautifulSoup

def get_urls(subreddit, max_pages=0, category="hot"):
    """!

    @brief Get the URLs for all available pages of a subreddit to avoid
    clicking through tens of pages.

    This script is not equivalent to a search, as Reddit currently caps the
    number of threads that can be viewed (by clicking "next" at the bottom of
    each page of a subreddit) at 1000. Older threads still exist and can be
    found through a Reddit search or Google (or other search engine) search.

    @param subreddit Name of the subreddit (e.g., "AskEngineers", not
        "r/AskEngineers").
    @param max_pages Maximum number of pages of threads to return. In practice,
        due to the 1000 thread limit, up to 40 pages will be returned
        (25 threads per page).
    @param category Subreddit thread category: hot (default), new, rising,
        controversial, top, or gilded.
    @return urls A list of urls corresponding to the available pages.
    """

    if category not in ("hot", "new", "rising", "controversial", "top", "gilded"):
        category = "hot"

    # Add header to allow https.
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
        page = urllib.request.urlopen(request)
        soup = BeautifulSoup(page, "html.parser")
        span_tags = soup.find("span", {"class": "next-button"})
        
        if span_tags is not None:
            url = span_tags.find("a")["href"]
        else:
            url = None

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
