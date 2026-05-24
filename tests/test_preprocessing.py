from src.preprocessing import clean_text


def test_clean_text_normalizes_spacing_and_case():
    text = "  Junior Python   Developer!!! With C++, Node.js and C#   "
    cleaned = clean_text(text)
    assert cleaned == "junior python developer with c++ node.js and c#"