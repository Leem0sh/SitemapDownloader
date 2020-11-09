import bs4 as bs
import requests
import urllib.request
import sys
import time


class SitemapSeeker:
    def __init__(self):
        if len(sys.argv) > 1:
            self.link = sys.argv[1]
        else:
            print(
                "Chybějící nebo neplatný argument. Zadej ve tvaru >> python sitemap_urls.py http(s)://(www.)seznam.cz/sitemap.xml <<"
            )
            exit(1)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
            "content-type": "application/json",
            "accept": "application/json",
            "cache-control": "no-cache",
        }

    def requester(self, url):
        req = urllib.request.Request(url, headers=self.headers)
        response = urllib.request.urlopen(req)
        content = bs.BeautifulSoup(response, "xml")
        return content


if __name__ == "__main__":
    with open("SITEMAP_URLS.txt", "w", encoding="utf-8") as sitemap_file:
        app = SitemapSeeker()
        sitemap_content = app.requester(app.link)
        for url in sitemap_content.find_all("loc"):
            print(url.text)
            if r".xml" in url.text:
                part_content = app.requester(url.text)
                for x in part_content.find_all("loc"):
                    sitemap_file.write(x.text + "\n")
            else:
                sitemap_file.write(url.text + "\n")
    print("Script complete - check ./SITEMAP_URLS.txt for results.")