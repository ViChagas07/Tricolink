from __future__ import annotations

import secrets
from collections.abc import Callable

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
CODE_LENGTH = 7


class CodeGenerator:
    def __init__(
        self,
        *,
        alphabet: str = BASE62,
        length: int = CODE_LENGTH,
        choice: Callable[[str], str] = secrets.choice,
    ) -> None:
        if length < 3 or length > 32:
            raise ValueError("length must be between 3 and 32")
        if len(alphabet) < 2:
            raise ValueError("alphabet must contain at least two characters")
        self._alphabet = alphabet
        self._length = length
        self._choice = choice

    def generate(self) -> str:
        return "".join(self._choice(self._alphabet) for _ in range(self._length))
