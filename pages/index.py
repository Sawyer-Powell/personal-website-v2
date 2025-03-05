from fasthtml.common import *
from .components import *

def IndexPage(): 
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
            ArticleCard(
                "Stargate and the Problem With AGI",
                "https://images.unsplash.com/photo-1576773689115-5cd2b0223523?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fHBhaW50aW5nfGVufDB8fDB8fHww",
                "https://google.com",
                ['ai', 'economics']
            ),
            ArticleCard(
                "Fossora",
                "https://the-public-domain-review.imgix.net/collections/atlas-des-champignons/deschampignonscatladesc_0011-featured.jpeg",
                "https://google.com",
                ['dist. systems']
            ),
            ArticleCard(
                "How Raft Safeguards Kubernetes",
                "https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=0.25&h=550&w=1920%20207w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=0.5&h=550&w=1920%20414w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=0.75&h=550&w=1920%20622w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&h=550&w=1920%20829w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=1.5&h=550&w=1920%201244w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=2&h=550&w=1920%201659w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=3&h=550&w=1920%202488w,https://www.datocms-assets.com/103094/1689259602-1506269777891914-7.jpg?auto=format%2Ccompress&dpr=4&h=550&w=1920%203318w",
                "https://google.com",
                ['dist. systems']
            ),
            ArticleCard(
                "Engineer Your Software",
                "https://cdna.artstation.com/p/assets/images/images/020/920/848/large/tony-etienne-the-power-bill-was-worse-than-he-expected.jpg?1569690775",
                "https://google.com",
                ['computer science']
            ),
            ArticleCard(
                "Case Study: ML Powered Product Substitutions",
                "https://www.paulkidby.com/wp-content/uploads/2016/01/gallery_2-650x884_c.jpg",
                "https://google.com",
                ['machine learning']
            ),
            ArticleCard(
                "Monads: Explained Simply",
                "https://cdna.artstation.com/p/assets/images/images/051/609/672/large/alariko-1649012335676-ilustracion-sin-titulo-01-01.jpg?1657724675",
                "https://google.com",
                ['computer science']
            ),
            ArticleCard(
                "Thoughts on the Economics of AI and Copyright",
                "https://cdna.artstation.com/p/assets/images/images/079/702/348/large/alariko-img-20240802-175045-178.jpg?1725576581",
                "https://google.com",
                ['ai', 'economics']
            ),
            ArticleCard(
                "The Magic of Lisp Machines",
                "https://sawyer-p.me/images/lisp_machine.jpg",
                "https://google.com",
                ['computer science']
            ),
            cls="grid grid-cols-1 xl:grid-cols-2",
            data_uk_grid="masonry: true"
        ),
        Script(src='./assets/centerpiece.js', type='module'),
    )
