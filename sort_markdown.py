import re

def sort_markdown_sections_and_lists(input_path: str, output_path: str = None):
    """
    Reads a Markdown file, sorts bullet lists alphabetically within each section,
    and sorts the sections themselves by their heading text.
    Keeps non-list content and formatting intact.
    """

    with open(input_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # Split into sections by top-level headings (lines starting with '# ')
    section_pattern = re.compile(r"(^# .*$)", re.MULTILINE)
    sections = section_pattern.split(markdown)

    # If the file doesn't start with a heading, the first chunk is preamble text
    preamble = ""
    if not sections[0].startswith("# "):
        preamble = sections.pop(0)

    # Pair each heading with its content
    paired_sections = []
    for i in range(0, len(sections), 2):
        if i + 1 < len(sections):
            heading = sections[i].strip()
            content = sections[i + 1]
        else:
            heading = sections[i].strip()
            content = ""
        paired_sections.append((heading, content))

    def sort_bullet_lists(text: str) -> str:
        """Sorts each bullet list alphabetically within the given text."""
        lines = text.splitlines()
        output_lines = []
        current_list = []

        def flush_current_list():
            if not current_list:
                return
            parsed = []
            for line in current_list:
                stripped = line.lstrip()
                indent = len(line) - len(stripped)
                bullet = stripped[0]
                text = stripped[1:].strip()
                parsed.append((indent, bullet, text))
            parsed.sort(key=lambda x: (x[0], x[2].lower()))
            for indent, bullet, text in parsed:
                output_lines.append(" " * indent + f"{bullet} {text}")
            current_list.clear()

        bullet_pattern = re.compile(r"^\s*[-*+]\s+")
        for line in lines:
            if bullet_pattern.match(line):
                current_list.append(line)
            else:
                flush_current_list()
                output_lines.append(line)
        flush_current_list()

        return "\n".join(output_lines)

    # Sort bullet lists inside each section
    for i, (heading, content) in enumerate(paired_sections):
        paired_sections[i] = (heading, sort_bullet_lists(content))

    # Sort sections by their heading text (case-insensitive)
    paired_sections.sort(key=lambda x: x[0].lower())

    # Reassemble the document
    sorted_markdown = preamble
    for heading, content in paired_sections:
        sorted_markdown += f"\n{heading}\n{content.strip()}\n"

    sorted_markdown = sorted_markdown.strip() + "\n"

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sorted_markdown)
        print(f"✅ Sorted markdown saved to '{output_path}'")
    else:
        print(sorted_markdown)


# Example usage
if __name__ == "__main__":
    input_file = "README.md"
    output_file = "README_sorted.md"
    sort_markdown_sections_and_lists(input_file, output_file)

