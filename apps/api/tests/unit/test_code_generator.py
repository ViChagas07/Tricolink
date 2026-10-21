import pytest

from tricolink.modules.links.domain.code_generator import BASE62, CODE_LENGTH, CodeGenerator
from tricolink.modules.links.domain.reserved_aliases import RESERVED_ALIASES
from tricolink.modules.links.domain.value_objects import ShortCode


def test_code_generator_uses_seven_base62_characters() -> None:
    generator = CodeGenerator()
    codes = {generator.generate() for _ in range(1000)}

    assert len(codes) >= 990
    assert all(len(code) == CODE_LENGTH == 7 for code in codes)
    assert all(set(code) <= set(BASE62) for code in codes)


def test_code_generator_can_be_made_deterministic() -> None:
    generator = CodeGenerator(choice=lambda _: "a")

    assert generator.generate() == "aaaaaaa"


def test_code_generator_validates_configuration() -> None:
    with pytest.raises(ValueError):
        CodeGenerator(length=2)
    with pytest.raises(ValueError):
        CodeGenerator(length=33)
    with pytest.raises(ValueError):
        CodeGenerator(alphabet="a")


def test_reserved_aliases_cover_application_routes() -> None:
    expected = {
        "login",
        "account",
        "links",
        "api",
        "r",
        "en",
        "pt-br",
        "admin",
        "static",
        "_next",
        "favicon.ico",
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
    }
    assert expected <= RESERVED_ALIASES
    assert all(ShortCode.is_reserved(alias) for alias in expected)
