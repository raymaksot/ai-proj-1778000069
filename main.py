import re
import sys


def process_inline(text: str) -> str:
    """Remove inline formatting from a markdown text span."""
    if not isinstance(text, str):
        raise TypeError(f"Expected a string, got {type(text).__name__}")

    try:
        # Images: ![alt](url) -> Image: alt (url)
        text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'Image: \1 (\2)', text)
        # Links: [text](url) -> text (url)
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (\2)', text)
        # Bold + italic (***text***)
        text = re.sub(r'\*\*\*(.*?)\*\*\*', r'\1', text)
        # Bold (**text**)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        # Italic (*text*)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        # Strikethrough (~~text~~)
        text = re.sub(r'~~(.*?)~~', r'\1', text)
        # Inline code (`text`)
        text = re.sub(r'`(.*?)`', r'\1', text)
    except re.error:
        # If a regex fails unexpectedly, return text unchanged
        pass
    return text


def markdown_to_plain(md: str) -> str:
    if not isinstance(md, str):
        raise TypeError(f"Expected a string, got {type(md).__name__}")

    lines = md.splitlines()
    output = []
    para_buffer = []
    in_fenced = False
    fence_marker = ""

    def flush_paragraph():
        if para_buffer:
            paragraph = ' '.join(para_buffer)
            output.append(process_inline(paragraph))
            para_buffer.clear()

    for line in lines:
        # Handle fenced code blocks
        if in_fenced:
            if line.strip().startswith(fence_marker) and line.strip() == fence_marker:
                in_fenced = False
            else:
                output.append(f"    {line}")
            continue

        if line.strip().startswith("```"):
            flush_paragraph()
            in_fenced = True
            fence_marker = line.strip()[:3]  # usually ```
            # output a blank line before code block
            output.append("")
            continue

        # Empty line triggers paragraph flush
        if line.strip() == "":
            flush_paragraph()
            output.append("")
            continue

        # Headers
        header_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if header_match:
            flush_paragraph()
            level = len(header_match.group(1))
            header_text = process_inline(header_match.group(2))
            if level == 1:
                output.append(header_text)
                output.append("=" * len(header_text))
            elif level == 2:
                output.append(header_text)
                output.append("-" * len(header_text))
            else:
                indent = "  " * (level - 3) if level >= 3 else ""
                underline_char = "~"
                output.append(f"{indent}{header_text}")
                output.append(f"{indent}{underline_char * len(header_text)}")
            continue

        # Blockquote
        if line.startswith("> "):
            flush_paragraph()
            content = line[2:]
            output.append(f"> {process_inline(content)}")
            continue

        # Unordered list items
        if re.match(r'^[\*\-\+]\s+', line):
            flush_paragraph()
            content = re.sub(r'^[\*\-\+]\s+', '', line)
            output.append(f"* {process_inline(content)}")
            continue

        # Ordered list items
        if re.match(r'^\d+\.\s+', line):
            flush_paragraph()
            match = re.match(r'^(\d+\.)\s+(.*)', line)
            number = match.group(1)
            content = match.group(2)
            output.append(f"{number} {process_inline(content)}")
            continue

        # Horizontal rule
        if re.match(r'^(\-\-\-|\*\*\*|___)$', line.strip()):
            flush_paragraph()
            output.append("-" * 60)
            continue

        # Normal paragraph text
        para_buffer.append(line)

    flush_paragraph()  # Don't forget trailing paragraph

    return '\n'.join(output)


def main():
    sample = """
# Markdown to Plain Text Converter

This is a **simple** converter that *preserves* structure.

## Features

- Converts **headings** to underlined text.
- Supports `inline code` and ~~strikethrough~~.
- Handles [links](https://example.com) and ![images](image.png).

### Example Blockquote
> This is a blockquote with **bold** inside.

```
def hello():
    print("Hello World")
```

1. First item
2. Second item
3. Third item

---

End of document.
"""
    plain = markdown_to_plain(sample)
    print(plain)


if __name__ == '__main__':
    main()