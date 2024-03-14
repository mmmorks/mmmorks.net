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

# Elegent theme customization
TAGS_URL = "tags"
CATEGORIES_URL = "categories"
ARCHIVES_URL = "archives"
ARTICLE_URL = "{slug}"
PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}.html"
