import pytest

from juristkr_ai.settings import Settings


def test_defaults_point_to_local_qdrant(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JURISTKR_QDRANT_URL", raising=False)
    monkeypatch.delenv("JURISTKR_QDRANT_COLLECTION", raising=False)

    settings = Settings(_env_file=None)

    assert settings.qdrant_url == "http://localhost:6333"
    assert settings.qdrant_collection == "articles"


def test_env_overrides_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JURISTKR_QDRANT_URL", "http://qdrant:6333")
    monkeypatch.setenv("JURISTKR_QDRANT_COLLECTION", "test-articles")

    settings = Settings(_env_file=None)

    assert settings.qdrant_url == "http://qdrant:6333"
    assert settings.qdrant_collection == "test-articles"
