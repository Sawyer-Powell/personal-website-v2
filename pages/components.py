from fasthtml.common import *
from typing import List
import datetime

def Title(*a, **k):
    return H1(*a, cls="text-foreground text-4xl font-semibold", **k)

def Subtitle(*a, **k):
    return H2(*a, cls="text-foreground !text-2xl italic", **k)

def Post(
    article
):
    pretty_date = article['date'].strftime("%B %-d, %Y")

    return PageContainer(
        Div(
            H1(
                article['title'],
                cls="mono !font-semibold !text-5xl !mb-4 !max-w-4xl w-full"
            ),
            H2(
                "image by ", A(article['artist'], href=article['artist-page'], cls='uk-link'),
                cls="mono !text-2xl !italic !mb-8 !max-w-4xl w-full"
            ),
            Img(
                src=article['hero'],
                cls="shadow-xl rounded-xl w-full !max-w-4xl"
            ),
            cls="w-full flex flex-col items-center"
        ),
        Div(
            Div(
                NotStr('''
                    <svg viewBox="0 0 1024 1024" class="icon" version="1.1" xmlns="http://www.w3.org/2000/svg" fill="#ffffff" stroke="#f9f5d7">
                        <g id="SVGRepo_bgCarrier" stroke-width="0">
                        </g>
                        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" stroke="#f9f5d7" stroke-width="2.048">
                        </g>
                        <g id="SVGRepo_iconCarrier">
                            <path d="M431.157895 162.250105V134.736842c0-41.552842-39.289263-80.842105-80.842106-80.842105-28.833684 0-57.128421 4.661895-58.314105 4.850526L269.473684 62.490947v83.887158C144.788211 223.824842 89.222737 346.839579 66.991158 431.157895h266.051368c240.747789 0 415.851789 107.789474 415.85179 269.473684-14.848-25.114947-43.924211-53.894737-88.68379-53.894737-67.988211 0-121.263158 71.033263-121.263158 161.684211 0 66.802526 30.477474 119.888842 60.712421 156.16 12.638316 15.171368 36.055579 37.726316 59.014737 58.88 5.066105 0.107789 9.781895 0.538947 15.009685 0.538947 219.297684 0 350.315789-191.811368 350.315789-377.263158C1024 327.545263 679.855158 172.813474 431.157895 162.250105z" fill="#fe8019">
                            </path>
                            <path d="M673.684211 1024c-114.768842 0-188.820211-33.333895-254.167579-62.787368-53.625263-24.144842-99.974737-45.002105-161.28-45.002106-40.448 0-83.590737 23.255579-103.639579 45.16379l-39.747369-36.432842C142.497684 894.787368 199.168 862.315789 258.236632 862.315789c68.392421 0 119.861895 21.288421 172.921263 45.056V673.684211c0-35.166316-17.542737-64.107789-30.639158-80.815158-15.198316 9.835789-32.067368 18.890105-50.741895 26.947368l-21.342316-49.475368C469.800421 509.413053 485.052632 377.317053 485.052632 323.368421V221.642105A597.827368 597.827368 0 0 0 404.210526 215.578947h-26.947368V134.736842c0-12.099368-14.848-26.947368-26.947369-26.947368-9.377684 0-18.836211 0.592842-26.947368 1.347368V269.473684h-53.894737V211.671579c-136.030316 102.912-158.450526 266.886737-161.306947 295.882105 9.135158 9.108211 38.992842 25.061053 71.976421 38.669474l38.103579-59.365053 12.449684-1.589894C321.212632 473.653895 377.263158 392.192 377.263158 323.368421h53.894737c0 88.333474-68.796632 192.242526-180.870737 213.342316l-48.397474 75.398737-20.291368-7.437474C53.894737 557.756632 53.894737 523.317895 53.894737 512c0-50.041263 37.025684-254.733474 215.578947-365.621895V62.490947l22.528-3.745684C293.187368 58.556632 321.482105 53.894737 350.315789 53.894737c41.552842 0 80.842105 39.289263 80.842106 80.842105v27.513263c248.697263 10.563368 592.842105 165.295158 592.842105 484.486737 0 185.451789-131.018105 377.263158-350.315789 377.263158z m-13.473685-323.368421c-36.513684 0-67.368421 49.367579-67.368421 107.789474 0 85.746526 68.096 145.084632 89.465263 161.549473 91.540211-2.533053 164.378947-45.487158 213.827369-107.654737H700.631579v-53.894736h230.238316c8.919579-17.273263 16.357053-35.354947 22.285473-53.894737h-239.885473l-6.467369-17.650527C706.290526 735.582316 692.439579 700.631579 660.210526 700.631579zM485.052632 931.112421c33.926737 14.066526 70.521263 26.597053 114.607157 33.468632C569.424842 928.309895 538.947368 875.223579 538.947368 808.421053c0-90.650947 53.274947-161.684211 121.263158-161.684211 44.759579 0 73.835789 28.779789 88.68379 53.894737h217.007158c2.775579-17.866105 4.203789-35.920842 4.203789-53.894737 0-38.938947-5.658947-74.752-15.925895-107.627789l-126.706526 126.679579-38.103579-38.103579L932.001684 485.052632a367.939368 367.939368 0 0 0-57.775158-81.596632l-154.543158 154.543158-38.103579-38.103579 153.573053-153.573053a537.869474 537.869474 0 0 0-82.593684-56.751158l-140.665263 140.638316-38.103579-38.103579 128.134737-128.134737A794.731789 794.731789 0 0 0 538.947368 231.046737V323.368421c0 50.149053-11.102316 156.698947-95.932631 236.328421 18.378105 23.417263 42.037895 63.407158 42.037895 113.987369v257.42821zM215.578947 431.157895v-53.894737c39.774316 0 53.894737-29.022316 53.894737-53.894737h53.894737c0 53.571368-37.025684 107.789474-107.789474 107.789474z" fill="#1d2021">
                            </path>
                        </g>
                    </svg>
                '''),
                cls="bg-foreground p-[5px] rounded-full shadow-xl",
                style="width: 2.2rem; height: 2.2rem;"
            ),
            Div(
                pretty_date,
                cls="my-4 mono font-semibold"
            ),
            cls="w-full flex flex-col items-center mt-8"
        ),
        Div(
            Div(
                NotStr(article.content),
                cls='article-body mt-8'
            ),
            cls='w-full flex justify-center'
        )
    )


