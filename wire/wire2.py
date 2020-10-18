""" Client for Reuters The Wire API """
import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from bs4 import BeautifulSoup  # type: ignore

FILTER_EXPRESSIONS = [
    re.compile(pattern)
    for pattern in [
        "Our Standards: The Thomson Reuters Trust Principles.",
        r"\d* Min Read",
    ]
]


@dataclass
class Article:
    """ An article """

    id: str
    headline: str
    paragraphs: List[str]
    keywords: List[str]
    published_at: datetime
    url: str


@dataclass
class Headline:
    """ A headline from The Wire API """

    id: str
    headline: str
    date_millis: int
    date_formatted: str
    url: str
    main_pic_url: str


def parse_headlines(wire_data: str) -> List[Headline]:
    """ Make Headlines from raw wire data """

    def parse_headline(raw_headline: Dict[str, Any]) -> Headline:
        return Headline(
            id=raw_headline["id"],
            headline=raw_headline["headline"],
            date_millis=int(raw_headline["dateMillis"]),
            date_formatted=raw_headline["formattedDate"],
            url=raw_headline["url"],
            main_pic_url=raw_headline["mainPicUrl"],
        )

    headlines: List[Headline] = [
        parse_headline(raw_headline)
        for raw_headline in json.loads(wire_data)["headlines"]
    ]
    return headlines


def _get_keywords(soup: BeautifulSoup) -> List[str]:
    """Extract keywords from Reuters article soup

    Args:
        soup: Beautifulsoup of a Reuters article
    Returns:
        keywords: Comma separated keywords

    """
    return soup.find("meta", {"name": "keywords"})["content"].split(",")


def _get_paragraphs(soup: BeautifulSoup) -> List[str]:
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

        excludes = ["Related Coverage", ""]
        cleaned_paragraph_texts = [
            text for text in cleaned_paragraph_texts if text not in excludes
        ]

        return cleaned_paragraph_texts

    article_body = soup.find("div", {"class": "ArticleBodyWrapper"})
    paragraphs = article_body.find_all("p")
    paragraph_texts = [p.get_text() for p in paragraphs]

    return clean_paragraphs(paragraph_texts)


def _get_datetime(date_millis: int) -> datetime:
    """ Get datetime from epoch milliseconds """
    date_seconds = date_millis / 1000.0
    return datetime.utcfromtimestamp(date_seconds)


def make_article(headline: Headline, raw_article: str) -> Article:
    """ Build an Article """
    soup = BeautifulSoup(raw_article, "lxml")

    article = Article(
        id=headline.id,
        headline=headline.headline,
        paragraphs=_get_paragraphs(soup),
        keywords=_get_keywords(soup),
        published_at=_get_datetime(headline.date_millis),
        url=headline.url,
    )

    return article
