"""Text tokenisation and syllabification utilities."""
from __future__ import annotations

import re
from functools import lru_cache
from typing import Iterable, List

try:
    import pyphen
except ImportError:  # pragma: no cover - optional dependency
    pyphen = None  # type: ignore


WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
VOWEL_GROUP_RE = re.compile(r"[aeiouyAEIOUY]+")


class TextSyllabifier:
    """Split text into syllables or punctuation tokens."""

    def __init__(self, lang: str = "en") -> None:
        self.lang = lang

    def syllabify(self, text: str) -> List[str]:
        text = text.strip()
        if not text:
            raise ValueError("Input text is empty")

        tokens: List[str] = []
        for raw_token in self._tokenize(text):
            if WORD_RE.fullmatch(raw_token):
                tokens.extend(self._syllabify_word(raw_token))
            else:
                tokens.append(raw_token)
        return tokens

    def _tokenize(self, text: str) -> Iterable[str]:
        splitter = re.finditer(r"\w+|[^\w\s]", text, flags=re.UNICODE)
        for match in splitter:
            yield match.group(0)

    def _syllabify_word(self, word: str) -> List[str]:
        hyphenated = self._hyphenate(word)
        if hyphenated:
            return [segment for segment in hyphenated.split("-") if segment]
        return self._fallback_syllables(word)

    def _fallback_syllables(self, word: str) -> List[str]:
        matches = list(VOWEL_GROUP_RE.finditer(word))
        if not matches:
            return [word]
        parts: List[str] = []
        last_idx = 0
        for idx, match in enumerate(matches):
            start = last_idx
            end = match.end()
            if idx < len(matches) - 1:
                next_start = matches[idx + 1].start()
                end = max(end, next_start)
            else:
                end = len(word)
            parts.append(word[start:end])
            last_idx = end
        if last_idx < len(word):
            parts[-1] = parts[-1] + word[last_idx:]
        return parts

    def _hyphenate(self, word: str) -> str | None:
        dictionary = get_pyphen_dict(self.lang)
        if dictionary is None:
            return None
        return dictionary.inserted(word)


@lru_cache(maxsize=None)
def get_pyphen_dict(lang: str):  # type: ignore[no-untyped-def]
    if pyphen is None:
        return None
    try:
        return pyphen.Pyphen(lang=lang)
    except KeyError:
        return pyphen.Pyphen(lang="en")


def syllabify_text(text: str, lang: str = "en") -> List[str]:
    """Convenience wrapper to syllabify a line of text."""
    return TextSyllabifier(lang=lang).syllabify(text)
