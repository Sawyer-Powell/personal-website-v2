from fasthtml.common import *
from typing import List

def Title(*a, **k):
    return H1(*a, cls="text-foreground text-4xl font-semibold", **k)

def Subtitle(*a, **k):
    return H2(*a, cls="text-foreground !text-2xl italic", **k)

def ArticleCard(
    title: str,
    img: str,
    link: str,
    tags: List[str] = []
):
    return A(
        Div(
            Div(
                Div(
                    P(
                        Span(
                            title,
                            cls="font-bold xl:text-3xl text-2xl bg-background !p-1",
                            style="font-family: JetBrains Mono, monospace; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);"
                        ),
                        cls="text-right w-full py-10 px-3 z-1",
                        style="backdrop-filter: blur(2px) grayscale(50%) brightness(80%)"
                    ),
                    cls="h-full w-full",
                    style="backdrop-filter: blur(1px)"
                ),
                cls="flex items-center justify-center xl:h-[12rem] h-[10rem]",
                style="background-size: cover",
                data_src=img,
                data_uk_img=True
            ),
            Div(
                Div(
                    H3(
                        "March 3, 2025",
                        cls="text-xs p-2"
                    ),
                    cls='flex-1'
                ),
                Div(
                    (
                        Span(
                            tag,
                            cls="uk-badge text-xs mono ms-2"
                        )
                        for tag in tags
                    ),
                    cls='flex-1 text-right'
                ),
                cls='flex flex-row justify-center items-center px-2'
            ),
            cls="uk-card uk-card-body uk-card-default !p-0 m-4 xl:mx-4 mx-0 max-w-lg !shadow-2xl",
            style="overflow: hidden",
        ),
        href=link,
    )

def Logo(small = False):
    return Div(
        Img(
            src="assets/horse.svg",
            style="width: 3rem; height: 3rem" 
                    if not small else
                "width: 2.2rem; height: 2.2rem",
            cls="me-2"
        ),
        H1("sawyer-p", cls="text-foreground !font-semibold" + (" !text-5xl" if not small else " !text-2xl")),
        cls="flex flex-row mb-2"
    )

def NavMenuPage(name: str, link: str, right = True):
    return Li(
        A(
            name,
            cls="mt-2",
            href=link,
            style="float: right; padding: 0 !important" if right else "padding: 0 !important"
        ),
    )

def NavMenuPages(right = True):
    return Ul(
        NavMenuPage("cv", '/', right),
        NavMenuPage("about", '/about', right),
        cls="uk-nav uk-nav-default text-xl mono p-0"
    )

def NavMenu():
    return (
        Div(
            A(
                NotStr('''<uk-icon icon="menu" height=32 width=32></uk-icon>'''),
                cls="uk-btn uk-btn-secondary shadow-xl p-2",
                style="border-radius: 50%; width: 52px; height: 52px",
                href="#offcanvas-menu",
                data_uk_toggle=True
            ),
            cls="uk-position-fixed uk-position-bottom-right m-4 md:d-none xl:hidden",
        ),
        Div(
            Div(
                NavMenuPages(),
                A(
                    Logo(small=True),
                    href="/",
                    cls="mt-8"
                ),
                cls='uk-offcanvas-bar p-4 flex justify-end items-end flex-col'
            ),
            cls="uk-offcanvas xl:hidden", 
            id="offcanvas-menu",
            data_uk_offcanvas="overlay: true; flip: true; mode: push"
        ),
    )

def PageContainer(*a):
    return Body(
        Div(
            Div(
                data_uk_spinner="ratio: 3"
            ),
            id="load-screen",
            cls="min-w-full min-h-[100vh] flex justify-center items-center fixed bg-background z-10 pointer-events-none transition-all"
        ),
        Div(
            Div(
                A(
                    Logo(small=True),
                    href="/",
                ),
                Div(cls='mb-8'),
                NavMenuPages(False),
                cls="p-4 h-fit min-w-sm hidden xl:block fixed",
            ),
            Div(
                Div(
                    *a,
                    cls="xl:w-4xl"
                ),
                cls="m-5 pb-10 flex-1 flex justify-center"
            ),
            cls="flex"
        ),
        NavMenu(),
        Script('''
            const pageBody = document.getElementById('page-body');
            const loadScreen = document.getElementById('load-screen');

            function startLoad() {
                document.body.style.overflow = 'hidden';
                document.body.style.height = '100vh';
            }

            function endLoad() {
                loadScreen.classList.add('opacity-0');
                setTimeout(() => {
                    loadScreen.classList.add('hidden');
                    document.body.style.overflow = '';
                    document.body.style.height = '';
                }, 200);
            }

            startLoad()

            window.addEventListener('load', function() {
                setTimeout(() => {
                    endLoad()
                }, 200);
            });
        '''),
        cls="dark bg-background text-foreground"
    )

