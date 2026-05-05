import pytest
from main import process_inline, markdown_to_plain


def test_process_inline_bold():
    assert process_inline("**bold**") == "bold"


def test_process_inline_link():
    assert process_inline("[text](url)") == "text (url)"


def test_process_inline_image():
    assert process_inline("![alt](img.png)") == "Image: alt (img.png)"


def test_process_inline_strikethrough():
    assert process_inline("~~striked~~") == "striked"


def test_process_inline_code():
    assert process_inline("`code`") == "code"


def test_process_inline_italic():
    assert process_inline("*italic*") == "italic"


def test_process_inline_combined():
    assert process_inline("***bolditalic***") == "bolditalic"


def test_process_inline_no_formatting():
    assert process_inline("plain text") == "plain text"


def test_process_inline_empty_string():
    assert process_inline("") == ""


def test_process_inline_invalid_type():
    with pytest.raises(TypeError, match="Expected a string"):
        process_inline(42)


def test_markdown_to_plain_headers():
    md = "# Main Title\nSome paragraph.\n\n## Section\nAnother paragraph.\n\n### Subsection\nContent."
    result = markdown_to_plain(md)
    expected = (
        "Main Title\n"
        "===========\n"
        "Some paragraph.\n"
        "\n"
        "Section\n"
        "-------\n"
        "Another paragraph.\n"
        "\n"
        "Subsection\n"
        "~~~~~~~~~~\n"
        "Content."
    )
    assert result == expected


def test_markdown_to_plain_paragraphs():
    md = "First paragraph.\n\nSecond paragraph."
    result = markdown_to_plain(md)
    expected = "First paragraph.\n\nSecond paragraph."
    assert result == expected


def test_markdown_to_plain_unordered_list():
    md = "* item1\n* item2\n* item3"
    result = markdown_to_plain(md)
    expected = "* item1\n* item2\n* item3"
    assert result == expected


def test_markdown_to_plain_ordered_list():
    md = "1. first\n2. second\n3. third"
    result = markdown_to_plain(md)
    expected = "1. first\n2. second\n3. third"
    assert result == expected


def test_markdown_to_plain_mixed_list_symbols():
    md = "- dash\n+ plus\n* asterisk"
    result = markdown_to_plain(md)
    expected = "* dash\n* plus\n* asterisk"
    assert result == expected


def test_markdown_to_plain_blockquote():
    md = "> quoted line\n> another line"
    result = markdown_to_plain(md)
    expected = "> quoted line\n> another line"
    assert result == expected


def test_markdown_to_plain_fenced_code_block():
    md = "```\nprint('hello')\n```\nAfter block."
    result = markdown_to_plain(md)
    expected = "\n    print('hello')\n\nAfter block."
    assert result == expected


def test_markdown_to_plain_horizontal_rule():
    md = "before\n---\nafter"
    result = markdown_to_plain(md)
    expected = "before\n" + "-" * 60 + "\nafter"
    assert result == expected


def test_markdown_to_plain_inline_formatting_in_header():
    md = "# **bold** title\nparagraph"
    result = markdown_to_plain(md)
    expected = "bold title\n==========\nparagraph"
    assert result == expected


def test_markdown_to_plain_empty_input():
    assert markdown_to_plain("") == ""


def test_markdown_to_plain_only_blank_lines():
    assert markdown_to_plain("\n\n") == "\n\n"


def test_markdown_to_plain_trailing_paragraph():
    md = "first\n\n## header\nlast paragraph"
    result = markdown_to_plain(md)
    expected = "first\n\nheader\n------\nlast paragraph"
    assert result == expected


def test_markdown_to_plain_invalid_type():
    with pytest.raises(TypeError, match="Expected a string"):
        markdown_to_plain(None)