from fasthtml.common import *
from .components import *

def IndexPage(articles): 
    visible_articles = list(filter(lambda a: a['visible'] == True, articles))
    visible_articles.sort(key=lambda a: a['date'], reverse=True)

    return PageContainer( 
        Logo(),
        Subtitle("computer science / engineering / art"),
        Div(id="centerpiece", cls="flex justify-center"),
        Div(
            Div(
                A(
                    "about",
                    href="/about",
                    cls="uk-btn uk-btn-default shadow-xl p-2 px-4 mono transition-all",
                    style="height: 48px; border-radius: 100px",
                ),
                A(
                    "cv",
                    href="/professional-work",
                    cls="uk-btn uk-btn-default shadow-xl p-2 ms-2 px-4 mono transition-all",
                    style="height: 48px; border-radius: 100px",
                ),
                cls="flex flex-row flex-1"
            ),
            Div(
                A(
                    NotStr('''<uk-icon icon="linkedin" height=24 width=24></uk-icon>'''),
                    cls="uk-btn uk-btn-default shadow-xl p-2 flex-end transition-all",
                    style="border-radius: 50%; width: 48px; height: 48px",
                    href="https://www.linkedin.com/in/sawyerhpowell/",
                    _target="none"
                ),
                A(
                    NotStr('''<uk-icon icon="github" height=24 width=24></uk-icon>'''),
                    cls="uk-btn uk-btn-default shadow-xl p-2 ms-2 flex-end transition-all",
                    style="border-radius: 50%; width: 48px; height: 48px",
                    href="https://github.com/Sawyer-Powell",
                    _target="none"
                ),
                cls="flex flex-row justify-end flex-1"
            ),
            cls="flex flex-row mb-4 xl:mx-4"
        ),
        Div(
            (ArticleCard(article) for article in visible_articles),
            cls="grid grid-cols-1 xl:grid-cols-2",
            data_uk_grid="masonry: true"
        ),
        Script(src='./assets/centerpiece.js', type='module'),
    )
