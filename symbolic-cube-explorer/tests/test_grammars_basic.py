from cube_explorer.grammars import get_grammar, list_grammars

def test_registry_has_expected() -> None:
    names = set(list_grammars())
    assert {"sefer", "runes", "enochian"}.issubset(names)

def test_validate_sequence_gives_good_error() -> None:
    g = get_grammar("sefer")
    try:
        g.validate_sequence(["א", "X", "ש"])
        assert False, "expected ValueError"
    except ValueError as e:
        msg = str(e)
        assert "Invalid symbols" in msg
        assert "Known" in msg
