"""Utilities for finite words over a small operation alphabet."""

from __future__ import annotations

from itertools import product
from typing import Iterable, Sequence


def words_upto(alphabet: Sequence[str], max_length: int) -> list[str]:
    """Return the empty word and every word up to ``max_length``.

    Symbols are required to be non-empty strings. The current prototype uses
    string concatenation, so callers should normally use one-character symbols.
    """

    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    if not alphabet:
        raise ValueError("alphabet must not be empty")
    if any(not isinstance(symbol, str) or symbol == "" for symbol in alphabet):
        raise ValueError("every alphabet symbol must be a non-empty string")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet symbols must be unique")

    words = [""]
    for length in range(1, max_length + 1):
        words.extend("".join(symbols) for symbols in product(alphabet, repeat=length))
    return words


def validate_word(word: str, alphabet: Iterable[str]) -> None:
    """Raise ``ValueError`` when ``word`` contains an unknown symbol."""

    allowed = set(alphabet)
    unknown = [symbol for symbol in word if symbol not in allowed]
    if unknown:
        raise ValueError(f"word contains symbols outside the alphabet: {unknown}")
