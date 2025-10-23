from tts2sv import text


def test_syllables_without_pyphen():
    result = text.syllabify_text("Hello, world!")
    assert result == ["Hel", "lo", ",", "world", "!"]


def test_syllables_with_pyphen(monkeypatch):
    class DummyDict:
        def inserted(self, word: str) -> str:
            if word.lower() == "hello":
                return "Hel-lo"
            return word

    monkeypatch.setattr(text, "get_pyphen_dict", lambda lang: DummyDict())
    result = text.syllabify_text("Hello")
    assert result == ["Hel", "lo"]
