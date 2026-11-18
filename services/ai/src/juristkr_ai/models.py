import uuid
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

_ARTICLE_NAMESPACE = uuid.UUID("6f1c2a4e-3b7d-4c55-9a0e-8d2f1b6c7e90")


class Codex(StrEnum):
    CRIMINAL = "criminal"

    @property
    def title(self) -> str:
        return _CODEX_TITLES[self]

    @property
    def short_name(self) -> str:
        return _CODEX_SHORT_NAMES[self]


_CODEX_TITLES = {Codex.CRIMINAL: "Уголовный кодекс Кыргызской Республики"}
_CODEX_SHORT_NAMES = {Codex.CRIMINAL: "УК КР"}


class Article(BaseModel):
    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    codex: Codex
    number: str = Field(pattern=r"^\d+(-\d+)?$")
    title: str = Field(min_length=1)
    text: str = Field(min_length=1)
    chapter: str = Field(min_length=1)
    section: str | None = None

    @property
    def point_id(self) -> str:
        return str(uuid.uuid5(_ARTICLE_NAMESPACE, f"{self.codex}:{self.number}"))

    @property
    def citation(self) -> str:
        return f"{self.codex.short_name}, ст. {self.number}"