def ArticleCard(article):
    pretty_date = article['date'].strftime("%B %-d, %Y")

    return A(
        Div(
            Div(
                Div(
                    P(
                        Span(
                            article['title'],
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
                data_src=article['hero'],
                data_uk_img=True
            ),
            Div(
                Div(
                    H3(
                        pretty_date,
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
                        for tag in article['tags']
                    ),
                    cls='flex-1 text-right'
                ),
                cls='flex flex-row justify-center items-center px-2'
            ),
            cls="uk-card uk-card-body uk-card-default !p-0 m-4 xl:mx-4 mx-0 max-w-lg !shadow-2xl",
            style="overflow: hidden",
        ),
        href='/'+article['url'],
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
        NavMenuPage("cv", '/professional-work', right),
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
            cls="uk-position-fixed uk-position-bottom-right m-4 md:d-none 2xl:hidden",
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

def DesktopNavMenu():
    return Div(
        A(
            Logo(small=True),
            href="/",
        ),
        Div(cls='mb-5'),
        NavMenuPages(False),
        cls='''
            h-fit w-sm hidden 2xl:block sticky p-5 top-[1rem] 
            rounded-xl mx-5 opacity-20 hover:opacity-100 transition-all
            hover:bg-card bg-background hover:uk-shadow
        ''',
    )

def TableOfContents():
    return Div(
        cls='''w-sm 2xl:block hidden'''
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
            DesktopNavMenu(),
            Div(
                Div(
                    *a,
                    cls="2xl:w-2xl 3xl:w-4xl"
                ),
                cls="m-5 pb-10 flex justify-center"
            ),
            TableOfContents(),
            cls="flex justify-center"
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

