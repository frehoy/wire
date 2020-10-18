""" Placeholder tests module """
# pylint: disable=protected-access

from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore

from wire import wire

DIR_DATA = Path(__file__).resolve().parent.joinpath("data")


def load_wire() -> str:
    """ Load testing wire.json """
    with open(DIR_DATA.joinpath("wire.json"), "r") as f:
        return f.read()


def load_raw_article() -> str:
    """ Load article.html """
    with open(DIR_DATA.joinpath("article.html"), "r") as f:
        return f.read()


def load_soup() -> BeautifulSoup:
    """ Load soup from raw article """
    return BeautifulSoup(load_raw_article(), "lxml")


def test_article() -> None:
    """ Test Article constructor """
    article = wire.Article(
        id="fake_id",
        headline="fake headline",
        paragraphs=["parag 1", "parag 2"],
        keywords=["fake", "news"],
        published_at=datetime.now(),
        url="https://example.com",
    )

    assert article.id == "fake_id"
    assert article.keywords == ["fake", "news"]


def test_parse_headlines() -> None:
    """ Test that parse_headlines produces a list of Headline """
    data = load_wire()
    headlines = wire.parse_headlines(data)

    assert isinstance(headlines, list)
    for headline in headlines:
        assert isinstance(headline, wire.Headline)

    first_headline = headlines[0]
    assert first_headline.id == "USKBN2720VH"
    assert first_headline.date_formatted == "20m ago"


def test_get_keywords():
    """ Test that _get_keywords gets some keywords """
    wanted = [
        "UK",
        "ARMENIA",
        "AZERBAIJAN",
        "International / National Security",
    ]
    got = wire._get_keywords(load_soup())
    for keyword in wanted:
        assert keyword in got


def test_get_paragraphs():
    """ Test that _get_paragraphs returns correct paragraphs """
    paragraphs = wire._get_paragraphs(load_soup())
    # assert len(paragraphs) == 23
    for paragraph in paragraphs:
        assert isinstance(paragraph, str)
        assert not paragraph == ""
        assert not paragraph == "RELATED COVERAGE"


def test_make_article() -> None:
    """ Test that make_article returns an Article """
    fake_headline = wire.Headline(
        id="fake",
        headline="fake headline",
        date_millis=1603053308000,
        date_formatted="Just now",
        url="https://example.com",
        main_pic_url="https://example.com/image.jpeg",
    )

    article = wire.make_article(headline=fake_headline, raw_article=load_raw_article())
    assert isinstance(article, wire.Article)
