""" Wire

A simple terminal-printing reader for The Wire

"""

import datetime
import re
import sys
import textwrap
import time
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup  # type: ignore

TTYPE_DELAY = 0.03
FETCH_DELAY = 60

URL_BASE = "https://www.reuters.com"
URL_WIRE = URL_BASE + "/assets/jsonWireNews"

FILTER_EXPRESSIONS = [
    re.compile(pattern)
    for pattern in [
        "Our Standards: The Thomson Reuters Trust Principles.",
        r"\d* Min Read",
    ]
]


def ttype_print(text: str, delay: float = TTYPE_DELAY, linewidth: int = 80) -> None:
    """Print text like a teletyper would

    Args:
        text: Text to print
        delay: Delay in seconds between each character
        linewidth: Width in characters

    """
    lines: List[str] = textwrap.wrap(text, width=linewidth)

    for line in lines:
        for character in line:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")

    sys.stdout.write("\n")


def get_keywords(soup) -> str:
    """Extract keywords from Reuters article

    Args:
        soup: Beatufilsoup of a Reuters article
    Returns:
        keywords: Comma separated keywords

    """
    kws = soup.find("meta", {"name": "keywords"})["content"].split(",")
    kws_separated = ", ".join(kws)
    keywords = f"Keywords: {kws_separated}"
    return keywords


def get_paragraphs(soup) -> List[str]:
    """Get a list of paragraphs from an article

    Args:
        soup: Beautifulsoup of a Reuters Article
    Returns:
        paragraphs: A list of paragraph strings.

    """

    def clean_paragraphs(paragraph_texts: List[str]) -> List[str]:
        cleaned_paragraph_texts = []
        for para_text in paragraph_texts:
            if not any([exp.match(para_text) for exp in FILTER_EXPRESSIONS]):
                cleaned_paragraph_texts.append(para_text)

        return cleaned_paragraph_texts

    article_body = soup.find("div", {"class": "ArticleBodyWrapper"})
    paragraphs = article_body.find_all("p")
    paragraph_texts = [p.get_text() for p in paragraphs]

    return clean_paragraphs(paragraph_texts)


def get_datetime(headline: Dict[str, str]) -> str:
    """ Get the date and time from a headline """
    return str(datetime.datetime.utcfromtimestamp(int(headline["dateMillis"]) / 1000.0))


def get_article(headline: Dict[str, Any]) -> Dict[str, Any]:
    """ Download and build an article dict """
    url = URL_BASE + headline["url"]

    article_raw = requests.get(url)
    soup = BeautifulSoup(article_raw.content, "lxml")

    article = {
        "id": headline["id"],
        "paragraphs": get_paragraphs(soup),
        "headline": headline["headline"],
        "keywords": get_keywords(soup),
        "datetime": get_datetime(headline),
        "url": url,
    }

    return article


def get_headlines() -> Dict[str, Any]:
    """ Fetch headlines from API """
    wire_raw = requests.get(URL_WIRE)
    headlines = wire_raw.json()["headlines"]
    return headlines


def print_articles(articles):
    """ Print articles """
    divider = "#" * 80
    for article in sorted(articles, key=lambda a: a["datetime"]):
        ttype_print(article["datetime"])
        ttype_print(article["headline"])
        for paragraph in article["paragraphs"]:
            ttype_print(paragraph)
        ttype_print(article["keywords"])
        ttype_print(article["url"])
        ttype_print(divider)


def main():
    """ Print articles in teleprinter style """
    finished_ids = []
    while True:
        headlines = get_headlines()
        articles = []
        for headline in headlines:
            if not headline["id"] in finished_ids:
                article = get_article(headline)
                finished_ids.append(headline["id"])
                articles.append(article)

        print_articles(articles)

        time.sleep(FETCH_DELAY)

        # prune finished_ids
        while len(finished_ids) > 1000:
            finished_ids.pop(0)


if __name__ == "__main__":
    main()
