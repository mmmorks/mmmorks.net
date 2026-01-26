AUTHOR = 'mmmorks'
SITENAME = 'mmmorks.net'
SITEURL = "https://mmmorks.net"
LANDING_PAGE_TITLE = "Reverse engineering, car hacking"

PATH = "content"

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
)

# Social widget
SOCIAL = (
    ("Mastodon", "https://infosec.exchange/@mmmorks"),
    ("Bluesky", "https://bsky.app/profile/mmmorks.net"),
    ("Github", "https://github.com/mmmorks"),
)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

COMMENTBOX_PROJECT = '5746575435366400-proj'

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.toc': {
            'toc_depth': 2,
        },
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# Plugins
import os
PLUGIN_PATHS = [os.path.join(os.path.dirname(__file__), "..", "pelican-plugins")]
PLUGINS = ["extract_toc", "post_stats"]
