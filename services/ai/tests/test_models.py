import pytest
from pydantic import ValidationError

from juristkr_ai.models import Article, Codex


def make_article(**overrides: object) -> Article:
    fields: dict[str, object] = {
        "codex": Codex.CRIMINAL,
        "number": "130",
        "title": "Убийство",
        "text": "Убийство, то есть умышленное причинение смерти другому человеку, -",
        "chapter": "Глава 24. Преступления против жизни",
        "section": "Раздел VII. Преступления против личности",
    }
    fields.update(overrides)
    return Article.model_validate(fields)


def test_citation_uses_codex_short_name() -> None:
    assert make_article().citation == "УК КР, ст. 130"


def test_point_id_is_stable_for_same_article() -> None:
    assert make_article().point_id == make_article(text="другая редакция").point_id


def test_point_id_differs_between_articles() -> None:
    assert make_article(number="130").point_id != make_article(number="131").point_id


@pytest.mark.parametrize("number", ["1", "130", "51-1"])
def test_accepts_valid_article_numbers(number: str) -> None:
    assert make_article(number=number).number == number


@pytest.mark.parametrize("number", ["", "ст. 130", "130a", "-1"])
def test_rejects_invalid_article_numbers(number: str) -> None:
    with pytest.raises(ValidationError):
        make_article(number=number)


def test_rejects_blank_text() -> None:
    with pytest.raises(ValidationError):
        make_article(text="   ")


def test_article_is_immutable() -> None:
    article = make_article()
    with pytest.raises(ValidationError):
        article.title = "Другое"


def test_codex_from_string() -> None:
    assert make_article(codex="criminal").codex is Codex.CRIMINAL
