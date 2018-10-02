import argparse
import urllib.request
from bs4 import BeautifulSoup

def get_urls(subreddit, max_pages=0):
    """
    Get the URLs for all available pages of a subreddit (sorted by new)
    to avoid clicking through tens of pages.
    """

    # Must use old reddit since new reddit uses infinite scroll.
    base_url = "https://old.reddit.com/r/"
    headers = {"User-Agent": "Mozilla/5.0"}

    url = base_url + subreddit + "/new/"
    urls = []
    while url:
        urls.append(url)

        if len(urls) >= max_pages > 0:
            break

        request = urllib.request.Request(url, headers=headers)
        try:
            page = urllib.request.urlopen(request)
            soup = BeautifulSoup(page, "html.parser")
            url = soup.find("span", {"class": "next-button"}).find("a")["href"]
        except AttributeError as e:
            url = None
        except Exception as e:
            raise e

    return urls

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sub", type=str, help="Name of subreddit")
    ap.add_argument("-n", "--num-pages", type=int, default=0,
        help="Maximum number of pages to return")
    args = vars(ap.parse_args())

    urls = get_urls(args["sub"], args["num_pages"])
    for url in urls:
        print(url)
