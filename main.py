from fasthtml.common import *

import markdown
import frontmatter
import os
import sys

from pages.components import Post
from pages.index import IndexPage

production = False

if len(sys.argv) > 1 and sys.argv[1] == 'prod':
    production = True



app, rt = fast_app(
    live=not production,
    pico=False,
    htmx=False,
    surreal=False,
    hdrs=(
        Link(rel='stylesheet', href="https://unpkg.com/franken-ui@2.0.0/dist/css/core.min.css", type='text/css'),
        Link(rel='stylesheet', href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Merriweather:ital,wght@0,400;0,700;0,900;1,400;1,700;1,900&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&display=swap"),
        Link(rel='stylesheet', href="./assets/styles.css", type='text/css'),
        Style('''
            :root {
              /* Light theme - keeping for reference but with Gruvbox light colors */
              --background: 43 38% 84%;        /* #fbf1c7 (light medium background) */
              --foreground: 40 3% 23%;         /* #3c3836 (light foreground) */
              --card: 44 36% 86%;              /* #f2e5bc (light soft background) */
              --card-foreground: 40 3% 23%;    /* #3c3836 (light foreground) */
              --popover: 43 38% 84%;           /* #fbf1c7 (light medium background) */
              --popover-foreground: 40 3% 23%; /* #3c3836 (light foreground) */
              --primary: 100 22% 35%;          /* #689d6a (aqua) */
              --primary-foreground: 0 0% 100%; /* white */
              --secondary: 44 34% 70%;         /* #d5c4a1 (light muted) */
              --secondary-foreground: 0 0% 0%; /* black */
              --muted: 44 36% 86%;             /* #f2e5bc (light soft background) */
              --muted-foreground: 40 6% 40%;   /* #665c54 (light muted foreground) */
              --accent: 58 31% 35%;            /* #98971a (green) */
              --accent-foreground: 40 3% 23%;  /* #3c3836 (light foreground) */
              --destructive: 0 73% 46%;        /* #cc241d (red) */
              --destructive-foreground: 43 38% 84%; /* #fbf1c7 (light background) */
              --border: 41 25% 40%;            /* #7c6f64 (light gray) */
              --input: 40 6% 40%;              /* #665c54 (light muted foreground) */
              --ring: 100 22% 35%;             /* #689d6a (aqua) */
              --radius: 0.5rem;
            }

            .dark {
              /* Gruvbox dark theme */
              --background: 195 6% 12%;         /* #282828 (dark medium background) */
              --foreground: 53 74% 91%;        /* #f9f5d7 (dark foreground) */
              --card: 20 6% 15%;               /* #282828 (dark medium background) */
              --card-foreground: 43 38% 84%;   /* #ebdbb2 (dark foreground) */
              --popover: 20 7% 12%;            /* #1d2021 (dark hard background) */
              --popover-foreground: 43 38% 84%; /* #ebdbb2 (dark foreground) */
              --primary: 29 74% 58%;           /* #fe8019 (bright orange) */
              --primary-foreground: 53 74% 91%; /* white */
              --secondary: 21 6% 19%;          /* #32302f (dark soft background) */
              --secondary-foreground: 53 74% 91%; /* white */
              --muted: 21 8% 25%;              /* #3c3836 (dark muted background) */
              --muted-foreground: 40 9% 63%;   /* #a89984 (dark gray) */
              --accent: 122 21% 51%;            /* #b8bb26 (bright green) */
              --accent-foreground: 43 38% 84%; /* #ebdbb2 (dark foreground) */
              --destructive: 0 73% 55%;        /* #fb4934 (bright red) */
              --destructive-foreground: 43 38% 84%; /* #ebdbb2 (dark foreground) */
              --border: 20 12% 30%;            /* #504945 (dark border) */
              --input: 20 12% 30%;             /* #504945 (dark border) */
              --ring: 29 74% 58%;              /* #fe8019 (bright orange) */
              --radius: 0.5rem;
            }

            h1, h2, h3, h4 {
                font-family: Jetbrains Mono, monospace;
            }

            .mono {
                font-family: Jetbrains Mono, monospace;
            }

            html {
                scrollbar-gutter: stable;
            }

        '''),
        Script(
            '''{
                "imports": {
                  "three": "https://cdn.jsdelivr.net/npm/three@0.174.0/build/three.module.js",
                  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.174.0/examples/jsm/",
                  "mathjs": "https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.min.js"
                }
            }''',
            type="importmap",
        ),
        Script(
            src="https://unpkg.com/franken-ui@2.0.0/dist/js/core.iife.js",
            type="module"
        ),
        Script(
            src="https://unpkg.com/franken-ui@2.0.0/dist/js/icon.iife.js",
            type="module"
        ),
    )
)

article_names = os.listdir('articles')
md = markdown.Markdown()
articles = []

for article_name in article_names:
    with open(os.path.join('articles', article_name), 'r') as article:
        article = frontmatter.load(article)
        article.content = md.convert(article.content)
        article['url'] = article_name.split('.')[0]
        articles.append(article)

def PostPage(article):
    return Title(article['title']), Post(article)

# Create a function factory to create route handlers
def create_article_handler(article_obj):
    def handler():
        return PostPage(article_obj)
    return handler

for article in articles:
    app.get('/'+article['url'])(create_article_handler(article))

@app.get('/')
def Index():
    return Title('Sawyer Powell'), IndexPage(articles)

serve()
