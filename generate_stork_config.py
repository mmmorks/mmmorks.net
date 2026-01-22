#!/usr/bin/env python3
"""Generate stork.toml configuration from output HTML files."""
from pathlib import Path
from html.parser import HTMLParser


class TitleParser(HTMLParser):
    """Extract title from HTML."""
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and not self.title:
            self.title = data.strip()


def get_title_from_html(filepath):
    """Extract title from HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        parser = TitleParser()
        parser.feed(content)
        return parser.title or filepath.stem
    except Exception:
        return filepath.stem


def generate_stork_config(output_dir='output'):
    """Generate stork.toml configuration."""
    output_path = Path(output_dir)

    # Find all HTML files, excluding certain patterns
    exclude_patterns = ['404.html', 'authors.html', 'categories.html', 'tags.html', 'archives.html']
    html_files = []

    for html_file in output_path.glob('*.html'):
        if html_file.name not in exclude_patterns:
            html_files.append(html_file)

    # Generate TOML content - use "/" for root-relative URLs that work everywhere
    toml_content = ['[input]', 'base_directory = "output"', 'url_prefix = "/"', '']

    for html_file in sorted(html_files):
        title = get_title_from_html(html_file)
        # Don't include leading slash since url_prefix already has it
        url = html_file.name if html_file.name != "index.html" else ""

        toml_content.extend([
            '[[input.files]]',
            f'path = "{html_file.name}"',
            f'url = "{url}"',
            'filetype = "HTML"',
            f'title = "{title}"',
            ''
        ])

    # Write to stork.toml
    with open('stork.toml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(toml_content))

    print(f"Generated stork.toml with {len(html_files)} files")


if __name__ == '__main__':
    generate_stork_config()
